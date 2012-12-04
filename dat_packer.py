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

from PyQt4 import QtCore, QtGui, Qt
from PyQt4.QtGui import QProgressDialog

import bitstring
from bitstring import BitStream, ConstBitStream
from tempfile import TemporaryFile

import codecs
import os.path
import re
import sys
import time

from enum import Enum

import common
import eboot_text
import text_files

from anagram_file import AnagramFile

PATCH_XMB_LANG   = {'enabled': True,  'pos': 0x1B290, 'data': ConstBitStream(hex = "0x01000424")}
PATCH_XMB_BUTTON = {'enabled': False, 'pos': 0x1B3DC, 'data': ConstBitStream(hex = "0x01000424")}

RE_SCRIPT  = re.compile(ur"(.*?)\0.*", re.UNICODE | re.S)
# UTF-16LE byte-order-marker, since we lose it loading the text
# into Python's unicode format.
SCRIPT_BOM = BitStream(hex = "0xFFFE")
SCRIPT_NULL = BitStream(hex = "0x0000")

SCRIPT_NONSTOP = [
  "e01_102_001.pak",
  "e01_104_001.pak",
  "e01_106_001.pak",
  "e01_110_001.pak",
  "e01_112_001.pak",
  "e01_114_001.pak",
  "e01_116_001.pak",
  "e01_118_001.pak",
  "e02_102_001.pak",
  "e02_104_001.pak",
  "e02_108_001.pak",
  "e02_110_001.pak",
  "e02_112_001.pak",
  "e02_114_001.pak",
  "e02_118_001.pak",
  "e02_120_001.pak",
  "e02_122_001.pak",
  "e03_102_001.pak",
  "e03_106_001.pak",
  "e03_108_001.pak",
  "e03_112_001.pak",
  "e03_114_001.pak",
  "e03_116_001.pak",
  "e03_118_001.pak",
  "e03_120_001.pak",
  "e03_122_001.pak",
  "e03_124_001.pak",
  "e03_126_001.pak",
  "e04_102_001.pak",
  "e04_104_001.pak",
  "e04_106_001.pak",
  "e04_110_001.pak",
  "e04_116_001.pak",
  "e04_118_001.pak",
  "e04_122_001.pak",
  "e04_124_001.pak",
  "e05_102_001.pak",
  "e05_104_001.pak",
  "e05_110_001.pak",
  "e05_114_001.pak",
  "e05_116_001.pak",
  "e05_118_001.pak",
  "e05_120_001.pak",
  "e05_122_001.pak",
  "e05_151_001.pak",
  "e06_102_001.pak",
  "e06_106_001.pak",
  "e06_108_001.pak",
  "e06_110_001.pak",
  "e06_112_001.pak",
  "e06_118_001.pak",
  "e06_120_001.pak",
  "e06_134_001.pak",
  "e06_137_001.pak",
  "e06_143_001.pak",
]

SPECIAL_ALIGN = {
 #'filename' : [toc_align, file_align, inner_toc_align, inner_file_align]
}

