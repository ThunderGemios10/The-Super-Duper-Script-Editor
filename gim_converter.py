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

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QProcess, QString

import os
import re
import shutil
import tempfile

from bitstring import ConstBitStream
from enum import Enum

QuantizeType = Enum("none", "auto", "index4", "index8")

OUTPUT_RE = re.compile(ur"save : ([^\n\r]*)")

class GimConverter:
  def __init__(self, parent = None):
    self.parent = parent
    self.process = QProcess()
    self.temp_dir = tempfile.mkdtemp(prefix = "sdse-")
  
  def __del__(self):
    shutil.rmtree(self.temp_dir)
  
  def quantize_png(self, png_file, quant_type = QuantizeType.auto):
    
    if quant_type == QuantizeType.none:
      return png_file
    
    basename = os.path.basename(png_file)
    temp_png = os.path.join(self.temp_dir, basename)
    
    shutil.copy(png_file, temp_png)
    
    options = ["--force", "--ext", ".png", "--speed", "1"]
    
    if quant_type == QuantizeType.auto:
      options.extend(["--quality", "100"])
    elif quant_type == QuantizeType.index4:
      options.append("16")
    elif quant_type == QuantizeType.index8:
      options.append("256")
    
    options.append(temp_png)
      
    self.process.start("tools/pngquant", options)
    self.process.waitForFinished(-1)
    
    return temp_png
  
  def png_to_gim(self, png_file, gim_file = None, quant_type = QuantizeType.auto):
    # So there's no confusion.
    png_file = os.path.abspath(png_file)
    
    if gim_file == None:
      gim_file = os.path.splitext(png_file)[0] + ".gim"
    
    png_file = self.quantize_png(png_file, quant_type)
    
    data = ConstBitStream(filename = png_file)
    data.bytepos = 0x18
    
    options = ["-jar", "tools/gimexport.jar", png_file, gim_file, "3"]
    
    depth      = data.read("int:8")
    color_type = data.read("int:8")
    
    if color_type == 3: # Indexed
      options.append("true")
    else:
      options.append("false")
    
    self.process.start("java", options)
    self.process.waitForFinished(-1)
  
  def gim_to_png(self, gim_file, png_file = None, quant_type = QuantizeType.none):
    # So there's no confusion.
    gim_file = os.path.abspath(gim_file)
    if png_file:
      png_file = os.path.abspath(png_file)
    
    # Convert our GIM.
    self.process.start("tools/gim2png", ["-9", gim_file])
    self.process.waitForFinished(-1)
    
    # Now get the output location.
    output = QString(self.process.readAllStandardOutput())
    output = output.split("\n", QString.SkipEmptyParts)
    
    saved_file = None
    
    for line in output:
      line = unicode(line.toUtf8(), "utf-8")
      
      match = OUTPUT_RE.match(line)
      
      if match == None:
        continue
      
      saved_file = match.group(1)
      break
    
    # Make sure we actually generated a file.
    if not saved_file:
      print "Error generating PNG file."
      return
    
    quant = self.quantize_png(saved_file, quant_type)
    
    if not quant == saved_file and not quant == png_file:
      os.remove(saved_file)
    
    # And move it to the requested location, if one exists.
    if png_file:
      shutil.move(quant, png_file)
    else:
      shutil.move(quant, saved_file)

if __name__ == "__main__":
  import sys
  app = QtGui.QApplication(sys.argv)
  
  conv = GimConverter()
  conv.gim_to_png("X:\\Danganronpa\\Danganronpa_BEST\\umdimage-img\\fla_735.pak\\0001.gim", "debug/yay.png")
  # conv.gim_to_png("X:\\Danganronpa\\Danganronpa_BEST\\umdimage-img\\fla_735.pak\\0001.gim", "debug/yay2.png", QuantizeType.auto)
  # conv.gim_to_png("X:\\Danganronpa\\Danganronpa_BEST\\umdimage-img\\fla_735.pak\\0001.gim", "debug/yay3.png", QuantizeType.index8)
  # conv.gim_to_png("X:\\Danganronpa\\Danganronpa_BEST\\umdimage-img\\fla_735.pak\\0001.gim", "debug/yay4.png", QuantizeType.index4)
  # conv.gim_to_png("X:\\Danganronpa\\Danganronpa_BEST\\umdimage\\adv_map_l_001.gim", "debug/yay2.png")
  # conv.gim_to_png("X:\\Danganronpa\\Danganronpa_BEST\\umdimage\\adv_map_l_001.gim", "debug/yay3.png")
  # conv.gim_to_png("X:\\Danganronpa\\Danganronpa_BEST\\umdimage\\adv_map_l_001.gim", "debug/yay4.png")
  
  # conv.png_to_gim("debug/yay.png", "debug/yay.gim")
  # conv.png_to_gim("debug/yay.png", "debug/yay2.gim", QuantizeType.index8)
  # conv.png_to_gim("debug/yay.png", "debug/yay3.gim", QuantizeType.index4)

### EOF ###