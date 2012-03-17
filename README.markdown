# removeDuplicateFiles
Copyright (c) 2012 Warren Moore <robowaz@gmail.com>
https://github.com/robowaz/removeDuplicateFiles

## About

I had a number of backups containing similar files. To make sure I only reviewed
files once, I wrote this script to remove any duplicates. Files are deemed
duplicates if they are in the same location, relative to the search directories,
and have identical binary content.

## Usage

    python removeDuplicateFiles.py [options] [directories]

    Options:
      --version      show program's version number and exit
      -h, --help     show this help message and exit
      -v, --verbose  verbose output [default: False]
      -p, --prune    remove directories that have been emptied [default: True]
      -n, --dry-run  don't remove files or directories [default: False]
      -d, --debug    enable debug output [default: False]

## Prerequisites

No extra modules required. Tested on Python 2.6 (OSX) and 2.7 (Linux).

## Change Log

* 1.0
  * Initial release

## To Do

* Improve performance by splitting into tests into multiple passes.

## License

This software may be redistributed under the terms of the MIT License.
See the file COPYING for details.
