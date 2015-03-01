#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Remove duplicate files
Copyright (c) 2012-2015 Warren Moore
https://github.com/wamonite/removeDuplicateFiles

This software may be redistributed under the terms of the MIT License.
See the file LICENSE for details.
"""

from __future__ import print_function, unicode_literals
import argparse
import os
import sys
import hashlib

VERSION_STRING = "1.1"
DEFAULT_VERBOSE = False
DEFAULT_PRUNE = True
DEFAULT_DRY_RUN = False
DEFAULT_DEBUG = False


class ScriptException(Exception):
    """Derived exception to throw simple error messages"""


def hash_file(directory, file_name_relative):
    """Return a hash for the file in the specified directory"""

    file_name = os.path.join(directory, file_name_relative)

    try:
        with open(file_name, 'rb') as file_object:
            file_data = file_object.read()

    except IOError:
        raise ScriptException('Unable to read (%s)' % file_name)

    hash_object = hashlib.md5()
    hash_object.update(file_name_relative)
    hash_object.update(file_data)

    return hash_object.digest()


def process_directory(directory, hash_value_lookup, directory_dirty_set, verbose, debug):
    """Walk the directory and generate hashes the files contained"""

    if not os.path.exists(directory):
        raise ScriptException("Directory (%s) not found" % directory)

    if not os.path.isdir(directory):
        raise ScriptException("(%s) is not a directory" % directory)

    for root, directory_list, file_name_list in os.walk(directory):
        if verbose and not debug:
            print("Scanning (%s)" % root)

        for file_name in file_name_list:
            file_name_absolute = os.path.join(root, file_name)
            file_name_relative = os.path.relpath(file_name_absolute, directory)

            if debug:
                print("Scanning (%s)" % file_name_absolute)

            if os.path.islink(file_name_absolute):
                if debug:
                    print("Link (%s)" % file_name_absolute)

                continue

            hash_value = hash_file(directory, file_name_relative)

            if hash_value in hash_value_lookup:
                directory_dirty_set.add(root)

            hash_list = hash_value_lookup.setdefault(hash_value, [])
            hash_list.append((directory, file_name_relative))


def prune_directories(directory_dirty_set, verbose, dry_run, debug):
    """For all directories that have had files removed, delete if empty"""

    for directory in directory_dirty_set:
        if not os.listdir(directory):
            if debug:
                print("Pruning (%s)" % directory)

            if not dry_run:
                try:
                    os.rmdir(directory)

                    if verbose:
                        print("Pruned (%s)" % directory)

                except OSError:
                    raise ScriptException('Failed to prune directory (%s)' % directory)


def process_directories(directory_list, verbose, dry_run, prune, debug):
    """Find and remove duplicate files from directories listed"""

    hash_value_lookup = {}
    directory_dirty_set = set()

    for directory in directory_list:
        process_directory(os.path.abspath(directory), hash_value_lookup, directory_dirty_set, verbose, debug)

    for hash_value, file_name_list in hash_value_lookup.iteritems():
        if len(file_name_list) > 1:
            if debug:
                print("Duplicate (%s)" % file_name_list[0][1])
                print("\n".join("  (%s)" % file_name_root for file_name_root, file_name_relative in file_name_list))

        for file_name_root, file_name_relative in file_name_list[1:]:
            file_name_absolute = os.path.join(file_name_root, file_name_relative)
            if verbose:
                action = 'Would remove' if dry_run else 'Removing'
                print("%s (%s)" % (action, file_name_absolute))

            if not dry_run:
                os.remove(file_name_absolute)

    if prune:
        prune_directories(directory_dirty_set, verbose, dry_run, debug)


def bool_action(default_bool):
    return 'store_false' if default_bool else 'store_true'


def minimum_args(nmin):
    """Check a minimum number of arguments are provided"""

    class MinimumLength(argparse.Action):
        def __call__(self, parser, args, values, option_string = None):
            if len(values) < nmin:
                msg = 'argument "{arg}" requires at least {nmin} arguments'.format(arg = self.dest, nmin = nmin)
                parser.error(msg)

            setattr(args, self.dest, values)

    return MinimumLength


def get_arguments():
    parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-V', '--version', action='version', version = '%(prog)s v' + VERSION_STRING)
    parser.add_argument('-v', '--verbose', action = bool_action(DEFAULT_VERBOSE), help = "verbose output")
    parser.add_argument("-p", "--prune", action = bool_action(DEFAULT_PRUNE), help = "remove directories that have been emptied")
    parser.add_argument("-n", "--dry-run", action = bool_action(DEFAULT_DRY_RUN), help = "don't remove files or directories")
    parser.add_argument("-d", "--debug", action = bool_action(DEFAULT_DEBUG), help = "enable debug output")
    parser.add_argument('directories', nargs = argparse.REMAINDER, action = minimum_args(2), help = 'directories to compare')

    return parser.parse_args()


if __name__ == "__main__":
    try:
        args = get_arguments()
        process_directories(args.directories, args.verbose, args.dry_run, args.prune, args.debug)

    except ScriptException as e:
        print('Error:', e, file = sys.stderr)
        sys.exit(1)
