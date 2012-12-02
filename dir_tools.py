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
import subprocess

def show_in_explorer(directory):
  subprocess.Popen(["explorer", "/select,", directory])

def expand_script_pak(directory):
  
  # If we have a script_pak without the base directory, prepend it.
  if directory[:10] == "script_pak" and directory[14:18] != ".pak":
    directory = os.path.join(directory[:14] + ".pak", directory)
  
  return directory

def expand_lin(directory):
  
  basename = os.path.basename(directory)
  
  if basename[-4:] == ".lin":
    directory = os.path.join(directory, basename[:-4] + ".pak")
  
  return directory

def expand_dir(directory):
  return expand_lin(expand_script_pak(directory))

def parse_dir(directory, umdimage = "umdimage"):
  
  base_name = os.path.splitext(os.path.basename(directory))[0]
  
  # Only expands if necessary.
  directory = expand_script_pak(directory)
  
  full_dir = os.path.join(umdimage, directory)
  if not os.path.isdir(full_dir):
    return None, None
  
  wrd_file = "!" + base_name + ".scp.wrd"
  wrd_file = os.path.join(full_dir, wrd_file)
  
  if os.path.isfile(wrd_file):
    directory = os.path.join(directory, base_name + ".pak")
  else:
    wrd_file = None
  
  return directory, wrd_file

### EOF ###