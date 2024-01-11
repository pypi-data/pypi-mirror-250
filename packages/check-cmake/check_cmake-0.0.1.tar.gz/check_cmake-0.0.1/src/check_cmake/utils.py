#!/usr/bin/env python3
# This file is a part of marzer/check_cmake and is subject to the the terms of the MIT license.
# Copyright (c) Mark Gillard <mark.gillard@outlook.com.au>
# See https://github.com/marzer/check_cmake/blob/main/LICENSE.txt for the full license text.
# SPDX-License-Identifier: MIT

from misk import *


def calc_line_and_column(text: str, pos: int) -> tuple[int, int]:
    assert 0 <= pos <= len(text)
    line = 0
    col = 0
    for i in range(min(len(text), pos)):
        if text[i] == '\n':
            line += 1
            col = 0
        else:
            col += 1
    return (line + 1, col + 1)


def find_first_char_on_line(text: str, pos: int) -> int:
    assert 0 <= pos <= len(text)
    if text:
        pos = max(min(len(text) - 1, pos), 0)
        assert text[pos] != '\n'
        for i in range(pos, -1, -1):
            if text[i] == '\n':
                return i + 1
    return 0


def find_last_char_on_line(text: str, pos: int) -> int:
    assert 0 <= pos <= len(text)
    if text:
        pos = max(min(len(text) - 1, pos), 0)
        assert text[pos] != '\n'
        for i in range(pos, len(text)):
            if text[i] == '\n':
                return i - 1
        return len(text) - 1
    return 0


__all__ = ['calc_line_and_column', 'find_first_char_on_line', 'find_last_char_on_line']

TEST_STRING = r'''
a        |
|   b    |
|      c d
'''.strip()

assert calc_line_and_column(TEST_STRING, TEST_STRING.find('a')) == (1, 1)
assert calc_line_and_column(TEST_STRING, TEST_STRING.find('b')) == (2, 5)
assert calc_line_and_column(TEST_STRING, TEST_STRING.find('c')) == (3, 8)
assert calc_line_and_column(TEST_STRING, TEST_STRING.find('d')) == (3, 10)
