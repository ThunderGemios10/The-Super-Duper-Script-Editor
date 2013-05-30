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

from bitstring import ConstBitStream

import os
import re

from .eboot import get_toc
from .pak_ex import get_pak_files, get_txt_files, get_script_pak_files, get_lin_files, EXT_MODE
from .invalidarchiveexception import InvalidArchiveException

EXTRACT_EXT = [".pak", ".lin"]
SKIP_EXTRACT_FILE_RE = re.compile(ur"hs_mtb_s\d\d|bg_\d\d\d|bg_lc01")
FILE_NORECURSIVE_RE  = re.compile(ur"effect_lensflare00")

SPECIAL_FILE_EXTRACT = [
  (re.compile(ur"^e?\d\d_.*?.pak$"),              get_txt_files),
  (re.compile(ur"^(event|mtb_s\d\d|voice).pak$"), get_txt_files),
  (re.compile(ur"^script_pak_.*?\.pak$"),         get_script_pak_files),
  (re.compile(ur"\.lin$"),                        get_lin_files),
  (re.compile(ur"\.pak$"),                        get_pak_files),
]

############################################################
### FUNCTIONS
############################################################

##################################################
### 
##################################################
def dump_to_file(data, filename):
  dirname = os.path.dirname(filename)
  try:
    os.makedirs(dirname)
  except: pass
  
  with open(filename, "wb") as out_file:
    data.tofile(out_file)

##################################################
### 
##################################################
def extract_umdimage(filename, eboot, umdimage, out_dir = None):
  if out_dir == None:
    out_dir = filename + "-out"
  
  data        = ConstBitStream(filename = filename)
  eboot_data  = ConstBitStream(filename = eboot)
  
  toc = get_toc(eboot_data, umdimage)
  
  for filename, file_data in get_pak_files(data, recursive = True, toc = toc):
    out_path = os.path.join(out_dir, filename)
    
    final_dir = os.path.dirname(out_path)
    try:
      os.makedirs(final_dir)
    except: pass
    
    name, ext = os.path.splitext(filename)
    ext = ext.lower()
    
    print filename
    
    if ext in EXTRACT_EXT and SKIP_EXTRACT_FILE_RE.search(filename) == None:
      try:
        extract_fn = get_pak_files
        file_ext = None
        ext_mode = EXT_MODE.auto
        recursive = True
        
        if FILE_NORECURSIVE_RE.search(filename):
          recursive = False
        
        for special in SPECIAL_FILE_EXTRACT:
          if special[0].search(filename):
            extract_fn = special[1]
            break
        
        # Hacky stupid thing to handle how I handled lin files in the old QuickBMS script.
        if extract_fn == get_lin_files or extract_fn == get_script_pak_files:
          lin_name = os.path.basename(out_path)
          lin_name = os.path.splitext(lin_name)[0]
          for sub_filename, sub_data in extract_fn(file_data, recursive, file_ext, ext_mode, lin_name = lin_name):
            dump_to_file(sub_data, os.path.join(out_path, sub_filename))
        else:
          for sub_filename, sub_data in extract_fn(file_data, recursive, file_ext, ext_mode):
            dump_to_file(sub_data, os.path.join(out_path, sub_filename))
        
      except InvalidArchiveException:
        dump_to_file(file_data, out_path)
    
    else:
      dump_to_file(file_data, out_path)
  
##################################################
### 
##################################################
# if __name__ == "__main__":
  # extract_umdimage("full-umdimage.dat",  eboot = "full-EBOOT.BIN", type = UMDIMAGE_TYPE.full,  out_dir = "full-umdimage",  toc_filename = "!full-toc.txt")
  # extract_umdimage("full-umdimage2.dat", eboot = "full-EBOOT.BIN", type = UMDIMAGE_TYPE.full2, out_dir = "full-umdimage2", toc_filename = "!full-toc2.txt")
  # extract_umdimage("best-umdimage.dat",  eboot = "best-EBOOT.BIN", type = UMDIMAGE_TYPE.best,  out_dir = "best-umdimage",  toc_filename = "!best-toc.txt")
  # extract_umdimage("best-umdimage2.dat", eboot = "best-EBOOT.BIN", type = UMDIMAGE_TYPE.best2, out_dir = "best-umdimage2", toc_filename = "!best-toc2.txt")

### EOF ###