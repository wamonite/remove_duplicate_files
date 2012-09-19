"""Remove Duplicate Files
Copyright (c) 2012 Warren Moore
https://github.com/wamonite/removeDuplicateFiles

This software may be redistributed under the terms of the MIT License.
See the file LICENSE for details.
"""

##################################################################
# Imports

from optparse import OptionParser
import os
import sys
import hashlib

##################################################################
# Constants

VERSION_STRING = "1.0"
DEFAULT_VERBOSE = False
DEFAULT_PRUNE = True
DEFAULT_DRY_RUN = False
DEFAULT_DEBUG = False

##################################################################
# Functions

def hashFile(options, directory, fileNameRelative):
  try:
    fileObject = open(os.path.join(directory, fileNameRelative), "rb")
    fileData = fileObject.read()
    fileObject.close()
    
  except Exception as e:
    print >> sys.stderr, "Unable to read '%s'" % fileNameAbsolute
    raise
  
  hashObject = hashlib.md5()
  hashObject.update(fileNameRelative)
  hashObject.update(fileData)
  
  return hashObject.digest()
  
def processDirectory(options, directory, hashValueDict, directoryDirtySet):
  if not os.path.exists(directory):
    raise IOError("Directory '%s' not found" % directory)
  
  if not os.path.isdir(directory):
    raise IOError("'%s' is not a directory" % directory)
  
  for root, directoryList, fileNameList in os.walk(directory):
    if options.verbose and not options.debug:
      print "Scanning: '%s'" % root
      
    for fileName in fileNameList:
      fileNameAbsolute = os.path.join(root, fileName)
      fileNameRelative = os.path.relpath(fileNameAbsolute, directory)
      
      if options.debug:
        print "Scanning: '%s'" % fileNameAbsolute
      
      if os.path.islink(fileNameAbsolute):
        if options.debug:
          print "Link: '%s'" % fileNameAbsolute
          
        continue
      
      try:
        hashValue = hashFile(options, directory, fileNameRelative)
        
      except:
        continue
      
      if hashValue in hashValueDict:
        directoryDirtySet.add(root)

      hashList = hashValueDict.setdefault(hashValue, [])
      hashList.append((directory, fileNameRelative))
      
def pruneDirectories(options, directoryDirtySet):
  for directory in directoryDirtySet:
    if options.debug:
      print "Pruning: '%s'" % directory
      
    if not options.dryRun:
      try:
        # Throws OSError if not empty
        os.rmdir(directory)
        
        if options.verbose:
          print "Pruned: '%s'" % directory
        
      except:
        pass
  
def findDuplicates(options, directoryList):
  hashValueDict = {}
  directoryDirtySet = set()
  
  for directory in directoryList:
    processDirectory(options, os.path.abspath(directory), hashValueDict, directoryDirtySet)
    
  for hashValue, fileNameList in hashValueDict.iteritems():
    if len(fileNameList) > 1:
      if options.debug:
        print "Duplicate: '%s'" % fileNameList[0][1]
        print "\n".join("  '%s'" % fileNameRoot for fileNameRoot, fileNameRelative in fileNameList)
      
      for fileNameRoot, fileNameRelative in fileNameList[1:]:
        fileNameAbsolute = os.path.join(fileNameRoot, fileNameRelative)
        if options.verbose:
          print "Removing%s: '%s'" % (("", " (dry run)")[options.dryRun], fileNameAbsolute)
            
        if not options.dryRun:
          os.remove(fileNameAbsolute)

  if options.prune:
    pruneDirectories(options, directoryDirtySet)
    
def main():
  applicationName = os.path.basename(__file__)
  
  parserUsage = "Usage: %s [options] [directories]" % applicationName
  parser = OptionParser(usage = parserUsage, version = "%prog " + VERSION_STRING)
  parserDefaults = {"verbose": DEFAULT_VERBOSE,
                    "prune": DEFAULT_PRUNE,
                    "dryRun": DEFAULT_DRY_RUN,
                    "debug": DEFAULT_DEBUG}
  parser.set_defaults(**parserDefaults)
  parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose", help = "verbose output [default: %default]")
  parser.add_option("-p", "--prune", action = "store_true", dest = "prune", help = "remove directories that have been emptied [default: %default]")
  parser.add_option("-n", "--dry-run", action = "store_true", dest = "dryRun", help = "don't remove files or directories [default: %default]")
  parser.add_option("-d", "--debug", action = "store_true", dest = "debug", help = "enable debug output [default: %default]")
  
  (options, args) = parser.parse_args()

  try:
    findDuplicates(options, args)
    
  except Exception as e:
    if options.debug:
      raise
    
    else:
      print >> sys.stderr, "%s error: %s" % (applicationName, e.__str__())
  
##################################################################
# Main

if __name__ == "__main__":
  main()
