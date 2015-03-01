# remove_duplicate_files

I had a number of backups containing similar files. To make sure I only reviewed
files once, I wrote this script to remove any duplicates. Files are deemed
duplicates if they are in the same location, relative to the search directories,
and have identical binary content.

[source @ github](https://github.com/wamonite/remove_duplicate_files)

## Usage

    usage: removeDuplicateFiles.py [-h] [-V] [-v] [-p] [-n] [-d] ...
    
    positional arguments:
      directories    directories to compare
    
    optional arguments:
      -h, --help     show this help message and exit
      -V, --version  show program's version number and exit
      -v, --verbose  verbose output (default: False)
      -p, --prune    remove directories that have been emptied (default: True)
      -n, --dry-run  don't remove files or directories (default: False)
      -d, --debug    enable debug output (default: False)

Directory arguments are scanned left to right. Duplicates are removed in
the order they are found.

## Prerequisites

No extra modules required. Tested on Python 2.6 (OSX) and 2.7 (Linux).

## Change Log

### 1.1
* Minor improvements and rename

### 1.0
* Initial release

## To Do

* Improve performance by splitting into tests into multiple passes.

## License

Copyright (c) 2012-2015 Warren Moore

This software may be redistributed under the terms of the MIT License.
See the file LICENSE for details.

## Contact

          @wamonite     - twitter
           \_______.com - web
    warren____________/ - email
