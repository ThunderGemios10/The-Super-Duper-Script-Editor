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
from PyQt4.QtGui import QFont, QFontMetrics, QImage, QPainter, QPainterPath, QColor

from bitstring import BitStream
from enum import Enum

import math
import sys
from text_files import load_text
from make_unique import make_unique

FONTS = Enum("font01", "font02")
GAMES = Enum("dr", "sdr2")
FONT_TO_GEN = FONTS.font01
GAME_TO_GEN = GAMES.dr

X_SHIFT       = 0
Y_SHIFT       = 0
X_MARGIN      = 2
Y_MARGIN      = 1
LINE_HEIGHT   = 25
MAX_HEIGHT    = 4096

UNKNOWN1      = BitStream(hex = '0x2D000000')
UNKNOWN2      = BitStream(hex = '0x01000000')

# The 0xFA has to do with vertical alignment.
# 0xFA = -6 = shift down six pixels when rendering.
# Not sure about the 0x08 though.
UNKNOWN3      = BitStream(hex = '0x00000000FA08')

if FONT_TO_GEN == FONTS.font01:
  CHAR_LIST = "data/font1-dr1.txt"
  SAVE_AS   = "font_gen/Font01"
  FONT_NAME = "Meiryo"
  FONT_ALT  = "Meiryo UI"
  ALT_CHARS = u'【】「」『』'
  FONT_SIZE = 11
  FONT_WEIGHT = 50
  PEN_WIDTH = 0.25
  IMG_WIDTH = 512
  IMG_HEIGHT = 2048
  
  CHAR_SUBS = {
    u"…":  u"...",
    u"\t": u'  ',
  }
  
  if GAME_TO_GEN == GAMES.dr:
    X_SHIFT       = 0
    Y_SHIFT       = 2
    #X_MARGIN      = 2
    #Y_MARGIN      = 1
  
  elif GAME_TO_GEN == GAMES.sdr2:
    X_SHIFT       = 0
    Y_SHIFT       = -1
    X_MARGIN      = 2
    Y_MARGIN      = 3
    UNKNOWN1      = BitStream(hex = '0x24000000')
    # Render two pixels higher.
    UNKNOWN3      = BitStream(hex = '0x000000000200')

elif FONT_TO_GEN == FONTS.font02:
  CHAR_LIST = "data/font2.txt"
  SAVE_AS   = "font_gen/Font02"
  FONT_NAME = "DFSoGei-W7"
  FONT_ALT  = "DFGSoGei-W7"
  ALT_CHARS = u' ",.\'!:;()-―-‒–—|“”‘’【】「」『』Ifijl'
  FONT_SIZE = 18
  FONT_WEIGHT = 50
  PEN_WIDTH = 0.001
  IMG_WIDTH = 1024
  IMG_HEIGHT = 1024
  
  CHAR_SUBS = {
    u"\t": u'  ',
  }
  
  if GAME_TO_GEN == GAMES.dr:
    X_SHIFT       = 0
    Y_SHIFT       = 2
    #X_MARGIN      = 2
    #Y_MARGIN      = 1
    UNKNOWN1      = BitStream(hex = '0x30000000')
    
  elif GAME_TO_GEN == GAMES.sdr2:
    X_SHIFT       = 0
    Y_SHIFT       = 0
    X_MARGIN      = 2
    #Y_MARGIN      = 1
    UNKNOWN3      = BitStream(hex = '0x00000000FD00')

class FontData:
  def __init__(self):
    self.data = []
  
  def save(self, filename):
    data = BitStream(hex = '0x7446705304000000') # Magic
    
    data += BitStream(uintle = len(self.data), length = 32)
    
    mapping_table_len = self.find_max_char() + 1 # zero-indexed so +1 for the size.
    mapping_table_start = 0x20
    font_table_start = mapping_table_len * 2 + mapping_table_start
    
    data += BitStream(uintle = font_table_start, length = 32)
    data += BitStream(uintle = mapping_table_len, length = 32)
    data += BitStream(uintle = mapping_table_start, length = 32)
    data += UNKNOWN1 + UNKNOWN2
    
    data += self.gen_mapping_table(mapping_table_len)
    
    data += self.gen_font_table()
    
    padding = BitStream(hex = '0x00') * (16 - ((data.len / 8) % 16))
    
    data += padding
    
    f = open(filename, "wb")
    data.tofile(f)
    f.close()
  
  # Returns the character with the highest hex value in UTF16
  def find_max_char(self):
    
    max_char = BitStream(hex = '0x0000')
    
    for entry in self.data:
      char = BitStream(bytes = bytearray(entry['char'], encoding = 'utf-16le'))
      
      if char.uintle > max_char.uintle:
        max_char = char
    
    return max_char.uintle
  
  def gen_mapping_table(self, num_entries):
    mapping_table = BitStream(hex = '0xFFFF') * num_entries
    
    for i, entry in enumerate(self.data):
      char = BitStream(bytes = bytearray(entry['char'], encoding = 'utf-16le'))
      
      entry_pos = char.uintle * 2 * 8 # Bytes -> Bits
      
      mapping_table[entry_pos : entry_pos + 16] = BitStream(uintle = i, length = 16)
    
    return mapping_table
  
  def gen_font_table(self):
    font_table = BitStream()
    
    padding = UNKNOWN3
    
    for entry in self.data:
      char    = BitStream(bytes = bytearray(entry['char'], encoding = 'utf-16le'))
      x_pos   = BitStream(uintle = entry['x'], length = 16)
      y_pos   = BitStream(uintle = entry['y'], length = 16)
      width   = BitStream(uintle = entry['w'], length = 16)
      height  = BitStream(uintle = entry['h'], length = 16)
      
      font_table += char + x_pos + y_pos + width + height + padding
    
    return font_table

