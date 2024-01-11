#!/usr/bin/env python3
# This file is a part of marzer/check_cmake and is subject to the the terms of the MIT license.
# Copyright (c) Mark Gillard <mark.gillard@outlook.com.au>
# See https://github.com/marzer/check_cmake/blob/main/LICENSE.txt for the full license text.
# SPDX-License-Identifier: MIT

import re
from io import StringIO

import colorama

from . import utils
from .colour import *
from .grid import Grid

INDENT = '  '


class Link(object):
    def __init__(self, uri, description=None):
        self.uri = str(uri)
        self.description = description
        if self.description is not None:
            self.description = str(self.description)
        else:
            last_slash = self.uri.rfind('/')
            last_dot = self.uri.rfind('.')
            if last_slash == -1 or last_dot == -1 or last_dot < last_slash:
                return
            self.description = self.uri[last_slash + 1 : last_dot]
            if (
                re.fullmatch('[a-z_]+', self.description)
                and re.match('^(set_|target_|find_|project)', self.description)
                and not re.match('\(\s*\)\s*$', self.description)
            ):
                self.description += '()'

    def __bool__(self):
        return bool(self.uri)

    def __str__(self):
        if self.description:
            return rf'{self.description}: {self.uri}'
        return self.uri


class Links(object):
    target_compile_options = Link('https://cmake.org/cmake/help/latest/command/target_compile_options.html')
    target_compile_features = Link('https://cmake.org/cmake/help/latest/command/target_compile_features.html')
    target_compile_definitions = Link('https://cmake.org/cmake/help/latest/command/target_compile_definitions.html')
    target_link_libraries = Link('https://cmake.org/cmake/help/latest/command/target_link_libraries.html')
    target_include_directories = Link('https://cmake.org/cmake/help/latest/command/target_include_directories.html')
    effective_modern_cmake = Link(
        'https://gist.github.com/mbinna/c61dbb39bca0e4fb7d1f73b0d66a4fd1', 'Effective Modern CMake'
    )
    set_target_properties = Link('https://cmake.org/cmake/help/latest/command/set_target_properties.html')
    INSTALL_RPATH = Link('https://cmake.org/cmake/help/latest/prop_tgt/INSTALL_RPATH.html')
    CMAKE_C_KNOWN_FEATURES = Link('https://cmake.org/cmake/help/latest/prop_gbl/CMAKE_C_KNOWN_FEATURES.html')
    CMAKE_CXX_KNOWN_FEATURES = Link('https://cmake.org/cmake/help/latest/prop_gbl/CMAKE_CXX_KNOWN_FEATURES.html')
    private_public_interface = Link(
        'https://leimao.github.io/blog/CMake-Public-Private-Interface/', 'Public vs. Private vs. Interface'
    )
    FindThreads = Link('https://cmake.org/cmake/help/latest/module/FindThreads.html')
    find_package = Link('https://cmake.org/cmake/help/latest/command/find_package.html')
    POSITION_INDEPENDENT_CODE = Link('https://cmake.org/cmake/help/latest/prop_tgt/POSITION_INDEPENDENT_CODE.html')
    project = Link('https://cmake.org/cmake/help/latest/command/project.html')


def make_example(str):
    return Grid(str.strip(), line_number=-999999, indent=INDENT * 2)


class Examples(object):
    INSTALL_RPATH = make_example(
        r'''
get_target_property(my_current_rpaths my_lib INSTALL_RPATH)
list(APPEND my_current_rpaths "/opt/lib")
set_target_properties(my_lib PROPERTIES INSTALL_RPATH "${my_current_rpaths}")
'''
    )

    FindThreads = make_example(
        r'''
find_package(Threads REQUIRED)
target_link_libraries(my_lib PUBLIC Threads::Threads)
'''
    )

    POSITION_INDEPENDENT_CODE = make_example('set_target_properties(my_lib PROPERTIES POSITION_INDEPENDENT_CODE ON)')


class Span(object):
    def __init__(self, start: int, length: int = 1, end: int = None):
        self.start = int(start)
        assert self.start >= 0
        if end is not None:
            self.length = int(end) - self.start
        else:
            self.length = int(length)
        assert self.length >= 0

    def __bool__(self):
        return bool(self.length)

    def __len__(self) -> int:
        return self.length

    @property
    def end(self) -> int:
        return self.start + self.length


