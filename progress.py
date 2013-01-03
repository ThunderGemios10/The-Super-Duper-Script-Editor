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

from PyQt4 import QtCore, QtGui, Qt
from PyQt4.QtGui import QProgressDialog

import os
import re
import time

import common
import dupe_db
import list_files
import script_file
import script_analytics
from script_file import ScriptFile
from word_count import count_words

def script_for_counting(data):

  # A little faster than using the ScriptFile's built-in
  # parser because we don't need as much of the data.
  file = ScriptFile()
  
  data = script_file.TAG_KILLER.sub("", data)
  data = script_file.LINE_BREAKS.sub("\n", data)
  match = script_file.TEXT_PARSER.search(data)
  
  if match:
    first_part = match.group(1)
    second_part = match.group(2)
    
    if not second_part:
      file.original_notags = first_part
    else:
      file.translated_notags = first_part
      file.original_notags = second_part
  
  return file

def calculate_progress(parent, filter = script_analytics.DEFAULT_FILTER):
  start_time = time.time()
  progress = QProgressDialog("Calculating translation progress...", "Abort", 0, 72000, parent)
  progress.setWindowTitle("Translation Progress")
  progress.setWindowModality(Qt.Qt.WindowModal)
  progress.setValue(0)
  progress.setAutoClose(False)
  
  # For our dupe database, we need "umdimage" instead of wherever the files
  # are really stored, so we strip that part off first.
  dir_start = len(common.editor_config.umdimage_dir) + 1
  
  total_files = 0
  unique_files = 0
  translated_files = 0
  translated_unique = 0
  
  total_chars = 0
  unique_chars = 0
  translated_chars = 0
  translated_unique_chars = 0
  
  translated_words = 0
  translated_unique_words = 0
  
  total_bytes = 0
  unique_bytes = 0
  translated_bytes = 0
  translated_unique_bytes = 0
  
  groups_seen = set()
  files_seen = set()
  
  untranslated_lines = []
  
  for i, total, filename, data in script_analytics.SA.get_data(filter):
    if progress.wasCanceled():
      return
    
    progress.setValue(i)
    progress.setMaximum(total)
    
    if data == None:
      continue
    
    db_name   = os.path.join("umdimage", filename)
    real_name = os.path.join(common.editor_config.umdimage_dir, filename)
    
    if db_name in files_seen:
      continue
    
    dupe_group = dupe_db.db.group_from_file(db_name)
    
    # Add the whole group to the translated files, but only one
    # to the unique translated. If there is no group, it's size 1.
    group_size = 1
    
    if not dupe_group == None:
      if dupe_group in groups_seen:
        continue
      else:
        groups_seen.add(dupe_group)
        group_files = dupe_db.db.files_in_group(dupe_group)
        group_size = 0
        for dupe_file in group_files:
          #if filter.search(dupe_file):
            group_size += 1
        files_seen.update(group_files)
    
    total_files += group_size
    unique_files += 1
    
    #file = script_for_counting(data)
    file = data
    
    # How many characters is the untranslated, non-tagged text?
    num_chars = len(file.original_notags)
    #num_bytes = len(bytearray(file.original_notags, encoding = "SJIS", errors = "replace"))
    
    total_chars  += num_chars * group_size
    unique_chars += num_chars
    
    #total_bytes  += num_bytes * group_size
    #unique_bytes += num_bytes
    
    if not file.translated_notags == "" or num_chars == 0:
      translated_files  += group_size
      translated_unique += 1
      
      translated_chars        += num_chars * group_size
      translated_unique_chars += num_chars
      
      words = count_words(file.translated_notags)
      translated_words        += words * group_size
      translated_unique_words += words
      
      #translated_bytes        += num_bytes * group_size
      #translated_unique_bytes += num_bytes
    
    #elif file.translated_notags == "":
      #untranslated_lines.append(db_name)
  
  progress.close()
  #print "Took %s seconds." % (time.time() - start_time)
  
  files_percent         = 100.0 if total_files == 0  else float(translated_files) / total_files * 100
  unique_files_percent  = 100.0 if unique_files == 0 else float(translated_unique) / unique_files * 100
  chars_percent         = 100.0 if total_chars == 0  else float(translated_chars) / total_chars * 100
  unique_chars_percent  = 100.0 if unique_chars == 0 else float(translated_unique_chars) / unique_chars * 100
  bytes_percent         = 100.0 if total_bytes == 0  else float(translated_bytes) / total_bytes * 100
  unique_bytes_percent  = 100.0 if unique_bytes == 0 else float(translated_unique_bytes) / unique_bytes * 100
  
  QtGui.QMessageBox.information(
    parent,
    "Translation Progress",
    ("Files: %d / %d (%0.2f%%)\n" % (translated_files, total_files, files_percent)) + 
    ("Unique Files: %d / %d (%0.2f%%)\n" % (translated_unique, unique_files, unique_files_percent)) +
    "\n" +
    ("Japanese Characters: %d / %d (%0.2f%%)\n" % (translated_chars, total_chars, chars_percent)) + 
    ("Unique Characters: %d / %d (%0.2f%%)\n" % (translated_unique_chars, unique_chars, unique_chars_percent)) +
    #"\n" +
    #("Bytes: %d / %d (%0.2f%%)\n" % (translated_bytes, total_bytes, bytes_percent)) + 
    #("Unique Bytes: %d / %d (%0.2f%%)\n" % (translated_unique_bytes, unique_bytes, unique_bytes_percent)) +
    "\n" +
    ("English Words: %d\n" % (translated_words)) + 
    ("Unique Words: %d\n" % (translated_unique_words)) +
    "\n" +
    "NOTE: Unique X is lazy for \"X in all unique files\"\n" +
    "and not what it seems to imply." +
    "",
    buttons = QtGui.QMessageBox.Ok,
    defaultButton = QtGui.QMessageBox.Ok
  )

def list_untranslated():
  
  files = list_files.list_all_files(common.editor_config.umdimage_dir)
  #files = list_files.list_all_files("X:\\Danganronpa\\FULL_TEST\\best-normal")
  
  text_files = []
  
  for i, file in enumerate(files):
    if os.path.splitext(file)[1] == ".txt":
      text_files.append(file)
  
  for file in text_files:
    try:
      script_file = ScriptFile(file, mecab = False)
    except:
      print file
      continue
    
    if not script_file.translated == "":
      print file

if __name__ == "__main__":
  import sys
  app = QtGui.QApplication(sys.argv)
  
  folder_re = ".*"
  
  if len(sys.argv) > 1:
    folder_re = sys.argv[1].decode(sys.stdin.encoding)
  
  calculate_progress(None, re.compile(folder_re))

### EOF ###