################################################################################
### Copyright © 2012 BlackDragonHunt
### 
### This file is part of the Super Duper Script Editor.
### 
### The Super Duper Script Editor is free software: you can redistribute it
### and/or modify it under the terms of the GNU General Public License as
### published by the Free Software Foundation, either version 3 of the License,
### or (at your option) any later version.
### 
### The Super Duper Script Editor is distributed in the hope that it will be
### useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
### MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
### GNU General Public License for more details.
### 
### You should have received a copy of the GNU General Public License
### along with the Super Duper Script Editor.
### If not, see <http://www.gnu.org/licenses/>.
################################################################################

from csv import DictReader, DictWriter
from collections import defaultdict
import codecs
import hashlib
import os.path
import sys
import shutil

file_list = []
GROUP_SIZES = {}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, 'data/dupes.csv')

################################################################################
### SOME FUNCTIONS
################################################################################

def normalize_filename(filename):
  return os.path.normpath(os.path.normcase(filename))

class DupesDB:
  def __init__(self, csv_file = CSV_FILE):
    
    self.dupes = defaultdict(set)
    self.csv_file = csv_file
    
    self.load_csv(self.csv_file)
  
  def load_csv(self, csv_file = None):
    if csv_file == None:
      csv_file = self.csv_file
    
    self.dupes.clear()

    # Load in our CSV.
    dupes_csv = DictReader(open(csv_file, 'rb'))

    for row in dupes_csv:
      group     = int(row['Group'])
      filename  = normalize_filename(row['File'])
      
      self.dupes[group].add(filename)
  
  def save_csv(self, csv_file = None):
    if csv_file == None:
      csv_file = self.csv_file
    
    dupes_csv = DictWriter(open(csv_file, 'wb'), fieldnames = ['Group', 'File'])
    dupes_csv.writerow({'Group':'Group', 'File':'File'})
    
    for group in sorted(self.dupes.keys()):
      files = self.dupes[group]
      
      # No point in keeping it if there aren't at least two files.
      if len(files) < 2:
        continue
      
      for filename in sorted(files):
        dupes_csv.writerow({'Group': group, 'File': filename})
  
  def files_in_group(self, group):
    
    if not group in self.dupes:
      return None
    else:
      return self.dupes[group]
  
  def group_from_file(self, filename):
    
    filename = normalize_filename(filename)
    
    for group in self.dupes:
      if filename in self.dupes[group]:
        return group
    
    return None
  
  def files_in_same_group(self, filename):
    
    group = self.group_from_file(filename)
    
    if not group == None:
      return self.files_in_group(group)
    
    return None
  
  def is_file_in_group(self, filename, group):
    filename = normalize_filename(filename)
    return filename in self.dupes[group]

  ################################################################################
  ### @fn   add_file(file, group)
  ### @desc Adds the file to the given group. If group == None, a new group is
  ###       created.
  ### @retn Returns the group the file was added to, or None if not.
  ################################################################################
  def add_file(self, filename, group = None):
    filename = normalize_filename(filename)
    
    test_group = self.group_from_file(filename)
    if not test_group == None:
      #print "ERROR: File %s already a member of group %d. Try merging groups." % (filename, test_group)
      #print "ERROR: File already a member of group %d. Try merging groups." % (test_group)
      return None
    
    if group == None:
      group = max(self.dupes.keys()) + 1
    
    self.dupes[group].add(filename)
    
    return group

  def remove_file(self, filename):
    filename = normalize_filename(filename)
    
    group = self.group_from_file(filename)
    if group == None:
      #print "ERROR: File %s not in any duplicate group, cannot remove." % filename
      return
    
    # If we have two or fewer and attempt to remove a file,
    # that would leave us with a group with one file, which
    # isn't much of a duplicate group. So just save the trouble
    # and kill it all right here.
    if len(self.dupes[group]) <= 2:
      self.remove_group(group)
    else:
      self.dupes[group].discard(filename)

  def remove_group(self, group):
    if not group in self.dupes:
      #print "ERROR: Cannot remove group %d. Group does not exist." % group
      return
    
    del self.dupes[group]
    
  def merge_groups(self, groups):
    #for group in groups:
      #if not group in self.dupes:
        #print "ERROR: Cannot merge groups. One or more groups does not exist."
        #return
    
    groups = set(groups)
    if len(groups) < 2:
      return
    
    new_group = min(groups)
    groups.remove(new_group)
    
    self.dupes[new_group].update(*[self.dupes[group] for group in groups])
    
    for group in groups:
      del self.dupes[group]

