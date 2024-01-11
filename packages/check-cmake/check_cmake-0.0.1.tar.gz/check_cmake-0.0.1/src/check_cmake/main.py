#!/usr/bin/env python3
# This file is a part of marzer/check_cmake and is subject to the the terms of the MIT license.
# Copyright (c) Mark Gillard <mark.gillard@outlook.com.au>
# See https://github.com/marzer/check_cmake/blob/main/LICENSE.txt for the full license text.
# SPDX-License-Identifier: MIT

import argparse
import shutil
import subprocess
import sys
from io import StringIO
from pathlib import Path

import colorama

from . import lints, paths, utils
from .colour import *
from .version import *


def error(text):
    print(rf"{bright(rf'error:', 'red')} {text}", file=sys.stderr)


def strip_cmake_comments(text: str) -> str:
    # todo: this currently does not support cmake's multi-line bracket syntax,
    # nor does it take strings into account (so a # in a string will count as a comment)
    in_comment = False
    with StringIO() as buf:
        for c in text:
            if in_comment:
                if c == '\n':
                    buf.write('\n')
                    in_comment = False
            else:
                if c == '#':
                    in_comment = True
                else:
                    buf.write(c)
        return buf.getvalue()


def main_impl():
    args = argparse.ArgumentParser(
        description=r'CMake checker for C and C++ projects.',
        epilog=rf'v{VERSION_STRING} - github.com/marzer/check_cmake',
    )
    args.add_argument(
        r"root", type=Path, metavar=r"<dir>", nargs=r'?', default=Path('.'), help="path to the project root"
    )
    args.add_argument(r'--version', action=r'store_true', help=r"print the version and exit", dest=r'print_version')
    args.add_argument(
        r"--recurse", action=argparse.BooleanOptionalAction, default=True, help=rf"recurse into subfolders"
    )
    args.add_argument(r"--limit", type=int, default=0, help="maximum errors to emit")
    args.add_argument(r'--where', action=r'store_true', help=argparse.SUPPRESS)
    args = args.parse_args()

    if args.print_version:
        print(VERSION_STRING)
        return

    if args.where:
        print(paths.PACKAGE)
        return

    print(rf'{bright("check_cmake", colour="cyan")} v{VERSION_STRING}')

    if not args.root.is_dir():
        return rf"root '{bright(args.root)}' did not exist or was not a directory"

    root_absolute = args.root.resolve()
    print(f'root: {root_absolute}')

    root_is_git_repo = (args.root / ".git").exists()
    git_ok = False
    if root_is_git_repo:
        print('detected git repository')
        git_ok = shutil.which('git') is not None
        if not git_ok:
            print(rf"{bright(rf'warning:', 'yellow')} could not detect git; .gitignore rules will not be respected")
        else:
            print('detected git')

    issue_count = 0
    file_count = 0
    prev_print_was_issue = False

    def print_ex(*args):
        nonlocal prev_print_was_issue
        prev_print_was_issue = False
        print(*args)

    def lint_directory(dir: Path, level=0):
        nonlocal args
        nonlocal root_is_git_repo
        nonlocal issue_count
        nonlocal file_count
        nonlocal prev_print_was_issue
        dir_absolute = dir.resolve()
        dir = dir_absolute.relative_to(root_absolute)
        # check if this directory contains known "ignore me" markers
        if level > 0:
            if root_is_git_repo and (dir / ".git").exists():
                print_ex(rf'detected {bright(dir)} as {bright("git subproject")}; skipping')
                return
            if (dir / 'build.ninja').is_file():
                print_ex(rf'detected {bright(dir)} as {bright("ninja")} build folder; skipping')
                return
            if (dir / 'CMakeCache.txt').is_file():
                if (dir / 'Makefile').is_file():
                    print_ex(rf'detected {bright(dir)} as {bright("GNU Make")} build folder; skipping')
                else:
                    print_ex(rf'detected {bright(dir)} as {bright("CMake")} build folder; skipping')
                return
            if (dir / 'meson-info').is_dir() or (dir / 'meson-logs').is_dir() or (dir / 'meson-private').is_dir():
                print_ex(rf'detected {bright(dir)} as {bright("meson")} build folder; skipping')
                return
        for item in dir.iterdir():
            # subdirectories
            if item.is_dir():
                if args.recurse:
                    lint_directory(item, level + 1)
            # files
            elif item.is_file():
                # skip non-CMake files
                if not (item.name.lower() == 'cmakelists.txt' or item.suffix.lower() == '.cmake'):
                    continue
                # skip .gitignored files
                if root_is_git_repo and git_ok:
                    if (
                        subprocess.run(
                            ['git', 'check-ignore', '--quiet', str(item)],
                            capture_output=True,
                            encoding='utf-8',
                            cwd=str(dir),
                            check=False,
                        ).returncode
                        == 0
                    ):
                        continue
                # read all text and get all lints
                file_count += 1
                text = utils.read_all_text_from_file(item)
                text = strip_cmake_comments(text)
                full_path = item.resolve()
                issues_in_file = []
                issues_in_file: list[lints.Issue]
                for lint in lints.LINTS:
                    issues = lint(full_path, text)
                    if issues is not None:
                        issues_in_file += list(utils.coerce_collection(issues))
                # sort lints by start location and print
                issues_in_file.sort(key=lambda i: i.span.start)
                for issue in issues_in_file:
                    if not prev_print_was_issue:
                        print('')
                    print(f"{bright(rf'error:', 'red')} {issue}\n")
                    prev_print_was_issue = True
                    issue_count += 1
                    if args.limit > 0 and issue_count >= args.limit > 0:
                        print_ex(f"reached error limit, stopping.")
                        return

    lint_directory(args.root)

    print_ex(
        rf'found {issue_count} error{"s" if issue_count > 1 else ""} in {file_count} file{"s" if file_count > 1 else ""}.'
    )
    return issue_count


def main():
    colorama.init()
    result = None
    try:
        result = main_impl()
        if result is None:
            sys.exit(0)
        elif isinstance(result, int):
            sys.exit(result)
        elif isinstance(result, str):  # error message
            error(result)
            sys.exit(-1)
        else:
            error('unexpected result type')
            sys.exit(-1)
    except SystemExit as exit:
        raise exit from None
    except argparse.ArgumentError as err:
        error(err)
        sys.exit(-1)
    except BaseException as err:
        with StringIO() as buf:
            buf.write(
                f'\n{dim("*************", "red")}\n\n'
                'You appear to have triggered an internal bug!'
                f'\n{style("Please file an issue at github.com/marzer/check_cmake/issues")}'
                '\nMany thanks!'
                f'\n\n{dim("*************", "red")}\n\n'
            )
            utils.print_exception(err, include_type=True, include_traceback=True, skip_frames=1, logger=buf)
            buf.write(f'{dim("*************", "red")}\n')
            print(buf.getvalue(), file=sys.stderr)
        sys.exit(-1)
