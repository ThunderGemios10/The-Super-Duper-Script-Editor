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

import sys
from text_files import load_text
from make_unique import make_unique

FONTS = Enum("font01", "font02")
GAMES = Enum("dr", "sdr2")
FONT_TO_GEN = FONTS.font02
GAME_TO_GEN = GAMES.sdr2

HEIGHT_ADJUST = 0
WIDTH_ADJUST  = 0
X_OFFSET      = 0
Y_OFFSET      = 0
X_MARGIN      = 2
Y_MARGIN      = 1
LINE_HEIGHT   = 25

UNKNOWN1      = BitStream(hex = '0x2D000000')
UNKNOWN2      = BitStream(hex = '0x01000000')

# The 0xFA has to do with vertical alignment.
# 0xFA = -6 = shift down six pixels when rendering.
# Not sure about the 0x08 though.
UNKNOWN3      = BitStream(hex = '0x00000000FA08')

if FONT_TO_GEN == FONTS.font01:
  CHAR_LIST = "data/font1_chars.txt"
  SAVE_AS   = "font_gen/Font01"
  FONT_NAME = "Meiryo"
  FONT_ALT  = "Meiryo UI"
  ALT_CHARS = u'【】「」『』'
  FONT_SIZE = 11
  FONT_WEIGHT = 50
  PEN_WIDTH = 0.25
  IMG_WIDTH = 1024
  IMG_HEIGHT = 1024 + 512
  
  CHAR_SUBS = {
    u"…":  u"...",
    u"\t": u'  ',
  }
  
  if GAME_TO_GEN == GAMES.dr:
    HEIGHT_ADJUST = 2
    WIDTH_ADJUST  = 0
    X_OFFSET      = 0
    Y_OFFSET      = 2
    #X_MARGIN      = 2
    #Y_MARGIN      = 1
  
  elif GAME_TO_GEN == GAMES.sdr2:
    HEIGHT_ADJUST = -4
    WIDTH_ADJUST  = 0
    X_OFFSET      = 0
    Y_OFFSET      = -1
    X_MARGIN      = 2
    Y_MARGIN      = 3
    UNKNOWN1      = BitStream(hex = '0x24000000')
    # Render two pixels higher.
    UNKNOWN3      = BitStream(hex = '0x000000000200')

elif FONT_TO_GEN == FONTS.font02:
  CHAR_LIST = "data/font2_chars.txt"
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
    HEIGHT_ADJUST = 2
    WIDTH_ADJUST  = 0
    X_OFFSET      = 0
    Y_OFFSET      = 2
    #X_MARGIN      = 2
    #Y_MARGIN      = 1
    UNKNOWN1      = BitStream(hex = '0x30000000')
    
  elif GAME_TO_GEN == GAMES.sdr2:
    HEIGHT_ADJUST = 2
    WIDTH_ADJUST  = 0
    X_OFFSET      = 0
    Y_OFFSET      = 0
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
      char = BitStream(bytes = bytearray(entry['char'], encoding = 'utf-16le'))
      x_pos = BitStream(uintle = entry['x'], length = 16)
      y_pos = BitStream(uintle = entry['y'], length = 16)
      width = BitStream(uintle = entry['w'], length = 16)
      height = BitStream(uintle = entry['h'], length = 16)
      
      font_table += char + x_pos + y_pos + width + height + padding
    
    return font_table

class GameFont:
  def __init__(self):
    self.trans  = QImage(IMG_WIDTH, IMG_HEIGHT, QImage.Format_ARGB32_Premultiplied)
    self.trans.fill(QColor(0, 0, 0, 0).rgba())
    
    self.opaque = QImage(IMG_WIDTH, IMG_HEIGHT, QImage.Format_ARGB32_Premultiplied)
    self.opaque.fill(QColor(0, 0, 0, 255).rgba())
    
    self.font_data = FontData()
  
  def save(self, basename):
    self.trans.save(basename + ".png")
    
    opaque_gray = self.to_gray(self.opaque)
    opaque_gray.save(basename + ".bmp")
    
    self.font_data.save(basename + ".font")
  
  def to_gray(self, image):
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

def gen_font(text):
  font = QFont(FONT_NAME, FONT_SIZE, FONT_WEIGHT)
  font.setKerning(False)
  #font.setLetterSpacing(QFont.AbsoluteSpacing, WIDTH_ADJUST)
  
  font_alt = QFont(FONT_ALT, FONT_SIZE, FONT_WEIGHT)
  font_alt.setKerning(False)
  
  metric = QFontMetrics(font)
  metric_alt = QFontMetrics(font_alt)
  
  LINE_HEIGHT = metric.height() + HEIGHT_ADJUST #abs(HEIGHT_ADJUST)
  
  game_font = GameFont()
  
  painter = QPainter(game_font.trans)
  painter.setFont(font)
  painter.setRenderHint(QPainter.TextAntialiasing, True)
  painter.setRenderHint(QPainter.Antialiasing, True)
  
  pen = painter.pen()
  pen.setColor(QColor(255, 255, 255, 255))
  pen.setWidthF(PEN_WIDTH)
  pen.setCapStyle(Qt.Qt.RoundCap)
  pen.setJoinStyle(Qt.Qt.RoundJoin)
  painter.setPen(pen)
  
  brush = QtGui.QBrush(QColor(255, 255, 255, 255))
  painter.setBrush(brush)
  
  x_pos = 0
  #y_pos = HEIGHT_ADJUST
  y_pos = 0
  
  using_alt = False
  
  for char in text:
    
    if char in ALT_CHARS:
      using_alt = True
    
    if using_alt:
      cur_font = font_alt
      cur_metric = metric_alt
    else:
      cur_font = font
      cur_metric = metric
    
    # If we want a character to represent something it's not.
    # Basically just for … = ... because in Meiryo, … is mid-aligned.
    char_to_print = char
    
    if char in CHAR_SUBS:
      char_to_print = CHAR_SUBS[char]
      
    char_w = cur_metric.width(char_to_print) + WIDTH_ADJUST
    
    if x_pos + char_w > IMG_WIDTH:
      x_pos = 0
      y_pos += LINE_HEIGHT + Y_MARGIN
    
    if y_pos < 0:
      y_pos = 0
    
    if y_pos + LINE_HEIGHT > IMG_HEIGHT:
      print "Ran out of vertical space. Generated font does not include all characters."
      break
    
    game_font.font_data.data.append({'char': char, 'x': x_pos, 'y': y_pos, 'w': char_w, 'h': LINE_HEIGHT})
    #painter.drawText(QtCore.QRectF(x_pos, y_pos + HEIGHT_ADJUST, char_w, LINE_HEIGHT), Qt.Qt.AlignCenter, char)
    
    path = QPainterPath()
    path.addText(x_pos + X_OFFSET, y_pos + cur_metric.ascent() + Y_OFFSET, cur_font, char_to_print)
    painter.drawPath(path)
    
    x_pos += char_w + X_MARGIN
    
    using_alt = False
  
  painter.end()
  
  painter = QPainter(game_font.opaque)
  painter.drawImage(game_font.opaque.rect(), game_font.trans, game_font.trans.rect())
  
  return game_font

if __name__ == '__main__':
  
  app = QtGui.QApplication(sys.argv)
  
  chars = load_text(CHAR_LIST)
  # We can't have dupes, and why not put them in order while we're at it?
  chars = sorted(make_unique(chars))
  
  game_font = gen_font(chars)
  game_font.save(SAVE_AS)

### EOF ###