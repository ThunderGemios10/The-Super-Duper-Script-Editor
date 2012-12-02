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

import os.path
import sys

from list_files import list_all_files
from text_files import load_text

################################################################################
### THE FUNCTIONS
################################################################################
def find_in_dir(directory, to_find):
  
  files = []
  
  for file in list_all_files(directory):
    if os.path.splitext(file)[1] == ".txt":
      if find_in_file(file, to_find):
        files.append(file)
  
  return files

def find_in_file(filename, to_find):
  
  if os.path.isfile(filename):
    text = load_text(filename)
    return to_find.lower() in text.lower()
  
  return False

################################################################################
### MAIN
################################################################################

if __name__ == "__main__":

  input_dir = ""
  to_find = ""

  if len(sys.argv) > 2:
    input_dir = sys.argv[1].decode(sys.stdin.encoding)
    to_find = sys.argv[2].decode(sys.stdin.encoding)
    
  else:
    print "Usage: search.py input_dir to_find"
    exit()
    
  for file in list_all_files(input_dir):
    if find_in_file(file, to_find):
      print file

################################################################################
### ALL DONE
################################################################################

### EOF ###