class DatPacker():
  def __init__(self, parent = None):
    self.file_count = 0
    
    self.parent = parent

  def create_archives(self):
    
    try:
      self.width = self.parent.width()
      self.height = self.parent.height()
      self.x = self.parent.x()
      self.y = self.parent.y()
    except:
      self.width = 1920
      self.height = 1080
      self.x = 0
      self.y = 0
    
    self.file_count = 0
    
    self.progress = QProgressDialog("Reading...", QtCore.QString(), 0, 72000, self.parent)
    self.progress.setWindowModality(Qt.Qt.WindowModal)
    self.progress.setValue(0)
    self.progress.setAutoClose(False)
    #self.progress.setMinimumDuration(1000)
    
    with open(common.editor_config.eboot_orig, "rb") as f:
      eboot = BitStream(bytes = f.read())
    
    USRDIR = os.path.join(common.editor_config.iso_dir, "PSP_GAME", "USRDIR")
    
    # So we can loop. :)
    ARCHIVE_INFO = [
      {
        "toc":  common.editor_config.toc,
        "dir":  common.editor_config.umdimage_dir,
        "dat":  os.path.join(USRDIR, "umdimage.dat"),
        "name": "umdimage.dat"
      },
      {
        "toc":  common.editor_config.toc2,
        "dir":  common.editor_config.umdimage2_dir,
        "dat":  os.path.join(USRDIR, "umdimage2.dat"),
        "name": "umdimage2.dat"
      },
    ]
    
    for archive in ARCHIVE_INFO:
      
      self.progress.setWindowTitle("Building " + archive["name"])
      
      with open(archive["toc"], "rb") as toc_file:
        toc_text  = toc_file.read()
        toc_lines = toc_text.splitlines()
      
      toc_info = {}
      file_list = []
      
      for line in toc_lines:
        entry = line.split()
        
        if len(entry) >= 3:
          # Stores where the file info is located in the EBOOT, so it can be
          # changed when we get the TOC info later.
          # toc_info[file name] = [position of file pos, position of file size]
          toc_info[entry[0]] = [BitStream(hex = entry[1]), BitStream(hex = entry[2])]
          file_list.append(entry[0])
      
      # Causes memory issues if I use the original order, for whatever reason.
      file_list = None
      
      archive_data, table_of_contents = self.pack_dir(archive["dir"], file_list = file_list)
      
      # We're playing fast and loose with the file count anyway, so why not?
      self.file_count += 1
      self.progress.setValue(self.file_count)
      self.progress.setLabelText("Saving " + archive["name"] + "...")
      
      with open(archive["dat"], "wb") as f:
        archive_data.tofile(f)
      
      for entry in table_of_contents:
        if not entry in toc_info:
          print entry, "missing from", archive["name"], "table of contents."
          continue
        
        file_pos  = table_of_contents[entry]["pos"]
        file_size = table_of_contents[entry]["size"]
        
        eboot.overwrite(BitStream(uintle = file_pos, length = 32),  toc_info[entry][0].uint * 8)
        eboot.overwrite(BitStream(uintle = file_size, length = 32), toc_info[entry][1].uint * 8)
      
      del archive_data
      del table_of_contents
    
    self.progress.setLabelText("Saving EBOOT.BIN...")
    self.progress.setValue(self.progress.maximum())
    
    # Text replacement
    to_replace = eboot_text.get_eboot_text()
    for replacement in to_replace:
      orig = bytearray(replacement.orig, encoding = replacement.enc)
      data = bytearray(replacement.text, encoding = replacement.enc)
      
      padding = len(orig) - len(data)
      if padding > 0:
        # Null bytes to fill the rest of the space the original took.
        data.extend(bytearray(padding))
      
      data = ConstBitStream(bytes = data)
      eboot.overwrite(data, replacement.pos.int * 8)
    
    if PATCH_XMB_LANG['enabled']:
      eboot.overwrite(PATCH_XMB_LANG['data'],   PATCH_XMB_LANG['pos'] * 8)
    if PATCH_XMB_BUTTON['enabled']:
      eboot.overwrite(PATCH_XMB_BUTTON['data'], PATCH_XMB_BUTTON['pos'] * 8)
    
    eboot_out = os.path.join(common.editor_config.iso_dir, "PSP_GAME", "SYSDIR", "EBOOT.BIN")
    
    with open(eboot_out, "wb") as f:
      eboot.tofile(f)
    
    self.progress.close()

  def pack_dir(self, dir, file_list = None, align_toc = 16, align_files = 16):
    
    table_of_contents = {}
    
    if os.path.basename(dir) in SCRIPT_NONSTOP:
      is_nonstop = True
    else:
      is_nonstop = False
    
    if file_list == None:
      file_list = sorted(os.listdir(dir))
      
    num_files    = len(file_list)
    
    toc_length = (num_files + 1) * 4
    if toc_length % align_toc > 0:
      toc_length += align_toc - (toc_length % align_toc)
    
    archive_data = BitStream(uintle = 0, length = toc_length * 8)
    archive_data.overwrite(bitstring.pack("uintle:32", num_files), 0)
    
    for file_num, item in enumerate(file_list):
      full_path = os.path.join(dir, item)
      
      data = BitStream()
    
      if os.path.isfile(full_path):
        
        basename = os.path.basename(item)
        basename, ext = os.path.splitext(basename)
        
        # Special handling for certain data types.
        if ext == ".txt":
          
          text = text_files.load_text(full_path)
          text = RE_SCRIPT.sub(u"\g<1>", text)
          
          # Nonstop Debate lines need an extra newline at the end
          # so they show up in the backlog properly.
          if is_nonstop and not text[-1] == "\n":
            text += "\n"
          
          data = SCRIPT_BOM + BitStream(bytes = bytearray(text, encoding = "UTF-16LE")) + SCRIPT_NULL
        
        # anagram_81.dat is not a valid anagram file. <_>
        elif basename[:8] == "anagram_" and ext == ".dat" and not basename == "anagram_81":
          anagram = AnagramFile(full_path)
          data    = anagram.pack(for_game = True)
        
        else:
          with open(full_path, "rb") as f:
            data = BitStream(bytes = f.read())
      
      else:
      
        temp_align_toc = 16
        temp_align_files = 4
        
        if item in SPECIAL_ALIGN:
          temp_align_toc = SPECIAL_ALIGN[item][0]
          temp_align_files = SPECIAL_ALIGN[item][1]
        elif os.path.basename(dir) in SPECIAL_ALIGN and len(SPECIAL_ALIGN[os.path.basename(dir)]) == 4:
          temp_align_toc = SPECIAL_ALIGN[os.path.basename(dir)][2]
          temp_align_files = SPECIAL_ALIGN[os.path.basename(dir)][3]
        
        data, toc_discard = self.pack_dir(full_path, align_toc = temp_align_toc, align_files = temp_align_files)
        del toc_discard
      
      file_size = data.len / 8
      padding = 0
      
      if file_size % align_files > 0:
        padding = align_files - (file_size % align_files)
        data.append(BitStream(uintle = 0, length = padding * 8))
      
      file_pos = archive_data.len / 8
      archive_data.overwrite(bitstring.pack("uintle:32", file_pos), (file_num + 1) * 32)
      archive_data.append(data)
      
      del data
      
      self.file_count += 1
      if self.file_count % 25 == 0:
        self.progress.setLabelText("Reading...\n" + full_path)
        self.progress.setValue(self.file_count)
        
        # Re-center the dialog.
        progress_w = self.progress.geometry().width()
        progress_h = self.progress.geometry().height()
        
        new_x = self.x + ((self.width - progress_w) / 2)
        new_y = self.y + ((self.height - progress_h) / 2)
        
        self.progress.move(new_x, new_y)
      
      table_of_contents[item] = {}
      table_of_contents[item]["size"] = file_size
      table_of_contents[item]["pos"]  = file_pos
    
    return archive_data, table_of_contents

if __name__ == "__main__":
  import sys
  app = QtGui.QApplication(sys.argv)
  
  packer = DatPacker()
  
  #start = time.time()
  packer.create_archives()
  #print "Took %s seconds to create the archives." % (time.time() - start)

### EOF ###