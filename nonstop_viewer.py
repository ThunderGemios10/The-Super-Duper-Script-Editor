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
from PyQt4.QtGui import QImage, QPainter, QColor, QLabel, QMatrix
from PyQt4.QtCore import QRect, QRectF
from ui_nonstop import Ui_Nonstop

import math
import os.path
import re
import sys
import time

import common
from nonstop import *
from text_printer import *

class NonstopViewer(QtGui.QDialog):
  def __init__(self, parent = None):
    super(NonstopViewer, self).__init__(parent)
    
    self.ui = Ui_Nonstop()
    self.ui.setupUi(self)
    self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    
    self.lines = []
  
  def load(self, filename):
    self.nonstop = NonstopParser()
    self.nonstop.load(filename)
    
    if len(self.nonstop.script_pack) == 0:
      return
    
    self.bg = get_trial(self.nonstop.script_pack[0].scene_info, show_box = False, show_sprite = False)
    qt_pixmap = QtGui.QPixmap.fromImage(self.bg)
    self.ui.lblPreview.setPixmap(qt_pixmap)
    
    self.lines = []
    for i in range(len(self.nonstop.lines)):
      if self.nonstop.script_pack[i].translated != "":
        text = self.nonstop.script_pack[i].translated
      else:
        text = self.nonstop.script_pack[i].original
      
      text_img = get_text(text, common.SCENE_MODES.debate)
      
      self.lines.append(text_img)
  
  def play(self):
    
    line = 0
    
    scene_info = self.nonstop.script_pack[line].scene_info
    sprite_id = scene_info.sprite
    sprite_id.sprite_type = SPRITE_TYPE.stand
    sprite = get_sprite(sprite_id)
    
    self.lblSprite = QLabel(self.ui.lblPreview)
    self.lblSprite.setGeometry(0, 0, 480, 272)
    
    qt_pixmap = QtGui.QPixmap.fromImage(sprite)
    self.lblSprite.setPixmap(qt_pixmap)
    
    line = 3
    
    text_img  = self.lines[line]
    line_info = self.nonstop.lines[line]
    
    matrix = QMatrix()
    matrix.rotate(line_info.rot_angle)
    matrix.scale(line_info.zoom_start / 100.0, line_info.zoom_start / 100.0)
    
    text_img = text_img.transformed(matrix, Qt.Qt.SmoothTransformation)
    
    x_start = line_info.x_start - (text_img.width() / 2.0)
    y_start = line_info.y_start - (text_img.height() / 2.0)
    x_vel   = line_info.velocity * math.cos(math.radians(90 - line_info.angle))
    y_vel   = -line_info.velocity * math.sin(math.radians(90 - line_info.angle))
    
    time_visible = line_info.time_visible / 60.0
    
    width_start  = text_img.width()
    height_start = text_img.height()
    width_end    = width_start * ((line_info.zoom_change / 100.0) ** time_visible)
    height_end   = height_start * ((line_info.zoom_change / 100.0) ** time_visible)
    
    x_end = x_start + (x_vel * time_visible)
    y_end = y_start + (y_vel * time_visible)
    #x_end = line_info.x_start + (x_vel * time_visible) - (width_end / 2.0)
    #y_end = line_info.y_start + (y_vel * time_visible) - (height_end / 2.0)
    
    print x_start, y_start, width_start, height_start
    print x_end, y_end, width_end, height_end
    
    self.lblText = QLabel(self.ui.lblPreview)
    self.lblText.setGeometry(x_start, y_start, text_img.width(), text_img.height())
    #self.lblText2 = QLabel(self.ui.lblPreview)
    #self.lblText2.setGeometry(x_end, y_end, text_img.width(), text_img.height())
    
    qt_pixmap = QtGui.QPixmap.fromImage(text_img)
    self.lblText.setPixmap(qt_pixmap)
    #self.lblText2.setPixmap(qt_pixmap)
    
    self.anim = QtCore.QPropertyAnimation(self.lblText, "geometry")
    self.anim.setDuration(time_visible * 1000)
    self.anim.setStartValue(QRectF(x_start, y_start, width_start, height_start))
    self.anim.setEndValue(QRectF(x_end, y_end, width_start, height_start))
    
    self.anim.start()

