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

import time
import os
import shutil

import common
from list_files import list_all_files

DIR_FORMAT = "%Y.%m.%d_%H.%M.%S"

def backup_dir(source_dir, suffix = "_SAVE"):
  files = [file[len(source_dir) + 1:] for file in list_all_files(source_dir)]
  backup_files(source_dir, files, suffix)

# def backup_file(file, suffix = "_SAVE"):
  # backup_files([file], suffix)

def backup_files(source_dir, files, suffix = "_SAVE"):
  
  backup_time = time.strftime(DIR_FORMAT + suffix)
  backup_dir = os.path.join(common.editor_config.backup_dir, backup_time)
  
  # umdimage  = common.editor_config.umdimage_dir
  # umdimage2 = common.editor_config.umdimage2_dir
  # source_dirs = [umdimage, umdimage2]
  
  # clean_files = []
  # Strip our source directories out of the paths.
  # for i, file in enumerate(files):
    # file = os.path.normpath(os.path.normcase(file))
    
    # for source in source_dirs:
      # source = os.path.normpath(os.path.normcase(source))
      # if source in file.lower():
        # file = file[len(source) + 1:]
        # break
  
    # clean_files.append(file)
  
  for file in files:
    src = os.path.join(source_dir, file)
    dst = os.path.join(backup_dir, file)
    
    try:
      os.makedirs(os.path.dirname(dst))
    except: pass
    
    shutil.copy(src, dst)

if __name__ == "__main__":
  # backup_files(
    # [
      # "X:/Danganronpa/Danganronpa_BEST/umdimage/e01_038_156.lin/!e01_038_156.scp.py",
      # "X:/Danganronpa/Danganronpa_BEST/umdimage/e01_038_156.lin/!e01_038_156.scp.wrd",
    # ],
    # suffix = "_TEST"
  # )
  backup_dir("X:/Danganronpa/Danganronpa_BEST/umdimage/e01_038_156.lin", suffix = "_TEST")

### EOF ###