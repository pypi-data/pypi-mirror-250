# check_cmake

A simple linter for CMake.

## Installation

`check_cmake` requires Python 3.

```
pip3 install check_cmake
```

## Usage

`check_cmake` is a command-line application

```
usage: check_cmake [-h] [--version] [--recurse | --no-recurse] [--limit LIMIT] [<dir>]

CMake checker for C and C++ projects.

positional arguments:
  <dir>                 path to the project root

options:
  -h, --help            show this help message and exit
  --version             print the version and exit
  --recurse, --no-recurse
                        recurse into subfolders
  --limit LIMIT         maximum errors to emit

v0.0.1 - github.com/marzer/check_cmake
```