class Issue(object):
    def __init__(
        self,
        source_path: str,
        source_text: str,
        description: str,
        span: Span,
        context: Span = None,
        replace_with=None,
        more_info=None,
        example=None,
    ):
        self.source_path = str(source_path) if source_path is not None else None
        self.description = str(description)
        assert self.description

        assert span is not None
        self.span = span
        self.context = span if context is None else context
        assert self.context.start <= self.span.start
        assert self.context.end >= self.span.end

        self.line_and_column = utils.calc_line_and_column(source_text, span.start)

        self.grid = Grid(source_text[self.context.start : self.context.end], indent=INDENT * 2)
        self.grid.line_number = self.line_and_column[0]
        grid_highlight_range = self.grid.find_range(source_text[self.span.start : self.span.end])
        if grid_highlight_range is not None:
            self.grid.style_range(
                first_line=grid_highlight_range[0],
                first_col=grid_highlight_range[1],
                last_line=grid_highlight_range[2],
                last_col=grid_highlight_range[3],
                colour=colorama.Fore.RED,
            )
            self.grid.style_range(
                first_line=grid_highlight_range[2],
                first_col=grid_highlight_range[3] + 1,
                last_line=99999,
                last_col=99999,
                style=colorama.Style.RESET_ALL,
            )

        self.example = example
        self.replace_with = str(replace_with) if replace_with is not None else None
        self.more_info = None
        if more_info is not None:
            self.more_info = [i for i in list(utils.coerce_collection(more_info)) if i]
            for i in range(len(self.more_info)):
                if isinstance(self.more_info[i], str):
                    self.more_info[i] = Link(self.more_info[i])

    def __str__(self):
        with StringIO() as buf:
            buf.write('\n')
            buf.write(colorama.Style.BRIGHT)
            if self.source_path:
                buf.write(f'{self.source_path}')
            else:
                buf.write(f'<file>')
            buf.write(rf':{self.line_and_column[0]}:{self.line_and_column[1]}: {colorama.Style.RESET_ALL}')
            buf.write(self.description)
            if self.grid:
                buf.write(f'\n{INDENT}{colorama.Style.BRIGHT}Context:{colorama.Style.RESET_ALL}\n{self.grid}')
            if self.replace_with:
                buf.write(
                    f'\n{INDENT}{colorama.Style.BRIGHT}Replace with:{colorama.Style.RESET_ALL}\n{INDENT*2}{self.replace_with}'
                )
            if self.example:
                buf.write(f'\n{INDENT}{colorama.Style.BRIGHT}Example:{colorama.Style.RESET_ALL}\n{self.example}')
            if self.more_info:
                buf.write(f'\n{INDENT}{colorama.Style.BRIGHT}More information:{colorama.Style.RESET_ALL}')
                for info in self.more_info:
                    buf.write(f'\n{INDENT*2}{info}')
            return buf.getvalue().lstrip()


def lint_using_regex(
    source_path: str,
    source_text: str,
    description: str,
    pattern: str,
    inner_group_index=1,
    inner_group_must_match: str = None,
    flags=0,
    **kwargs,
):
    results = []
    flags = flags | re.DOTALL
    patterns = utils.coerce_collection(pattern)
    for pattern in patterns:
        for m in re.finditer(pattern, source_text, flags=flags):
            try:
                m[inner_group_index]
            except IndexError:
                inner_group_index = 0
            if inner_group_must_match is not None:
                m2 = re.search(inner_group_must_match, str(m[inner_group_index]), flags=flags)
                if m2:
                    continue
            for i in range(10):
                try:
                    description = description.replace(f'\\{i}', str(m[i]))
                except IndexError:
                    pass
            results.append(
                Issue(
                    source_path=source_path,
                    source_text=source_text,
                    description=description,
                    span=Span(m.start(inner_group_index), end=m.end(inner_group_index)),
                    context=Span(
                        utils.find_first_char_on_line(source_text, m.start(0)),
                        end=utils.find_last_char_on_line(source_text, m.end(0) - 1) + 1,
                    ),
                    **kwargs,
                )
            )
    return results


def specify_project_version(source_path: str, source_text: str):
    return lint_using_regex(
        source_path=source_path,
        source_text=source_text,
        description=rf'project() should specify a {bright("VERSION", colour="yellow")}',
        pattern=r'\bproject\s*\(([^)]*?)\)',
        inner_group_must_match=r'\bVERSION\b',
        more_info=Links.project,
    )


def specify_scope_on_target_functions(source_path: str, source_text: str):
    return lint_using_regex(
        source_path=source_path,
        source_text=source_text,
        description=rf'\1() should specify at least one dependency scope '
        rf'({bright("PRIVATE", colour="yellow")}, {bright("INTERFACE", colour="yellow")} or {bright("PUBLIC", colour="yellow")}) ',
        pattern=r'\b(target_(?:link_(?:options|libraries)|compile_(?:options|features|definitions)|(?:include|link)_directories))\s*\(([^)]*?)\)',
        inner_group_index=2,
        inner_group_must_match=r'\b(?:PRIVATE|PUBLIC|INTERFACE)\b',
        more_info=(Links.private_public_interface, Links.effective_modern_cmake),
    )


