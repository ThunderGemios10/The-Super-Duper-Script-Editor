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

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QProcess, QString

import os
import re
import shutil

OUTPUT_RE = re.compile(ur"save : ([^\n\r]*)")

class GimConverter():
  def __init__(self, parent = None):
    self.parent = parent
    self.process = QProcess()
  
  def convert(self, gim_file, png_file = None):
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
    
    # And move it to the requested location, if one exists.
    if png_file:
      shutil.move(saved_file, png_file)

if __name__ == "__main__":
  import sys
  app = QtGui.QApplication(sys.argv)
  
  conv = GimConverter()
  conv.convert("X:\\Danganronpa\\Danganronpa_BEST\\umdimage\\adv_map_l_001.gim", "debug/yay.png")
  conv.convert("X:\\Danganronpa\\Danganronpa_BEST\\umdimage\\adv_map_l_001.gim", "debug/yay2.png")
  conv.convert("X:\\Danganronpa\\Danganronpa_BEST\\umdimage\\adv_map_l_001.gim", "debug/yay3.png")
  conv.convert("X:\\Danganronpa\\Danganronpa_BEST\\umdimage\\adv_map_l_001.gim", "debug/yay4.png")

### EOF ###