class GameFont:
  def __init__(self, width = 512):
    self.trans  = QImage(width, MAX_HEIGHT, QImage.Format_ARGB32_Premultiplied)
    self.trans.fill(QColor(0, 0, 0, 0).rgba())
    
    self.opaque = QImage(width, MAX_HEIGHT, QImage.Format_ARGB32_Premultiplied)
    self.opaque.fill(QColor(0, 0, 0, 255).rgba())
    
    self.font_data = FontData()
  
  def save(self, basename):
    self.trans.save(basename + ".png")
    
    opaque_gray = to_gray(self.opaque)
    opaque_gray.save(basename + ".bmp")
    
    self.font_data.save(basename + ".font")

class FontConfig:
  def __init__(self, family = "Meiryo", size = 11, weight = 50,
      x_offset = 0, y_offset = 2, x_margin = 2, y_margin = 2,
      y_shift = -1, chars = "", subs = {u"\t": u'  '}):
    
    self.family   = family
    self.size     = size
    self.weight   = weight
    self.x_offset = x_offset
    self.y_offset = y_offset
    self.x_margin = x_margin
    self.y_margin = y_margin
    self.y_shift  = y_shift
    
    self.chars    = chars
    self.subs     = subs
  
def to_gray(image):
  out = QImage(image.width(), image.height(), QImage.Format_Indexed8)
  color_table = []
  
  for i in range(256):
    color_table.append(QtGui.qRgb(i, i, i))
  
  out.setColorTable(color_table)
  
  for i in range(image.width()):
    for j in range(image.height()):
      color = image.pixel(i, j)
      out.setPixel(i, j, QtGui.qGray(color))
  
  return out

def gen_font(font_configs, img_width = 1024, draw_outlines = False):
  height_factor = 512
  img_height    = height_factor
  
  seen_chars = []
  
  game_font = GameFont()
  painter = QPainter(game_font.trans)
  
  text_brush = QtGui.QBrush(QColor(255, 255, 255, 255))
  painter.setBrush(text_brush)
  
  outline_brush = QtGui.QBrush()
  outline_pen   = QtGui.QPen(QColor(255, 0, 0, 255), 1, style = Qt.Qt.DotLine, join = Qt.Qt.MiterJoin)
  
  x_pos = 0
  y_pos = 0
  
  for config in font_configs:
    font = QFont(config.family, config.size, config.weight, italic = False)
    font.setKerning(False)
    metric = QFontMetrics(font)
    
    painter.setFont(font)
    painter.setRenderHint(QPainter.TextAntialiasing, True)
    painter.setRenderHint(QPainter.Antialiasing, True)
    
    text_pen = painter.pen()
    text_pen.setBrush(QColor(255, 255, 255, 255))
    text_pen.setWidthF(0)
    text_pen.setCapStyle(Qt.Qt.RoundCap)
    text_pen.setJoinStyle(Qt.Qt.RoundJoin)
    text_pen.setStyle(Qt.Qt.NoPen)
    painter.setPen(text_pen)
    
    for char in config.chars:
      
      if char in seen_chars:
        continue
      else:
        seen_chars.append(char)
      
      # If we want a character to represent something it's not.
      # Basically just for … = ... because in Meiryo, … is mid-aligned.
      char_to_print = char
      
      if char in config.subs:
        char_to_print = config.subs[char]
      
      char_w = metric.width(char_to_print)
      
      if x_pos + char_w > img_width:
        x_pos = 0
        y_pos += LINE_HEIGHT + config.y_margin
      
      if y_pos < 0:
        y_pos = 0
    
      if y_pos + LINE_HEIGHT > MAX_HEIGHT:
        print "Ran out of vertical space. Generated font does not include all characters."
        break
    
      game_font.font_data.data.append({'char': char, 'x': x_pos, 'y': y_pos, 'w': char_w, 'h': LINE_HEIGHT, 'y_shift': config.y_shift})
      
      path = QPainterPath()
      path.addText(x_pos + config.x_offset, y_pos + metric.ascent() + config.y_offset, font, char_to_print)
      painter.drawPath(path)
      
      if draw_outlines:
        painter.setBrush(outline_brush)
        painter.setPen(outline_pen)
        painter.setRenderHint(QPainter.Antialiasing, False)
        
        painter.drawRect(x_pos, y_pos, char_w, LINE_HEIGHT)
        
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setBrush(text_brush)
        painter.setPen(text_pen)
      
      x_pos += char_w + config.x_margin
  
  painter.end()
  
  painter = QPainter(game_font.opaque)
  painter.drawImage(game_font.opaque.rect(), game_font.trans, game_font.trans.rect())
  painter.end()
  
  # Crop our images so they only take up as much space as they need.
  final_height = int(math.ceil(float(y_pos + LINE_HEIGHT) / float(height_factor)) * height_factor)
  game_font.trans   = game_font.trans.copy(0, 0, img_width, final_height)
  game_font.opaque  = game_font.opaque.copy(0, 0, img_width, final_height)
  
  return game_font

# if __name__ == '__main__':
  
  # app = QtGui.QApplication(sys.argv)
  
  # chars = load_text(CHAR_LIST)
  # We can't have dupes, and why not put them in order while we're at it?
  # chars = sorted(make_unique(chars))
  
  # game_font = gen_font(chars)
  # game_font.save(SAVE_AS)

### EOF ###