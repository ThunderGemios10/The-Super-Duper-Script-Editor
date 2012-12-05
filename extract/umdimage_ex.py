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

from bitstring import ConstBitStream
from enum import Enum

import os
import re

from pak_ex import get_pak_files, get_txt_files, get_script_pak_files, get_lin_files, EXT_MODE
from invalidarchiveexception import InvalidArchiveException
from unique_postfix import add_unique_postfix

UMDIMAGE_TYPE = Enum("demo", "full", "full2", "best", "best2")

TOC_INFO = {
  UMDIMAGE_TYPE.demo:  {"start": 0x00145C24, "count": 0x00145C1C, "name_offset": 0xC0},
  UMDIMAGE_TYPE.full:  {"start": 0x000F8248, "count": 0x000F8240, "name_offset": 0xC0},
  UMDIMAGE_TYPE.full2: {"start": 0x00103C5C, "count": 0x00103C54, "name_offset": 0xC0},
  UMDIMAGE_TYPE.best:  {"start": 0x000F5A18, "count": 0x00100EB4, "name_offset": 0xA0},
  UMDIMAGE_TYPE.best2: {"start": 0x000F5200, "count": 0x000F5A10, "name_offset": 0xA0},
}

EXTRACT_EXT = [".pak", ".lin"]
SKIP_EXTRACT_FILE_RE = re.compile(ur"hs_mtb_s\d\d|bg_\d\d\d|bg_lc01")
FILE_NORECURSIVE_RE  = re.compile(ur"effect_lensflare00")

SPECIAL_FILE_EXTRACT = [
  (re.compile(ur"e?\d\d_.*?.pak$"),               get_txt_files),
  (re.compile(ur"^(event|mtb_s\d\d|voice).pak$"), get_txt_files),
  (re.compile(ur"script_pak_.*?\.pak$"),          get_script_pak_files),
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
def extract_umdimage(filename, out_dir = None, eboot = "EBOOT.BIN", type = UMDIMAGE_TYPE.best, toc_filename = "!toc.txt"):
  if out_dir == None:
    out_dir = filename + "-out"
  
  data       = ConstBitStream(filename = filename)
  eboot_data = ConstBitStream(filename = eboot)
  
  toc_start     = TOC_INFO[type]["start"]
  toc_count_pos = TOC_INFO[type]["count"]
  toc_name_off  = TOC_INFO[type]["name_offset"]
  
  eboot_data.bytepos = toc_count_pos
  toc_count = eboot_data.read("uintle:32")
  
  eboot_data.bytepos = toc_start
  
  toc = []
  file_starts = []
  filenames   = []
  
  toc_file = open(toc_filename, "wb")
  
  for i in xrange(toc_count):
    name_pos = eboot_data.read("uintle:32")
    
    file_pos_pos  = eboot_data.bytepos
    file_pos      = eboot_data.read("uintle:32")
    file_len_pos  = eboot_data.bytepos
    file_len      = eboot_data.read("uintle:32")
    
    name_pos += toc_name_off
    
    temp_pos = eboot_data.bytepos
    eboot_data.bytepos = name_pos
    
    filename = eboot_data.readto("0x00", bytealigned = True).bytes
    # Strip the null character.
    filename = filename[:-1]
    
    # Ensure the filenames don't conflict.
    filename = add_unique_postfix(filename, check_fn = (lambda fn: fn in filenames))
    filenames.append(filename)
    
    eboot_data.bytepos = temp_pos
    
    entry = {
      "filename":     filename,
      "file_pos_pos": file_pos_pos,
      "file_pos":     file_pos,
      "file_len_pos": file_len_pos,
      "file_len":     file_len,
    }
    
    toc.append(entry)
    
    toc_file.write("%s 0x%08X 0x%08X\n" % (filename, file_pos_pos, file_len_pos))
  
  toc_file.close()
  
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