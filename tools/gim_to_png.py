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
    # self.process.finished.connect(self.__build_finished)
    # self.process.setReadChannel(QProcess.StandardError)
    # self.process.readyRead.connect(self.__parse_output)
  
  def convert(self, gim_file, png_file):
    # So there's no confusion.
    gim_file = os.path.abspath(gim_file)
    png_file = os.path.abspath(png_file)
    
    # Convert our GIM.
    self.process.start("gim2png", ["-9", gim_file])
    self.process.waitForFinished(-1)
    
    # Now get the output location.
    output = QString(self.process.readAllStandardOutput())
    output = output.split("\n", QString.SkipEmptyParts)
    
    out_file = None
    
    for line in output:
      line = unicode(line.toUtf8(), "utf-8")
      
      match = OUTPUT_RE.match(line)
      
      if match == None:
        continue
      
      out_file = match.group(1)
      break
    
    # And move it to the requested location.
    if out_file:
      shutil.move(out_file, png_file)
    else:
      print "Error generating PNG file."

if __name__ == "__main__":
  import sys
  app = QtGui.QApplication(sys.argv)
  
  conv = GimConverter()
  conv.convert("adv_map_l_001.gim", "yay.png")
  conv.convert("adv_map_l_001.gim", "yay2.png")
  conv.convert("adv_map_l_001.gim", "yay3.png")
  conv.convert("adv_map_l_001.gim", "yay4.png")

### EOF ###