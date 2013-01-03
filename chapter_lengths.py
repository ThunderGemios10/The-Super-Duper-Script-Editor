################################################################################
### Copyright © 2012-2013 BlackDragonHunt
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

import os
import re

import common
import dupe_db
import list_files

from progress import script_for_counting

CHAPTER_RE = [
  ("Prologue",  re.compile(ur"e00_\d\d\d_\d\d\d\.lin|script_pak_e00.pak", re.IGNORECASE | re.DOTALL | re.UNICODE)),
  ("Chapter 1", re.compile(ur"e01_\d\d\d_\d\d\d\.lin|script_pak_e01.pak", re.IGNORECASE | re.DOTALL | re.UNICODE)),
  ("Chapter 2", re.compile(ur"e02_\d\d\d_\d\d\d\.lin|script_pak_e02.pak", re.IGNORECASE | re.DOTALL | re.UNICODE)),
  ("Chapter 3", re.compile(ur"e03_\d\d\d_\d\d\d\.lin|script_pak_e03.pak", re.IGNORECASE | re.DOTALL | re.UNICODE)),
  ("Chapter 4", re.compile(ur"e04_\d\d\d_\d\d\d\.lin|script_pak_e04.pak", re.IGNORECASE | re.DOTALL | re.UNICODE)),
  ("Chapter 5", re.compile(ur"e05_\d\d\d_\d\d\d\.lin|script_pak_e05.pak", re.IGNORECASE | re.DOTALL | re.UNICODE)),
  ("Chapter 6", re.compile(ur"e06_\d\d\d_\d\d\d\.lin|script_pak_e06.pak", re.IGNORECASE | re.DOTALL | re.UNICODE)),
  ("Epilogue",  re.compile(ur"e07_\d\d\d_\d\d\d\.lin|script_pak_e07.pak", re.IGNORECASE | re.DOTALL | re.UNICODE)),
  ("Free Time", re.compile(ur"e08_0(0[1-9]|1[0-9])_\d\d\d\.lin", re.IGNORECASE | re.DOTALL | re.UNICODE)),
 #("Monokuma",  re.compile(ur"e08_000_\d\d\d\.lin", re.IGNORECASE | re.DOTALL | re.UNICODE)),
  ("Other",     re.compile(ur".*", re.IGNORECASE | re.DOTALL | re.UNICODE)),
]

def list_lengths():
  
  groups_seen = []
  
  num_lines = {}
  num_chars = {}
  
  for i, total, filename, data in script_analytics.SA.get_data():
    
    if i % 500 == 0:
      print i
    
    if data == None:
      continue
    
    #db_name   = os.path.join("umdimage", filename)
    #real_name = os.path.join(common.editor_config.umdimage_dir, filename)
    #
    #dupe_group = dupe_db.db.group_from_file(db_name)
    #
    #if not dupe_group == None:
    #  if dupe_group in groups_seen:
    #    continue
    #  else:
    #    groups_seen.append(dupe_group)
    
    #file = script_for_counting(data)
    #
    # How many characters is the untranslated, non-tagged text?
    #char_count = len(file.original_notags)
    #char_count = 0
    char_count = len(data.original_notags)
    
    for chapter in CHAPTER_RE:
      ch_name = chapter[0]
      ch_re   = chapter[1]
      
      if ch_re.search(filename):
        try:
          num_lines[ch_name] += 1
        except:
          num_lines[ch_name] = 1
          
        try:
          num_chars[ch_name] += char_count
        except:
          num_chars[ch_name] = char_count
        break
  
  return num_lines, num_chars

if __name__ == "__main__":
  num_lines, num_chars = list_lengths()
  
  for chapter in sorted(num_lines.keys()):
    print "%s: %d lines, %d chars" % (chapter, num_lines[chapter], num_chars[chapter])

### EOF ###