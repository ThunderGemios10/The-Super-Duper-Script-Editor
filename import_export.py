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

# from PyQt4 import QtGui, QtCore
# from PyQt4.QtCore import QProcess, QString

import glob
import logging
import os
import re
import shutil
import tempfile

# from bitstring import ConstBitStream

import common

from backup import backup_files
from dupe_db import DupesDB
from enum import Enum
from list_files import list_all_files
from gim_converter import GimConverter, QuantizeType
from model_pak import ModelPak

_CONV     = GimConverter()
_DUPE_DB  = DupesDB()

DIR_TYPE  = Enum("umdimage", "umdimage2")

SKIP_CONV = ["save_icon0.png", "save_icon0_t.png", "save_new_icon0.png", "save_pic1.png"]

FORCE_QUANTIZE = [
  (re.compile(ur"art_chip_002_\d\d\d.*", re.UNICODE),                         QuantizeType.index8),
  (re.compile(ur"bgd_\d\d\d.*", re.UNICODE),                                  QuantizeType.index8),
  (re.compile(ur"bustup_\d\d_\d\d.*", re.UNICODE),                            QuantizeType.index8),
  (re.compile(ur"(cutin|gallery|kotodama|present)_icn_\d\d\d.*", re.UNICODE), QuantizeType.index8),
]

# MODEL_PAK = re.compile(ur"bg_\d\d\d")

_LOGGER_NAME = common.LOGGER_NAME + "." + __name__
_LOGGER = logging.getLogger(_LOGGER_NAME)

################################################################################
### FUNCTIONS
################################################################################

######################################################################
### Importing
######################################################################
def import_dir(src, dst, dir_type, convert_png = True, propogate = True):
  if dir_type == DIR_TYPE.umdimage:
    import_umdimage(src, dst, convert_png, propogate)
  elif dir_type == DIR_TYPE.umdimage2:
    import_umdimage2(src, dst, convert_png, propogate)
  else:
    _LOGGER.error("Unable to import %s. Unknown dirtype %s provided." % (src, dir_type))

def import_umdimage(src, dst, convert_png = True, propogate = True):
  pass

def import_umdimage2(src, dst, convert_png = True, propogate = True):
  tmp_dst     = tempfile.mkdtemp(prefix = "sdse-")
  backup_dir  = None
  
  for pak_dir in glob.iglob(os.path.join(src, "bg_*.pak")):
    for image in list_all_files(pak_dir):
      ext = os.path.splitext(image)[1].lower()
      if ext == ".png" and not convert_png:
        continue
      
      base_name = image[len(src) + 1:]
      dst_files = []
      
      if propogate:
        dupe_name = os.path.splitext(base_name)[0] + ".gim"
        dupe_name = os.path.join("umdimage2", dupe_name)
        dupe_name = os.path.normpath(os.path.normcase(dupe_name))
      
        dupes = _DUPE_DB.files_in_same_group(dupe_name)
        
        if dupes == None:
          dupes = [dupe_name]
        
        for dupe in dupes:
          dst_file = dupe[10:] # chop off the "umdimage2/"
          dst_file = os.path.splitext(dst_file)[0] + ext # original extension
          dst_file = os.path.join(tmp_dst, dst_file)
          dst_files.append(dst_file)
      
      else:
        dst_files = [os.path.join(tmp_dst, base_name)]
      
      for dst_file in dst_files:
        try:
          os.makedirs(os.path.dirname(dst_file))
        except:
          pass
        shutil.copy(image, dst_file)
    
    pak_name    = os.path.basename(pak_dir)
    backup_dir  = backup_files(dst, [pak_name], suffix = "_IMPORT", backup_dir = backup_dir)
    
    insert_textures(os.path.join(tmp_dst, pak_name), os.path.join(dst, pak_name))
  
  shutil.rmtree(tmp_dst)

######################################################################
### Exporting
######################################################################
def export_dir(src, dst, dir_type, convert_gim = True, unique = False):
  if dir_type == DIR_TYPE.umdimage:
    export_umdimage(src, dst, convert_gim, unique)
  elif dir_type == DIR_TYPE.umdimage2:
    export_umdimage2(src, dst, convert_gim, unique)
  else:
    _LOGGER.error("Unable to export %s. Unknown dirtype %s provided." % (src, dir_type))

def export_umdimage(src, dst, convert_gim = True, unique = False):
  seen_groups = []
  
  for filename in list_all_files(src):
    base_name = filename[len(src) + 1:]
    
    if unique:
      dupe_name = os.path.join("umdimage", base_name)
      dupe_name = os.path.normpath(os.path.normcase(dupe_name))
      
      group = _DUPE_DB.group_from_file(dupe_name)
      
      if group in seen_groups:
        continue
      
      if not group == None:
        seen_groups.append(group)
    
    dst_file = os.path.join(dst, base_name)
    dst_dir  = os.path.dirname(dst_file)
    ext      = os.path.splitext(dst_file)[1].lower()
    
    try:
      os.makedirs(dst_dir)
    except:
      pass
    
    if ext == ".gim" and convert_gim:
      dst_file = os.path.splitext(dst_file)[0] + ".png"
      _CONV.gim_to_png(filename, dst_file)
    else:
      shutil.copy(filename, dst_file)