##############################################################################
### @fn   get_text(text, scene_mode = common.SCENE_MODES.normal)
### @desc Gets an image with the given text.
###       Shamelessly copied from text_printer.py::print_text in a classic
###       case of "too lazy to refactor" (though I did technically try, once).
##############################################################################
def get_text(text, scene_mode = common.SCENE_MODES.normal):
  
  #default_clt = 0
  format = TEXT_FORMAT[scene_mode]
  
  # Replace our unmarked CLTs with whatever default CLT we're given.
  # Also start the line off with the default CLT so we're definitely using it.
  # Useful for modes like Nonstop Debate, where text is normally CLT 16.
  text = "<CLT>" + text
  text = re.sub("<CLT>", "<CLT %d>" % format["clt"], text)
  
  split_text = text.split("\n")
  lines = []
  lengths = []
  clt_changes = []
  last_clt = format["clt"]
  for line in split_text:
    # Start the line off with the last-used CLT, so the parsers know what it is.
    line = ("<CLT %d>" % last_clt) + line
    
    line, length, clt = get_len(line, format["clt"])
    if not 0 in clt:
      clt[0] = last_clt
    if format["killblanks"] and line.strip() == "":
      continue
    lines.append(line)
    lengths.append(length)
    clt_changes.append(clt)
    last_clt = clt[max(clt.keys())]
  
  base_x      = 0
  base_y      = 0
  line_height = format["h"]
  
  # 10.006000042 seconds -> 1000 iterations
  x, y = base_x, base_y
  cur_clt = 0
  cur_font = 1
  cur_hscale = 1.0
  cur_vscale = 1.0
  
  if len(lines) == 0:
    text_height = 0
  else:
    text_height = ((len(lines) - 1) * line_height) + 25
  
  text_width  = 1
  text_expand = 0
  if format["clt"] in CLT_EXPAND:
    text_expand += CLT_EXPAND[format["clt"]][0]
    text_expand += CLT_EXPAND[format["clt"]][1]
  if format["clt"] in CLT_BORDER:
    text_expand += CLT_BORDER[format["clt"]]['size']
    text_expand += CLT_BORDER[format["clt"]]['size']
  for i, line in enumerate(lines):
    # Hack the line up a bit to reflect how it'll show up in-game
    # based on some in-game quirks.
    lines[i], lengths = mangle_line(line, lengths, i, scene_mode, cur_font, format["clt"])
    line_length = sum(lengths[i]) + text_expand
    
    if line_length > text_width:
      text_width = line_length
    
  out = QImage(text_width, text_height, QImage.Format_ARGB32_Premultiplied)
  out.fill(QColor(0, 0, 0, 0).rgba())
  
  painter = QPainter(out)
  painter.setRenderHint(QPainter.Antialiasing, True)
  
  center_x = base_x + (text_width / 2.0)
  right_x  = base_x + text_width
  
  for i in range(len(lines)):
    line = lines[i]
    
    line_length = sum(lengths[i])
    
    if format["a"] == TEXT_ALIGN.left:
      x = base_x
    elif format["a"] == TEXT_ALIGN.right:
      x = right_x - line_length
    elif format["a"] == TEXT_ALIGN.center:
      x = center_x - (line_length / 2.0)
    elif format["a"] == TEXT_ALIGN.offcenter:
      x = center_x - (line_length / 2.0) - 7
      
      # This is hackish as hell, but I want guidelines.
      painter.end()
      stripped_len = line_length
      
      # Strip the widths of any leading and trailing spaces
      for j in range(len(line)):
        if line[j] == ' ' or line[j] == u'　':
          stripped_len -= lengths[i][j]
        else:
          break
      for j in reversed(range(len(line))):
        if line[j] == ' ' or line[j] == u'　':
          stripped_len -= lengths[i][j]
        else:
          break
        
      out = draw_centering_guides(out, center_x, y, stripped_len, 40)
      painter = QPainter(out)
    
    for j in range(len(line)):
      char = line[j]
      
      if j in clt_changes[i]:
        cur_clt = clt_changes[i][j]
      
      letter, (xshift, yshift, final_w, final_h) = get_letter(cur_clt, char)
      
      final_x = (x + xshift)
      final_y = (y + yshift)
      
      painter.drawImage(QRect(final_x, final_y, final_w, final_h), letter, letter.rect())
      
      x += lengths[i][j]
        
    y = y + line_height
  
  painter.end()
  return out

if __name__ == "__main__":
  #test = get_text("<CLT 9>Who the hell do you\nthink you are?!", common.SCENE_MODES.debate, False)
  #test.save("ss/test.png")

  app = QtGui.QApplication(sys.argv)
  app.connect(app, QtCore.SIGNAL("lastWindowClosed()"),
              app,
              QtCore.SLOT("quit()")
             )
  
  form = NonstopViewer()
  form.load("nonstop_03_010.dat")
  form.play()
  form.show()
  sys.exit(app.exec_())

### EOF ###