################################################################################
### OLD FUNCTIONS
################################################################################

#def hash_check_group(dir, group):
#  
#  files = get_files_in_group(group)
#  testhash = ""
#  
#  match = True
#  
#  if not files == None:
#    
#    for index, file in enumerate(files):
#      
#      if os.path.isfile(os.path.join(dir, file)):
#        hasher = hashlib.md5()
#        f = open(os.path.join(dir, file), 'rb')
#        
#        data = f.read()
#        hasher.update(data)
#        
#        f.close()
#        
#        if index == 0:
#          testhash = hasher.hexdigest()
#        elif not testhash == hasher.hexdigest():
#          match = False
#          break
#        
#  return match

#def get_most_recently_updated(dir, group):
#  
#  if hash_check_group(dir, group):
#    #print "Group " + str(group) + " does not need updating (hashes)."
#    return None
#  
#  files = get_files_in_group(group)
#  
#  most_recent_time = 0
#  most_recent = None
#  needs_updating = False
#  
#  if not files == None:
#    
#    for index, file in enumerate(files):
#      
#      if os.path.isfile(os.path.join(dir, file)):
#      
#        file_stats = os.stat(os.path.join(dir, file))
#          
#        if index >= 1 and file_stats.st_mtime != most_recent_time:
#          needs_updating = True
#        
#        if file_stats.st_mtime > most_recent_time:
#          most_recent_time = file_stats.st_mtime
#          most_recent = file
#  
#  if not needs_updating:
#    #print "Group " + str(group) + " does not need updating (timestamps)."
#    return None
#  
#  return most_recent

#def list_all_files(dir, subdir = ""):
#  
#  files = []
#  
#  basedir = os.path.join(dir, subdir)
#  
#  for item in os.listdir(basedir):
#    full_path = os.path.join(basedir, item)
#    full_item = os.path.join(subdir, item)
#  
#    if os.path.isfile(full_path):
#      files.append(full_item)
#      
#    else:
#      for file in list_all_files(dir, full_item):
#        files.append(file)
#      
#  return files

#def list_unique_files(dir):
#  
#  groups_seen = {}
#  unique_files = []
#  
#  for key in GROUP_SIZES.keys():
#    groups_seen[key] = False
#  
#  for item in list_all_files(dir):
#    group = get_group_from_file(item)
#    
#    if group == None:
#      unique_files.append(item)
#    elif groups_seen[group] == False:
#      unique_files.append(item)
#      groups_seen[group] = True
#      
#      others_in_group = get_files_in_group(group)
#      
#      for other in others_in_group:
#        if other != item:
#          unique_files.append(" -> " + other)
#  
#  return unique_files

################################################################################
### MAIN
################################################################################

db = DupesDB()

# if __name__ == "__main__":

  # import pprint
  # import time
  # import glob
  # pp = pprint.PrettyPrinter()
  
  # gfx_db = DupesDB("data/dupes-models-pruned.csv")
  
  # for i in xrange(1000):
    # files = gfx_db.files_in_group(i)
    # if files == None:
      # continue
    
    # for file in files:
      # temp = db.group_from_file(file)
      
      # if temp == None:
        # continue
      
      # db.remove_file(file)
    
    # group = None
    # for file in files:
      # group = db.add_file(file, group)
      
      # if group == None:
        # print "Failed to add %s" % file
    
  # db.save_csv()
  
################################################################################
### ALL DONE
################################################################################

### EOF ###