def export_umdimage2(src, dst, convert_gim = True, unique = False):
  if unique:
    tmp_dst = tempfile.mkdtemp(prefix = "sdse-")
  else:
    tmp_dst = dst
  
  seen_groups = []
  
  for pak in glob.iglob(os.path.join(src, "bg_*.pak")):
    out_dir = extract_model_pak(pak, tmp_dst, convert_gim)
  
    if unique:
      for img in list_all_files(out_dir):
        img_base  = img[len(tmp_dst) + 1:]
        dupe_name = os.path.splitext(img_base)[0] + ".gim"
        dupe_name = os.path.join("umdimage2", dupe_name)
        dupe_name = os.path.normpath(os.path.normcase(dupe_name))
        # print dupe_name
        
        group = _DUPE_DB.group_from_file(dupe_name)
        
        if group in seen_groups:
          continue
        
        if not group == None:
          seen_groups.append(group)
        
        dst_file = os.path.join(dst, img_base)
        dst_dir  = os.path.dirname(dst_file)
        
        try:
          os.makedirs(dst_dir)
        except:
          pass
        
        shutil.copy(img, dst_file)
      
      shutil.rmtree(out_dir)
    _LOGGER.info("Exported %s to %s" % (pak, dst))
  
  if unique:
    shutil.rmtree(tmp_dst)

######################################################################
### Models/textures
######################################################################
def extract_model_pak(filename, dst_dir, to_png = True):
  # out_dir = os.path.splitext(os.path.basename(filename))[0]
  out_dir = os.path.basename(filename)
  out_dir = os.path.join(dst_dir, out_dir)
  
  pak = ModelPak(filename = filename)
  pak.extract(out_dir, to_png)
  
  return out_dir

def insert_textures(pak_dir, filename):
  
  pak = ModelPak(filename = filename)
  
  for gmo_name in os.listdir(pak_dir):
    full_path = os.path.join(pak_dir, gmo_name)
    if not os.path.isdir(full_path):
      _LOGGER.warning("Not a directory of textures. Skipped importing %s to %s" % (full_path, filename))
      continue
  
    gmo_id = pak.id_from_name(gmo_name)
    if gmo_id == None:
      _LOGGER.warning("GMO %s does not exist in %s" % (gmo_name, filename))
      continue
    
    gmo = pak.get_gmo(gmo_id)
    if gmo == None:
      _LOGGER.warning("Failed to retrieve GMO %s from %s" % (gmo_name, filename))
      continue
    
    for img in os.listdir(os.path.join(pak_dir, gmo_name)):
      name, ext = os.path.splitext(img)
      
      if ext.lower() == ".gim":
        is_png = False
      elif ext.lower() == ".png":
        is_png = True
      else:
        _LOGGER.warning("Did not insert %s into %s" % (img, gmo_name))
        continue
      
      gim_id = int(name)
      if is_png:
        gmo.replace_png_file(gim_id, os.path.join(pak_dir, gmo_name, img))
      else:
        gmo.replace_gim_file(gim_id, os.path.join(pak_dir, gmo_name, img))
      
      _LOGGER.info("Inserted %s into %s" % (img, gmo_name))
    
    pak.replace_gmo(gmo_id, gmo)
    _LOGGER.info("Inserted %s into %s" % (gmo_name, filename))
  
  pak.save(filename)
  _LOGGER.info("Saved %s" % filename)

if __name__ == "__main__":
  import sys
  handler = logging.StreamHandler(sys.stdout)
  logging.getLogger(common.LOGGER_NAME).addHandler(handler)
  
  # export_umdimage2("Y:/Danganronpa/Danganronpa_BEST/umdimage2", "wip/umdimage3", convert_gim = True, unique = True)
  # export_umdimage("Y:/Danganronpa/Danganronpa_BEST/umdimage", "wip/umdimage", convert_gim = True, unique = True)
  # import_umdimage2("Y:/Danganronpa/Danganronpa_BEST/image-editing/umdimage2-edited-png", "wip/umdimage2-orig")
  import_umdimage2("wip/umdimage2-edited-png", "wip/umdimage2-orig")
  # export_umdimage2("wip/umdimage2-orig", "wip/umdimage2-test", convert_gim = True, unique = False)
  
  # extract_model_pak("wip/test/bg_042.pak", "wip/test")
  # import_model_pak("wip/test/bg_042-eng", "wip/test/bg_042.pak")
  # extract_model_pak("wip/test/bg_042.pak", "wip/test")

### EOF ###