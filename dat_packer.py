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

import bitstring
from bitstring import BitStream, ConstBitStream
from tempfile import TemporaryFile

import codecs
import logging
import os.path
import re
import shutil
import sys
import tempfile
import time
import traceback

from enum import Enum

import common
import eboot_text
import eboot_patch
import text_files

from extract.eboot import get_toc, UMDIMAGES

from anagram_file import AnagramFile
from list_files import list_all_files
from wrd.wrd_file import WrdFile

_LOGGER_NAME = common.LOGGER_NAME + "." + __name__
_LOGGER = logging.getLogger(_LOGGER_NAME)

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
    self.progress.setMinimumDuration(0)
    
    # with open(common.editor_config.eboot_orig, "rb") as f:
    with open(os.path.join(common.editor_config.iso_dir, "PSP_GAME", "SYSDIR", "EBOOT.BIN"), "rb") as f:
      eboot = BitStream(bytes = f.read())
    
    eboot, eboot_offset = eboot_patch.apply_eboot_patches(eboot)
    
    USRDIR = os.path.join(common.editor_config.iso_dir, "PSP_GAME", "USRDIR")
    
    # So we can loop. :)
    ARCHIVE_INFO = [
      {
        "toc":  UMDIMAGES.umdimage,
        "dir":  common.editor_config.umdimage_dir,
        "dat":  os.path.join(USRDIR, "umdimage.dat"),
        "name": "umdimage.dat",
        "pack": common.editor_config.pack_umdimage,
        "eof":  False,
      },
      {
        "toc":  UMDIMAGES.umdimage2,
        "dir":  common.editor_config.umdimage2_dir,
        "dat":  os.path.join(USRDIR, "umdimage2.dat"),
        "name": "umdimage2.dat",
        "pack": common.editor_config.pack_umdimage2,
        "eof":  False,
      },
      {
        "toc":  None,
        "dir":  common.editor_config.voice_dir,
        "dat":  os.path.join(USRDIR, "voice.pak"),
        "name": "voice.pak",
        "pack": common.editor_config.pack_voice,
        "eof":  True,
      },
      {
        "toc":  None,
        "dir":  common.editor_config.bgm_dir,
        "dat":  os.path.join(USRDIR, "bgm.pak"),
        "name": "bgm.pak",
        "pack": common.editor_config.pack_bgm,
        "eof":  True,
      },
    ]
    
    for archive in ARCHIVE_INFO:
      
      if not archive["pack"]:
        continue
      
      self.progress.setWindowTitle("Building " + archive["name"])
      
      toc_info = {}
      file_list = None
      
      if archive["toc"]:
        file_list = []
        
        toc = get_toc(eboot, archive["toc"])
        
        for entry in toc:
          filename  = entry["filename"]
          pos_pos   = entry["file_pos_pos"]
          len_pos   = entry["file_len_pos"]
          
          toc_info[filename] = [pos_pos, len_pos]
          file_list.append(filename)
      
      # Causes memory issues if I use the original order, for whatever reason.
      file_list = None
      
      archive_data, table_of_contents = self.pack_dir(archive["dir"], file_list = file_list, eof = archive["eof"])
      
      # We're playing fast and loose with the file count anyway, so why not?
      self.file_count += 1
      self.progress.setValue(self.file_count)
      self.progress.setLabelText("Saving " + archive["name"] + "...")
      
      with open(archive["dat"], "wb") as f:
        archive_data.tofile(f)
      
      if archive["toc"]:
        for entry in table_of_contents:
          if not entry in toc_info:
            _LOGGER.warning("%s missing from %s table of contents." % (entry, archive["name"]))
            continue
          
          file_pos  = table_of_contents[entry]["pos"]
          file_size = table_of_contents[entry]["size"]
          
          eboot.overwrite(BitStream(uintle = file_pos, length = 32),  toc_info[entry][0] * 8)
          eboot.overwrite(BitStream(uintle = file_size, length = 32), toc_info[entry][1] * 8)
      
      del archive_data
      del table_of_contents
    
    self.progress.setLabelText("Saving EBOOT.BIN...")
    self.progress.setValue(self.progress.maximum())
    
    # Text replacement
    to_replace = eboot_text.get_eboot_text()
    for replacement in to_replace:
    
      orig = bytearray(replacement.orig, encoding = replacement.enc)
      
      # If they left something blank, write the original text back.
      if len(replacement.text) == 0:
        data = orig
      else:
        data = bytearray(replacement.text, encoding = replacement.enc)
      
      pos  = replacement.pos.int + eboot_offset
      
      padding = len(orig) - len(data)
      if padding > 0:
        # Null bytes to fill the rest of the space the original took.
        data.extend(bytearray(padding))
      
      data = ConstBitStream(bytes = data)
      eboot.overwrite(data, pos * 8)
    
    eboot_out = os.path.join(common.editor_config.iso_dir, "PSP_GAME", "SYSDIR", "EBOOT.BIN")
    
    with open(eboot_out, "wb") as f:
      eboot.tofile(f)
    
    self.progress.close()

  def pack_dir(self, dir, file_list = None, align_toc = 16, align_files = 16, eof = False):
    
    table_of_contents = {}
    
    if file_list == None:
      file_list = sorted(os.listdir(dir))
      
    num_files    = len(file_list)
    
    toc_length = (num_files + 1) * 4
    
    if eof:
      toc_length += 1
    
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
          
          data = self.pack_txt(full_path)
        
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
        
        if os.path.splitext(full_path)[1].lower() == ".lin":
          data = self.pack_lin(full_path)
        
        else:
          data, toc_discard = self.pack_dir(full_path, align_toc = temp_align_toc, align_files = temp_align_files, eof = eof)
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
    
    if eof:
      archive_data.overwrite(bitstring.pack("uintle:32", archive_data.len / 8), (num_files + 1) * 32)
    
    return archive_data, table_of_contents
  
  def pack_txt(self, filename):
    
    if os.path.basename(os.path.dirname(filename)) in SCRIPT_NONSTOP:
      is_nonstop = True
    else:
      is_nonstop = False
  
    text = text_files.load_text(filename)
    text = RE_SCRIPT.sub(u"\g<1>", text)
    
    # Nonstop Debate lines need an extra newline at the end
    # so they show up in the backlog properly.
    if is_nonstop and not text[-1] == "\n":
      text += "\n"
    
    return SCRIPT_BOM + BitStream(bytes = bytearray(text, encoding = "UTF-16LE")) + SCRIPT_NULL
    
  def pack_lin(self, dir):
    
    # Collect our files.
    file_list = sorted(list_all_files(dir))
    
    txt = [filename for filename in file_list if os.path.splitext(filename)[1].lower() == ".txt"]
    wrd = [filename for filename in file_list if os.path.splitext(filename)[1].lower() == ".wrd"]
    py  = [filename for filename in file_list if os.path.splitext(filename)[1].lower() == ".py"]
    
    # If there are more than one for whatever reason, just take the first.
    # We only have use for a single wrd or python file.
    wrd = wrd[0] if wrd else None
    py  = py[0]  if py  else None
    
    # Prepare our temporary output directory.
    temp_dir = tempfile.mkdtemp(prefix = "sdse-")
    
    # Where we're outputting our wrd file, regardless of whether it's a python
    # file or a raw binary data file.
    wrd_dst = os.path.join(temp_dir, "0.scp.wrd")
    
    if py:
      # _LOGGER.info("Compiling %s to binary." % py)
      try:
        wrd_file = WrdFile(py)
      except:
        _LOGGER.warning("%s failed to compile. Parsing wrd file instead. Exception info:\n%s" % (py, traceback.format_exc()))
        shutil.copy(wrd, wrd_dst)
      else:
        # If we succeeded in loading the python file, compile it to binary.
        # wrd_file.save_bin(wrd)
        wrd_file.save_bin(wrd_dst)
    
    else:
      shutil.copy(wrd, wrd_dst)
    
    # Pack the text files in-place to save us a bunch of copying
    # and then move it to the tmp directory with the wrd file.
    if txt:
      data, temp_toc = self.pack_dir(dir, file_list = txt)
      with open(os.path.join(temp_dir, "1.dat"), "wb") as f:
        data.tofile(f)
    
    # Then pack it like normal.
    data, temp_toc = self.pack_dir(temp_dir)
    shutil.rmtree(temp_dir)
    
    return data

if __name__ == "__main__":
  import sys
  app = QtGui.QApplication(sys.argv)
  
  packer = DatPacker()
  
  #start = time.time()
  packer.create_archives()
  #print "Took %s seconds to create the archives." % (time.time() - start)

### EOF ###