def use_set_target_properties_rpath(source_path: str, source_text: str):
    return lint_using_regex(
        source_path=source_path,
        source_text=source_text,
        description=rf'rpaths should be set using {bright("set_target_properties()", colour="yellow")} and {bright("INSTALL_RPATH", colour="yellow")}',
        pattern=r'(-Wl,-rpath=)',
        replace_with=Links.set_target_properties,
        more_info=Links.INSTALL_RPATH,
        example=Examples.INSTALL_RPATH,
    )


def use_set_target_properties_pic(source_path: str, source_text: str):
    return lint_using_regex(
        source_path=source_path,
        source_text=source_text,
        description=rf'position-independent code should be set per-target using {bright("set_target_properties()", colour="yellow")} and {bright("POSITION_INDEPENDENT_CODE", colour="yellow")}',
        pattern=r'\bset\s*\([^)]*?\b(CMAKE_POSITION_INDEPENDENT_CODE)\b[^)]*?\)',
        replace_with=Links.set_target_properties,
        example=Examples.POSITION_INDEPENDENT_CODE,
        more_info=Links.POSITION_INDEPENDENT_CODE,
    )


def use_target_compile_definitions(source_path: str, source_text: str):
    return lint_using_regex(
        source_path=source_path,
        source_text=source_text,
        description=rf'compiler defines should be set on a per-target basis using {bright("target_compile_definitions()", colour="yellow")}',
        pattern=r'\b(add_(?:compile_)?definitions)\s*\([^)]*?\)',
        replace_with=Links.target_compile_definitions,
        more_info=Links.effective_modern_cmake,
    )


def use_target_compile_features_language_standard(source_path: str, source_text: str):
    return lint_using_regex(
        source_path=source_path,
        source_text=source_text,
        description=rf'language standard level should be set on a per-target basis using {bright("target_compile_features()", colour="yellow")}',
        pattern=(
            r'\bset_target_properties\s*\([^)]*?\b(C(?:XX)?_STANDARD)\b[^)]*?\)',
            r'\bset\s*\(\s*\b(CMAKE_C(?:XX)?_STANDARD)\b[^)]*?\)',
        ),
        replace_with=Links.target_compile_features,
        more_info=(Links.CMAKE_CXX_KNOWN_FEATURES, Links.CMAKE_C_KNOWN_FEATURES),
    )


def use_target_compile_options(source_path: str, source_text: str):
    return lint_using_regex(
        source_path=source_path,
        source_text=source_text,
        description=rf'compiler options should be set on a per-target basis using {bright("target_compile_options()", colour="yellow")}',
        pattern=(r'\b(add_compile_options)\s*\([^)]*?\)', r'\bset\s*\(\s*(CMAKE_C(?:XX)?_FLAGS)\b[^)]*?\)'),
        replace_with=Links.target_compile_options,
        more_info=Links.effective_modern_cmake,
    )


def use_target_include_directories(source_path: str, source_text: str):
    return lint_using_regex(
        source_path=source_path,
        source_text=source_text,
        description=rf'include paths should be set on a per-target basis using {bright("target_include_directories()", colour="yellow")}',
        pattern=r'\b(include_directories)\s*\([^)]*?\)',
        replace_with=Links.target_include_directories,
        more_info=Links.effective_modern_cmake,
    )


def use_target_link_libraries(source_path: str, source_text: str):
    return lint_using_regex(
        source_path=source_path,
        source_text=source_text,
        description=rf'linker paths should be inherited from library targets using {bright("target_link_libraries()", colour="yellow")}',
        pattern=r'\b(link_directories)\s*\([^)]*?\)',
        replace_with=Links.target_link_libraries,
        more_info=Links.effective_modern_cmake,
    )


def use_threads_package(source_path: str, source_text: str):
    return lint_using_regex(
        source_path=source_path,
        source_text=source_text,
        description=rf'support for threading should be provided by linking with {bright("Threads::Threads", colour="yellow")} from the {bright("Threads", colour="yellow")} package',
        pattern=r'\btarget_link_libraries\s*\([^)]*?\b(pthread)\b[^)]*?\)',
        replace_with='Threads::Threads',
        example=Examples.FindThreads,
        more_info=(Links.FindThreads, Links.find_package),
    )


LINTS = [
    specify_project_version,
    specify_scope_on_target_functions,
    use_set_target_properties_rpath,
    use_set_target_properties_pic,
    use_target_compile_definitions,
    use_target_compile_features_language_standard,
    use_target_compile_options,
    use_target_include_directories,
    use_target_link_libraries,
    use_threads_package,
]


__all__ = ['Issue', 'LINTS']
