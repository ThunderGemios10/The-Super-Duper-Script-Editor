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
from PyQt4.QtGui import QImage, QPainter, QColor, QPixmap, QBitmap, QMatrix
from PyQt4.QtCore import QRect, QRectF

from enum import Enum
import ctypes
import os.path
import re
import sys
import time

import common

import font_parser
from font_parser import FONT_DATA, CLT
#from gfx import filters # Crashes on exit for whatever reason.
from text_files import load_text
from sprite import get_sprite_file, SPRITE_TYPE

################################################################################
### VARIABLES
################################################################################
IMG_W           = 480
IMG_H           = 272

# BASE_DIR        = os.path.dirname(os.path.abspath(__file__))

# GFX_DIR         = os.path.join(BASE_DIR, "data/gfx")
GFX_DIR         = common.editor_config.gfx_dir
AMMO_DIR        = os.path.join(GFX_DIR, "ammo")
ANAGRAM_DIR     = os.path.join(GFX_DIR, "anagram")
BG_DIR          = os.path.join(GFX_DIR, "bg")
BGD_DIR         = os.path.join(GFX_DIR, "bgd")
CUTIN_DIR       = os.path.join(GFX_DIR, "cutin")
EVENT_DIR       = os.path.join(GFX_DIR, "events")
FLASH_DIR       = os.path.join(GFX_DIR, "flash")
FONT_FOLDER     = os.path.join(GFX_DIR, "font")
MENU_DIR        = os.path.join(GFX_DIR, "menu")
MOVIEFRAME_DIR  = os.path.join(GFX_DIR, "movieframes") # Full-sized background frames
MOVIE_DIR       = os.path.join(GFX_DIR, "movies") # Icons for the movie gallery
NAMETAG_DIR     = os.path.join(GFX_DIR, "nametags")
PRESENT_DIR     = os.path.join(GFX_DIR, "presents")
SPRITE_DIR      = os.path.join(GFX_DIR, "sprites")
TEXTBOX_DIR     = os.path.join(GFX_DIR, "textbox")
TRIAL_DIR       = os.path.join(GFX_DIR, "trial")

TEXT_ALIGN   = Enum("left", "right", "center", "offcenter")
#TEXT_V_ALIGN = Enum("normal", "nonstop")
IMG_FILTERS  = Enum("unfiltered", "sepia", "inverted")

#SCENE_MODES = Enum("normal", "trial", "rules", "ammo", "ammoname", "present", "presentname", "debate", "mtb", "climax", "anagram", "menu", "map", "report", "report2", "skill", "skill2", "music", "eventname", "moviename", "theatre", "help", "other")
TEXT_FORMAT = {
  common.SCENE_MODES.normal:      {"x":  18, "y": 202, "w": 444, "h": 24, "a": TEXT_ALIGN.left,   "clt":  0, "killblanks": True},
  common.SCENE_MODES.trial:       {"x":  18, "y": 202, "w": 444, "h": 24, "a": TEXT_ALIGN.left,   "clt":  0, "killblanks": True},
  common.SCENE_MODES.rules:       {"x":  32, "y": 159, "w": 416, "h": 18, "a": TEXT_ALIGN.center, "clt":  0, "killblanks": True},
  common.SCENE_MODES.ammo:        {"x": 247, "y":  72, "w": 185, "h": 14, "a": TEXT_ALIGN.left,   "clt":  7, "killblanks": False},
  common.SCENE_MODES.ammoname:    {"x":  32, "y": 199, "w": 200, "h": 14, "a": TEXT_ALIGN.center, "clt":  7, "killblanks": True},
  common.SCENE_MODES.ammosummary: {"x":  41, "y": 192, "w": 200, "h": 12, "a": TEXT_ALIGN.left,   "clt":  7, "killblanks": False},
  common.SCENE_MODES.present:     {"x": 247, "y":  72, "w": 185, "h": 14, "a": TEXT_ALIGN.left,   "clt":  7, "killblanks": False},
  common.SCENE_MODES.presentname: {"x":  32, "y": 199, "w": 200, "h": 14, "a": TEXT_ALIGN.center, "clt":  7, "killblanks": True},
  common.SCENE_MODES.debate:      {"x":  18, "y": 160, "w": 444, "h": 24, "a": TEXT_ALIGN.center, "clt":  8, "killblanks": True},
  common.SCENE_MODES.mtb:         {"x":  18, "y": 160, "w": 444, "h": 24, "a": TEXT_ALIGN.center, "clt": 12, "killblanks": True},
  common.SCENE_MODES.climax:      {"x":  18, "y": 202, "w": 420, "h": 24, "a": TEXT_ALIGN.left,   "clt":  0, "killblanks": True},
  common.SCENE_MODES.anagram:     {"x":  18, "y": 202, "w": 420, "h": 24, "a": TEXT_ALIGN.left,   "clt":  8, "killblanks": True},
  common.SCENE_MODES.menu:        {"x":  55, "y": 198, "w": 370, "h": 14, "a": TEXT_ALIGN.left,   "clt":  7, "killblanks": True},
  common.SCENE_MODES.map:         {"x":  38, "y":  59, "w": 200, "h": 14, "a": TEXT_ALIGN.center, "clt":  7, "killblanks": True},
  common.SCENE_MODES.report:      {"x": 170, "y":  84, "w": 292, "h": 14, "a": TEXT_ALIGN.left,   "clt":  6, "killblanks": True},
  common.SCENE_MODES.report2:     {"x": 182, "y": 181, "w": 292, "h": 14, "a": TEXT_ALIGN.left,   "clt":  6, "killblanks": True},
  common.SCENE_MODES.skill:       {"x":  18, "y": 100, "w": 292, "h": 14, "a": TEXT_ALIGN.left,   "clt":  6, "killblanks": False},
  common.SCENE_MODES.skill2:      {"x": 248, "y": 148, "w": 292, "h": 14, "a": TEXT_ALIGN.left,   "clt":  6, "killblanks": True},
  common.SCENE_MODES.music:       {"x": 173, "y":  78, "w": 180, "h": 14, "a": TEXT_ALIGN.left,   "clt":  6, "killblanks": True},
  common.SCENE_MODES.eventname:   {"x": 262, "y":  85, "w": 196, "h": 14, "a": TEXT_ALIGN.left,   "clt":  6, "killblanks": True},
  common.SCENE_MODES.moviename:   {"x": 262, "y":  85, "w": 196, "h": 14, "a": TEXT_ALIGN.left,   "clt":  6, "killblanks": True},
  common.SCENE_MODES.theatre:     {"x":  18, "y": 202, "w": 420, "h": 24, "a": TEXT_ALIGN.left,   "clt":  0, "killblanks": True},
  common.SCENE_MODES.help:        {"x":  18, "y":  18, "w": 420, "h": 14, "a": TEXT_ALIGN.left,   "clt":  6, "killblanks": False},
  common.SCENE_MODES.other:       {"x":  18, "y":  18, "w": 420, "h": 14, "a": TEXT_ALIGN.left,   "clt":  6, "killblanks": False},
  common.SCENE_SPECIAL.option:    {"x": 227, "y":  85, "w": 254, "h": 25, "a": TEXT_ALIGN.left,   "clt":  0, "killblanks": True},
}

# Just some arbitrary tuning to make things look a little closer to the original.
CLT_EXPAND = {
  # 5: (1, 1, 1, 1),
  # 8: (1, 0, -3, 0),
  #12: (1, 1, 2, 0),
  #17: (1, 1, -3, -3),
}

CLT_INSIDE = {
 # 0: {'color': QColor(0, 0, 0, 255)},
 # 1: {'color': QColor(0, 0, 0, 255)},
   2: {'color': QColor(198, 128, 248, 255)},
   3: {'color': QColor(250, 220, 1, 255)},
   4: {'color': QColor(102, 230, 255, 255)},
   5: {'color': QColor(0, 0, 0, 255)},
 # 6: {'color': QColor(0, 0, 0, 255)},
   7: {'color': QColor(71, 71, 71, 255)},
 # 8: {'color': QColor(0, 0, 0, 255)},
   9: {'gradient': [QColor(255, 225, 0, 255), QColor(250, 142, 0, 255)]},
  10: {'color': QColor(165, 254, 208, 255)},
 #11: {'color': QColor(0, 0, 0, 255)},
  12: {'gradient': [QColor(255, 255, 225, 255), QColor(209, 247, 58, 255)]},
  13: {'color': QColor(71, 71, 71, 255)},
 #14: {'color': QColor(0, 0, 0, 255)},
 #15: {'color': QColor(0, 0, 0, 255)},
 #16: {'color': QColor(0, 0, 0, 255)},
 #17: {'color': QColor(0, 0, 0, 255)},
  18: {'color': QColor(71, 71, 71, 255)},
 #19: {'color': QColor(0, 0, 0, 255)},
  20: {'color': QColor(71, 71, 71, 255)},
  21: {'color': QColor(96, 219, 254, 255)},
  22: {'color': QColor(97, 214, 237, 255)},
  23: {'color': QColor(97, 246, 59, 255)},
  24: {'color': QColor(105, 105, 105, 255)},
  25: {'color': QColor(0, 0, 0, 255)},
  26: {'color': QColor(255, 80, 255, 255)},
 #98: {'color': QColor(255, 216, 0, 255)},
 #99: {'color': QColor(0, 0, 0, 255)},
 #99: {'color': QColor(255, 216, 0, 255)},
}

CLT_BORDER = {
 # 0:  {'size': 0, 'color': QColor(0, 0, 0, 255)},
   1:  {'size': 1, 'color': QColor(165, 91, 215, 255)},
   2:  {'size': 1, 'color': QColor(89, 24, 136, 255)},
   3:  {'size': 1, 'color': QColor(179, 104, 14, 255)},
 # 4:  {'size': 0, 'color': QColor(0, 0, 0, 255)},
 # 5:  {'size': 0, 'color': QColor(0, 0, 0, 255)},
 # 6:  {'size': 0, 'color': QColor(0, 0, 0, 255)},
 # 7:  {'size': 0, 'color': QColor(0, 0, 0, 255)},
   8:  {'size': 1, 'color': QColor(0, 0, 0, 255)},
   9:  {'size': 1, 'color': QColor(0, 0, 0, 255)},
  10:  {'size': 1, 'color': QColor(0, 0, 0, 255)},
  11:  {'size': 1, 'color': QColor(183, 63, 28, 255)},
 #12:  {'size': 0, 'color': QColor(0, 0, 0, 255)},
 #13:  {'size': 0, 'color': QColor(0, 0, 0, 255)},
 #14:  {'size': 0, 'color': QColor(0, 0, 0, 255)},
 #15:  {'size': 0, 'color': QColor(0, 0, 0, 255)},
  16:  {'size': 1, 'color': QColor(0, 0, 0, 255)},
  17:  {'size': 1, 'color': QColor(0, 0, 0, 255)},
 #18:  {'size': 0, 'color': QColor(0, 0, 0, 255)},
 #19:  {'size': 0, 'color': QColor(0, 0, 0, 255)},
 #20:  {'size': 0, 'color': QColor(0, 0, 0, 255)},
  21:  {'size': 1, 'color': QColor(38, 108, 236, 255)},
 #22:  {'size': 0, 'color': QColor(0, 0, 0, 255)},
 #23:  {'size': 0, 'color': QColor(0, 0, 0, 255)},
 #24:  {'size': 0, 'color': QColor(0, 0, 0, 255)},
 #25:  {'size': 0, 'color': QColor(0, 0, 0, 255)},
  26:  {'size': 2, 'color': QColor(0, 0, 0, 255)},
 #98:  {'size': 1, 'color': QColor(0, 0, 0, 255)},
 #99:  {'size': 2, 'color': QColor(0, 0, 0, 255)},
}
#CLT[99]['vscale'] = 1.00
#CLT[98]['vscale'] = .75

FONTS = {}

################################################################################
### FUNCTIONS
################################################################################

##############################################################################
### @fn   load_fonts()
### @desc Loads the two font images.
##############################################################################
def load_fonts():
  FONTS[1] = QImage(os.path.join(FONT_FOLDER, "Font01.png"))
  FONTS[2] = QImage(os.path.join(FONT_FOLDER, "Font02.png"))
  
  font_parser.parse_font(1, os.path.join(FONT_FOLDER, "Font01.font"))
  font_parser.parse_font(2, os.path.join(FONT_FOLDER, "Font02.font"))

##############################################################################
### @fn   replace_all_colors(image, color)
### @desc Replaces all colors in the image with the given color.
##############################################################################
def replace_all_colors(image, color):
  
  new_img = image.copy()
  
  color_img = QImage(new_img.width(), new_img.height(), QImage.Format_ARGB32_Premultiplied)
  color_img.fill(color.rgba())
  
  painter = QPainter(new_img)
  painter.setCompositionMode(QPainter.CompositionMode_SourceAtop)
  painter.drawImage(new_img.rect(), color_img, color_img.rect())
  painter.end()
  
  return new_img

##############################################################################
### @fn   add_v_gradient(image, colors)
### @desc Paints a vertical gradient over the image from colors[0] to colors[i]
##############################################################################
def add_v_gradient(image, colors):
  
  if len(colors) < 2:
    return image
  
  new_img = image.copy()
  
  gradient = QtGui.QLinearGradient(0, 0, 0, new_img.height())
  
  gradient.setColorAt(0, colors[0])
  
  for i in range(1, len(colors) - 1):
    gradient.setColorAt(i / len(colors), colors[i])
  
  gradient.setColorAt(1, colors[-1])
  
  painter = QPainter(new_img)
  painter.setCompositionMode(QPainter.CompositionMode_SourceAtop)
  painter.fillRect(new_img.rect(), gradient)
  painter.end()
  
  return new_img

##############################################################################
### @fn   add_border(image, color, size)
### @desc Adds a colored border to the image "size" pixels large.
##############################################################################
def add_border(image, color, size):

  w = image.width()
  h = image.height()
  
  out = QImage(w + (size * 2), h + (size * 2), QImage.Format_ARGB32_Premultiplied)
  out.fill(QColor(0, 0, 0, 0).rgba())
  
  #border = image.scaled(w, h, Qt.Qt.KeepAspectRatioByExpanding, Qt.Qt.FastTransformation)
  border = replace_all_colors(image, color)
  
  painter = QPainter(out)
  
  for i in range(0, (size * 2) + 1):
    for j in range(0, (size * 2) + 1):
      painter.drawImage(QRectF(i, j, w, h), border, QRectF((border.rect())))
  
  painter.drawImage(QRect(size, size, w, h), image, image.rect())
  painter.end()
  
  return out

##############################################################################
### @fn   filter_image(image)
### @desc Filters the image.
###       The DLL crashes on app quit for whatever reason,
###       so this presently does nothing at all. <_>
##############################################################################
def filter_image(image, filter):
  if filter == IMG_FILTERS.unfiltered:
    return image
  
  out = image.copy()
  # So we know we have 32 bits
  out.convertToFormat(QImage.Format_ARGB32_Premultiplied)
  
  if filter == IMG_FILTERS.sepia:
    pass
    # Slow as all hell.
    #def to_sepia(color):
    #  gray = QtGui.qGray(color)
    #  sepia_r = gray * 255 / 255
    #  sepia_g = gray * 240 / 255
    #  sepia_b = gray * 192 / 255
    #  sepia_a = QtGui.qAlpha(color)
    #  #return QtGui.qRgba(sepia_r, sepia_g, sepia_b, sepia_a)
    #  return sepia_r, sepia_g, sepia_b, sepia_a
    #
    #bpp = out.byteCount() / (out.width() * out.height())
    #assert bpp == 4 # Why would it be anything else?
    #
    #for j in range(out.height()):
    #  scanline = out.scanLine(j)
    #  scanline.setsize(out.bytesPerLine())
    #  QRgba* line = (QRgba*)out.scanLine(j)
    #  
    #  for i in range(out.width()):
    #    pixel = scanline[i * bpp : (i + 1) * bpp]
    #    b, g, r, a = ord(pixel[0]), ord(pixel[1]), ord(pixel[2]), ord(pixel[3])
    #    sepia_r, sepia_g, sepia_b, sepia_a = to_sepia(QtGui.qRgba(r, g, b, a))
    #    pixel[0] = chr(sepia_b)
    #    pixel[1] = chr(sepia_g)
    #    pixel[2] = chr(sepia_r)
    #    pixel[3] = chr(sepia_a)
  
  elif filter == IMG_FILTERS.inverted:
    out.invertPixels()
  
  #pixels_ptr = ctypes.c_void_p(out.bits().__int__())
  #img = filters.image(pixels_ptr, out.width(), out.height(), out.width(), out.height())
  
  #g_val = 32
  #filters.flatten(img, filters.rgb(g_val, g_val, g_val), filters.sepia)
  #filters.brightness(img, 32)
  #filters.contrast(img, 164)
  #filters.desaturate(img, 0.15)
  
  return out

##############################################################################
### @fn   draw_centering_guides(image, target_x, target_y, target_w, guide_h)
### @desc Draws two vertical red lines surrounding the given area
###       to be used to assist in centering text.
##############################################################################
def draw_centering_guides(image, target_x, target_y, target_w, guide_h):
  
  left_x = target_x - (target_w / 2.0)
  right_x = left_x + target_w
  
  top_y = target_y
  bottom_y = top_y + guide_h
  
  new_img = image.copy()
  painter = QPainter(new_img)
  
  pen = painter.pen()
  pen.setColor(QColor(255, 0, 0))
  painter.setPen(pen)
  
  painter.drawLine(left_x, top_y, left_x, bottom_y)
  painter.drawLine(right_x, top_y, right_x, bottom_y)
  
  painter.end()
  
  return new_img

##############################################################################
### @fn   get_sprite(sprite_id)
### @desc Returns the sprite for the specified sprite ID.
##############################################################################
def get_sprite(sprite_id):

  sprite_file = get_sprite_file(sprite_id)
  
  if sprite_file == None:
    return None
  
  sprite_file = os.path.join(SPRITE_DIR, sprite_file)
  
  if not os.path.isfile(sprite_file):
    sprite_file = os.path.join(SPRITE_DIR, "bustup_%02d_%02d.png" % (99, 99))
  
  out = QImage(IMG_W, IMG_H, QImage.Format_ARGB32_Premultiplied)
  out.fill(QColor(0, 0, 0, 0).rgba())
  painter = QPainter(out)
  
  sprite = QImage(sprite_file)
  
  # Center the sprite on our image.
  sprite_x = (out.width() - sprite.width()) / 2
  sprite_y = 0
  
  painter.drawImage(QRect(sprite_x, sprite_y, sprite.width(), sprite.height()), sprite, sprite.rect())
  painter.end()
  
  return out

##############################################################################
### @fn   get_bg(room_id)
### @desc Returns the background image for the specified room ID.
##############################################################################
def get_bg(room_id):
  
  if room_id == -1:
    return None
  
  bg_file = os.path.join(BG_DIR, "%04d.png" % room_id)
  
  if not os.path.isfile(bg_file):
    bg_file = os.path.join(BG_DIR, "%04d.png" % 9999)
  
  out = QImage(bg_file)
  if not out.format == QImage.Format_ARGB32_Premultiplied:
    out = out.convertToFormat(QImage.Format_ARGB32_Premultiplied)
  
  return out

##############################################################################
### @fn   get_bgd(bgd_id)
### @desc Returns the background image for the specified CG background.
##############################################################################
def get_bgd(bgd_id):
  
  if bgd_id == -1:
    return None
  
  bgd_file = os.path.join(BGD_DIR, "bgd_%03d.png" % bgd_id)
  
  if not os.path.isfile(bgd_file):
    bgd_file = os.path.join(BG_DIR, "%04d.png" % 9999)
  
  out = QImage(bgd_file)
  if not out.format == QImage.Format_ARGB32_Premultiplied:
    out = out.convertToFormat(QImage.Format_ARGB32_Premultiplied)
  
  return out

##############################################################################
### @fn   get_ammo(ammo_id, x, y)
### @desc Returns the specified ammo.
##############################################################################
def get_ammo(ammo_id, x, y):
  
  if ammo_id == -1:
    return None
  
  ammo_file =        os.path.join(AMMO_DIR, "kotodama_icn_%03d.png" % ammo_id)
  ammo_border_file = os.path.join(AMMO_DIR, "border.png")
  
  if not os.path.isfile(ammo_file):
    ammo_file = os.path.join(AMMO_DIR, "kotodama_icn_%03d.png" % 999)
  
  ammo  = QImage(ammo_file)
  border = QImage(ammo_border_file)
  
  x_pos = x
  y_pos = y
  
  out = QImage(IMG_W, IMG_H, QImage.Format_ARGB32_Premultiplied)
  out.fill(QColor(0, 0, 0, 0).rgba())
  painter = QPainter(out)
  
  painter.drawImage(QRect(x_pos, y_pos, ammo.width(), ammo.height()), ammo, ammo.rect())
  painter.drawImage(QRect(x_pos, y_pos, border.width(), border.height()), border, border.rect())
  
  painter.end()
  
  return out

##############################################################################
### @fn   get_ammo_ingame(ammo_id)
### @desc Returns the specified ammo.
##############################################################################
def get_ammo_ingame(ammo_id):
  
  x_pos = 144
  y_pos = 59
  
  return get_ammo(ammo_id, x_pos, y_pos)

##############################################################################
### @fn   get_cutin(cutin_id)
### @desc Returns the specified cutin.
##############################################################################
def get_cutin(cutin_id):
  
  if cutin_id == -1:
    return None
  
  cutin_file =        os.path.join(CUTIN_DIR, "cutin_icn_%03d.png" % cutin_id)
  cutin_border_file = os.path.join(CUTIN_DIR, "border.png")
  
  if not os.path.isfile(cutin_file):
    cutin_file = os.path.join(CUTIN_DIR, "cutin_icn_%03d.png" % 999)
  
  cutin  = QImage(cutin_file)
  border = QImage(cutin_border_file)
  
  x_pos = 277
  y_pos = 59
  
  out = QImage(IMG_W, IMG_H, QImage.Format_ARGB32_Premultiplied)
  out.fill(QColor(0, 0, 0, 0).rgba())
  painter = QPainter(out)
  
  painter.drawImage(QRect(x_pos, y_pos, cutin.width(), cutin.height()), cutin, cutin.rect())
  painter.drawImage(QRect(x_pos, y_pos, border.width(), border.height()), border, border.rect())
  
  painter.end()
  
  return out

##############################################################################
### @fn   get_flash(flash_id)
### @desc Returns the background image for the specified flash event.
##############################################################################
def get_flash(flash_id):
  
  if flash_id == -1:
    return None
  
  flash_file = os.path.join(FLASH_DIR, "fla_%03d.png" % flash_id)
  
  if not os.path.isfile(flash_file):
    flash_file = os.path.join(FLASH_DIR, "fla_%03d.png" % 999)
  
  out = QImage(flash_file)
  if not out.format == QImage.Format_ARGB32_Premultiplied:
    out = out.convertToFormat(QImage.Format_ARGB32_Premultiplied)
  
  return out

##############################################################################
### @fn   get_movie(movie_id)
### @desc Returns the background image for the specified movie.
##############################################################################
def get_movie(movie_id):
  
  if movie_id == -1:
    return None
  
  movie_file = os.path.join(MOVIEFRAME_DIR, "movie_%02d.png" % movie_id)
  
  if not os.path.isfile(movie_file):
    movie_file = os.path.join(MOVIEFRAME_DIR, "movie_%02d.png" % 99)
  
  out = QImage(movie_file)
  if not out.format == QImage.Format_ARGB32_Premultiplied:
    out = out.convertToFormat(QImage.Format_ARGB32_Premultiplied)
  
  return out

##############################################################################
### @fn   get_ammo_menu(ammo_id)
### @desc Returns the specified ammunition icon.
##############################################################################
def get_ammo_menu(ammo_id):
  
  x_pos = 35
  y_pos = 80
  
  return get_ammo(ammo_id, x_pos, y_pos)

##############################################################################
### @fn   get_present_icon(file_id)
### @desc Returns the specified present icon.
##############################################################################
def get_present_icon(file_id):
  
  icon_file = os.path.join(PRESENT_DIR, "present_icn_%03d.png" % file_id)
  
  if not os.path.isfile(icon_file):
    icon_file = os.path.join(PRESENT_DIR, "present_icn_%03d.png" % 999)
  
  icon = QImage(icon_file)
  
  x_pos = 35
  y_pos = 80
  
  out = QImage(IMG_W, IMG_H, QImage.Format_ARGB32_Premultiplied)
  out.fill(QColor(0, 0, 0, 0).rgba())  
  painter = QPainter(out)
  
  painter.drawImage(QRect(x_pos, y_pos, icon.width(), icon.height()), icon, icon.rect())
  
  painter.end()
  
  return out

##############################################################################
### @fn   get_event_icon(file_id)
### @desc Returns the specified event icon.
##############################################################################
def get_event_icon(file_id):
  
  icon_file = os.path.join(EVENT_DIR, "gallery_icn_%03d.png" % file_id)
  
  if not os.path.isfile(icon_file):
    icon_file = os.path.join(EVENT_DIR, "gallery_icn_%03d.png" % 999)
  
  icon = QImage(icon_file)
  
  x_pos = 35
  y_pos = 80
  
  out = QImage(IMG_W, IMG_H, QImage.Format_ARGB32_Premultiplied)
  out.fill(QColor(0, 0, 0, 0).rgba())  
  painter = QPainter(out)
  
  painter.drawImage(QRect(x_pos, y_pos, icon.width(), icon.height()), icon, icon.rect())
  
  painter.end()
  
  return out

##############################################################################
### @fn   get_movie_icon(file_id)
### @desc Returns the specified movie icon.
##############################################################################
def get_movie_icon(file_id):
  
  icon_file   = os.path.join(MOVIE_DIR, "movie_%03d.png" % file_id)
  border_file = os.path.join(MOVIE_DIR, "clip.png")
  
  if not os.path.isfile(icon_file):
    icon_file = os.path.join(MOVIE_DIR, "movie_%03d.png" % 999)
  
  icon   = QImage(icon_file)
  border = QImage(border_file)
  
  x_pos = 10
  y_pos = 45
  
  x_offset = 29
  y_offset = 88
  
  out = QImage(IMG_W, IMG_H, QImage.Format_ARGB32_Premultiplied)
  out.fill(QColor(0, 0, 0, 0).rgba())  
  painter = QPainter(out)
  
  painter.drawImage(QRect(x_pos, y_pos, border.width(), border.height()), border, border.rect())
  painter.drawImage(QRect(x_pos + x_offset, y_pos + y_offset, icon.width(), icon.height()), icon, icon.rect())
  
  painter.end()
  
  return out

##############################################################################
### @fn   get_box(scene_info)
### @desc Returns the text box specified by the given scene info.
##############################################################################
def get_box(scene_info):
  
  mode       = scene_info.mode
  box_color  = scene_info.box_color
  box_type   = scene_info.box_type
  speaking   = scene_info.speaking
  speaker_id = scene_info.speaker
  headshot   = scene_info.headshot
  chapter    = scene_info.chapter
  
  if box_color != common.BOX_COLORS.orange and box_color != common.BOX_COLORS.green and box_color != common.BOX_COLORS.blue:
    box_color = common.BOX_COLORS.orange
  
  if not speaker_id in common.CHAR_IDS:
    speaker_id = None
  
  out = QImage(IMG_W, IMG_H, QImage.Format_ARGB32_Premultiplied)
  out.fill(QColor(0, 0, 0, 0).rgba())
  
  painter = QPainter(out)
  painter.setRenderHint(QPainter.Antialiasing, True)
  
  # Some commonality between the boxes.
  box     = QImage()
  button  = QImage()
  
  if not speaker_id == None:
    nametag = QImage(os.path.join(NAMETAG_DIR, "%02d" % speaker_id))
  else:
    nametag = QImage()
  
  nametag_offset = ()
  
  if box_type == common.BOX_TYPES.flat:
    box    = QImage(os.path.join(TEXTBOX_DIR, "box_gray.png"))
    button = QImage(os.path.join(TEXTBOX_DIR, "button_gray.png"))
    nametag_color = QColor(255, 255, 255, 255)
    nametag_offset = (9, 187)
  
  elif box_type == common.BOX_TYPES.normal:
    
    if mode == common.SCENE_MODES.normal:
      
      box    = QImage(os.path.join(TEXTBOX_DIR, "box.png"))
      button = QImage(os.path.join(TEXTBOX_DIR, "button_%s.png" % box_color))
      nametag_color = QColor(60, 60, 60, 255)
      nametag_offset = (10, 180)
      
      box_painter = QPainter(box)
      box_painter.setRenderHint(QPainter.Antialiasing, True)
      
      if speaking and not speaker_id == None:
        label_file = os.path.join(TEXTBOX_DIR, "speaking_label.png")
        speaking_file = os.path.join(TEXTBOX_DIR, "speaking_%s.png" % box_color)
        
        label = QImage(label_file)
        speaking_img = QImage(speaking_file)
        
        box_painter.drawImage(box.rect(), speaking_img, speaking_img.rect())
        box_painter.drawImage(box.rect(), label, label.rect())
      
      if speaker_id == 0: # Naegi gets a special text box.
        namebox = QImage(os.path.join(TEXTBOX_DIR, "name_naegi_%s.png" % box_color))
      elif not speaker_id == None:
        namebox = QImage(os.path.join(TEXTBOX_DIR, "name_%s.png" % box_color))
      else:
        namebox = QImage()
        
      box_painter.drawImage(box.rect(), namebox, namebox.rect())
      
      box_painter.end()
    
    elif mode == common.SCENE_MODES.trial:
      
      if not headshot == None:
        box_base = QImage(os.path.join(TRIAL_DIR, "trial_speaking.png"))
        case_num = QImage(os.path.join(TRIAL_DIR, "case", "case%1d.png" % chapter))
        underlay = QImage(os.path.join(TRIAL_DIR, "pink.png"))
      else:
        box_base = QImage(os.path.join(TRIAL_DIR, "trial_narration.png"))
        case_num = QImage()
        underlay = QImage()
      
      if not headshot == None:
        headshot = QImage(os.path.join(TRIAL_DIR, "headshot", "%02d.png" % headshot))
      else:
        headshot = QImage()
      
      button = QImage(os.path.join(TRIAL_DIR, "button.png"))
      nametag_color = QColor(0, 0, 0, 255)
      nametag_offset = (20, 183)
      
      box = QImage(IMG_W, IMG_H, QImage.Format_ARGB32_Premultiplied)
      box.fill(QColor(0, 0, 0, 0).rgba())
      
      box_painter = QPainter(box)
      box_painter.setRenderHint(QPainter.Antialiasing, True)
      
      box_painter.drawImage(box.rect(), underlay, underlay.rect())
      box_painter.drawImage(box.rect(), headshot, headshot.rect())
      box_painter.drawImage(box.rect(), box_base, box_base.rect())
      box_painter.drawImage(box.rect(), case_num, case_num.rect())
      
      box_painter.end()
    
    else:
      box = QImage(IMG_W, IMG_H, QImage.Format_ARGB32_Premultiplied)
      box.fill(QColor(0, 0, 0, 0).rgba())
  
  painter.drawImage(out.rect(), box,     box.rect())
  painter.drawImage(out.rect(), button,  button.rect())
  
  if not speaker_id == None:
    nametag = replace_all_colors(nametag, nametag_color)
    painter.drawImage(QRect(nametag_offset[0], nametag_offset[1], nametag.width(), nametag.height()), nametag, nametag.rect())
  
  painter.end()
  
  return out

##############################################################################
### @fn   get_normal(scene_info, show_bg = True, show_sprite = True, show_box = True)
### @desc Returns an image containing the scene in normal mode.
##############################################################################
def get_normal(scene_info, show_bg = True, show_sprite = True, show_box = True):
  
  sprite_id = scene_info.sprite
  room_id = scene_info.room
  scene_id = scene_info.scene
  
  out = QImage(IMG_W, IMG_H, QImage.Format_ARGB32_Premultiplied)
  out.fill(QColor(0, 0, 0, 0).rgba())
  
  painter = QPainter(out)
  painter.setRenderHint(QPainter.Antialiasing, True)
  
  if show_bg:
    if scene_info.movie >= 0:
      bg = get_movie(scene_info.movie)
    elif scene_info.flash >= 0:
      bg = get_flash(scene_info.flash)
    elif scene_info.bgd >= 0:
      bg = get_bgd(scene_info.bgd)
    else:
      bg = get_bg(room_id)
    
    if bg:
      painter.drawImage(out.rect(), bg, bg.rect())
  
  if show_sprite:
    sprite = get_sprite(sprite_id)
    if sprite:
      painter.drawImage(out.rect(), sprite, sprite.rect())
  
  if not scene_info.img_filter == IMG_FILTERS.unfiltered:
    painter.end()
    out = filter_image(out, scene_info.img_filter)
    painter = QPainter(out)
    painter.setRenderHint(QPainter.Antialiasing, True)
  
  if show_box:
    box = get_box(scene_info)
    painter.drawImage(out.rect(), box, box.rect())
  
  painter.end()
  
  return out

##############################################################################
### @fn   get_trial(scene_info, show_bg = True, show_sprite = True, show_box = True)
### @desc Returns an image containing the scene in trial mode.
##############################################################################
def get_trial(scene_info, show_bg = True, show_sprite = True, show_box = True):
  
  case_num = scene_info.chapter
  sprite_id = scene_info.sprite
  
  if case_num > 6 or case_num <= 0:
    case_num = 1
  
  out = None
  
  if show_bg:
    if scene_info.movie >= 0:
      out = get_movie(scene_info.movie)
    elif scene_info.flash >= 0:
      out = get_flash(scene_info.flash)
    elif scene_info.bgd >= 0:
      out = get_bgd(scene_info.bgd)
    else:
      out = QImage(os.path.join(TRIAL_DIR, "bg", "%02d.png" % case_num))
  else:
    out = QImage(IMG_W, IMG_H, QImage.Format_ARGB32_Premultiplied)
    out.fill(QColor(0, 0, 0, 0).rgba())
  
  painter = QPainter(out)
  painter.setRenderHint(QPainter.Antialiasing, True)
  
  if show_sprite:
    sprite_id.sprite_type = SPRITE_TYPE.stand
    
    sprite = get_sprite(sprite_id)
    if sprite:
      painter.drawImage(out.rect(), sprite, sprite.rect())
  
  if not scene_info.img_filter == IMG_FILTERS.unfiltered:
    painter.end()
    out = filter_image(out, scene_info.img_filter)
    painter = QPainter(out)
    painter.setRenderHint(QPainter.Antialiasing, True)
  
  if show_box:
  
    box = get_box(scene_info)
    painter.drawImage(out.rect(), box, box.rect())
  
  return out

##############################################################################
### @fn   get_letter(clt, char)
### @desc Returns an image containing the letter rendered with the given CLT.
##############################################################################
def get_letter(clt, char):
  
  if not clt in CLT:
    clt = 0
  
  font    = CLT[clt]['font']
  hscale  = CLT[clt]['hscale']
  vscale  = CLT[clt]['vscale']
  
  try:
    info = FONT_DATA[font][char]
  except:
    # This is the character the game replaces unknown characters with.
    info = FONT_DATA[font][u'\u2261']
  
  expand_l = 0
  expand_r = 0
  expand_t = 0
  expand_b = 0
  
  if clt in CLT_EXPAND:
    expand_l = CLT_EXPAND[clt][0]
    expand_r = CLT_EXPAND[clt][1]
    expand_t = CLT_EXPAND[clt][2]
    expand_b = CLT_EXPAND[clt][3]
  
  box = QRect(info['x'] - expand_l, info['y'] - expand_t, info['w'] + expand_l + expand_r, info['h'] + expand_t + expand_b)
  #box = QRect(info['x'] - expand_l, info['y'] - expand_t, info['w'], info['h'])
  
  if clt in CLT_BORDER:
    expand_l += CLT_BORDER[clt]['size']
    expand_r += CLT_BORDER[clt]['size']
    expand_t += CLT_BORDER[clt]['size']
    expand_b += CLT_BORDER[clt]['size']
  
  xshift = -expand_l
  yshift = -expand_t
  
  if font == 1:
    yshift += 6
  #elif font == 2:
    #yshift += 2
  
  base_w = info['w'] + expand_l + expand_r
  base_h = info['h'] + expand_t + expand_b
  
  final_w = base_w
  final_h = base_h
  
  if hscale != 1.0:
    final_w = (final_w * hscale)
  
  if vscale != 1.0:
    old_h   = final_h
    final_h = (final_h * vscale)
    
    yshift = yshift + old_h - final_h
  
  letter = FONTS[CLT[clt]['font']].copy(box)
  
  if hscale != 1.0 or vscale != 1.0:
    matrix = QMatrix()
    matrix.scale(hscale, vscale)
    letter = letter.transformed(matrix, Qt.Qt.SmoothTransformation)
    #letter = letter.scaled(int(final_w), int(final_h), Qt.Qt.IgnoreAspectRatio, Qt.Qt.SmoothTransformation)
  
  if clt in CLT_INSIDE:
    if 'color' in CLT_INSIDE[clt]:
      letter = replace_all_colors(letter, CLT_INSIDE[clt]['color'])
    elif 'gradient' in CLT_INSIDE[clt]:
      letter = add_v_gradient(letter, CLT_INSIDE[clt]['gradient'])
  
  if clt in CLT_BORDER:
    letter = add_border(letter, CLT_BORDER[clt]['color'], CLT_BORDER[clt]['size'])
  
  return letter, (xshift, yshift, final_w, final_h)

##############################################################################
### @fn   mangle_line(line, lengths, scene_mode, cur_font)
### @desc Hack the line up a bit to reflect how it'll show up in-game
###       based on some in-game quirks.
##############################################################################
def mangle_line(line, lengths, index, scene_mode, cur_font, default_clt):
  
  # If it doesn't have a category, assume it's safe.
  if scene_mode == common.SCENE_MODES.other:
    return line, lengths

  # The game auto-wraps after 54 characters.
  # Not that we should ever run into an issue with that.
  max_len = 54
  
  # Replace extra characters with something ugly
  # so it's easy to know it needs to be fixed.
  too_long  = u'\u2261'
  
  # The max length is even tighter 
  if scene_mode == common.SCENE_MODES.ammo or scene_mode == common.SCENE_MODES.present:
    if index == 0:   max_len = 61
    else:            max_len = 61
    
    # Keep the code here for posterity, but we don't need it to do anything.
    # min_len = 14
    # too_short = u'®'
    
    # if (index == 0 or index == 1) and len(line) < min_len:
      # extra_chars = min_len - len(line)
      
      # line += too_short * (extra_chars)
      
      # char_width = FONT_DATA[cur_font][too_short]['w'] * CLT[default_clt]["hscale"]
      # lengths[index][max_len:] = [char_width] * extra_chars
  
  elif scene_mode == common.SCENE_SPECIAL.option:
    max_len = 24
  
  elif scene_mode == common.SCENE_MODES.help:
    max_len = 31
  
  extra_chars = len(line) - max_len
  if extra_chars > 0:
  
    line = line[:max_len] + (too_long * extra_chars)
    
    char_width = FONT_DATA[cur_font][too_long]['w'] * CLT[default_clt]["hscale"]
    lengths[index][max_len:] = [char_width] * extra_chars
  
  return line, lengths

##############################################################################
### @fn   print_text(image, text, scene_mode = common.SCENE_MODES.normal)
### @desc Prints the given text onto the given image.
##############################################################################
def print_text(image, text, scene_mode = common.SCENE_MODES.normal, mangle = True):
  
  # A couple exceptions.
  if scene_mode in [common.SCENE_MODES.ammo, common.SCENE_MODES.present]:
    text_lines = text.split('\n')
    temp_text = text_lines[:2]
    temp_text = '\n'.join(temp_text)
    if len(text_lines) > 2:
      temp_text += "..."
    image = print_text(image, temp_text, common.SCENE_MODES.ammosummary, False)
  
  #default_clt = 0
  format = TEXT_FORMAT[scene_mode]
  
  # Replace our unmarked CLTs with whatever default CLT we're given.
  # Also start the line off with the default CLT so we're definitely using it.
  # Useful for modes like Nonstop Debate, where text is normally CLT 16.
  text = "<CLT>" + text
  text = re.sub("<CLT>", "<CLT %d>" % format["clt"], text)
  
  img_w = IMG_W
  img_h = IMG_H
  
  if image:
    img_w = image.width()
    img_h = image.height()
    
  out = QImage(img_w, img_h, QImage.Format_ARGB32_Premultiplied)
  out.fill(QColor(0, 0, 0, 0).rgba())
  
  painter = QPainter(out)
  # This is a better representation of how the game handles text.
  painter.setCompositionMode(QPainter.CompositionMode_DestinationOver)
  painter.setRenderHint(QPainter.Antialiasing, True)
  
  split_text = text.split("\n")
  lines = []
  lengths = []
  clt_changes = []
  last_clt = format["clt"]
  
  for line in split_text:
    # Start the line off with the last-used CLT, so the parsers know what it is.
    line = ("<CLT %d>" % last_clt) + line
    
    line, length, clt = font_parser.get_len(line, format["clt"])
    # If there isn't an initial CLT, start the line off with
    # the CLT still in use at the end of the previous line.
    if not 0 in clt.keys():
      clt[0] = last_clt
    
    last_clt = clt[max(clt.keys())]
    
    # If we're supposed to skip blanks and this line is blank
    # after parsing the formatting, then don't add it to the list.
    if format["killblanks"] and line.strip() == "":
      continue
    
    lines.append(line)
    lengths.append(length)
    clt_changes.append(clt)
  
  base_x      = format["x"]
  base_y      = format["y"]
  line_height = format["h"]
  
  x, y = base_x, base_y
  cur_clt = 0
  cur_font = 1
  cur_hscale = 1.0
  cur_vscale = 1.0
  
  if len(lines) == 0:
    text_height = 0
  else:
    text_height = ((len(lines) - 1) * line_height) + 25
  while text_height + y > IMG_H:
    y -= line_height
    
    #if y < 0:
      #y = 0
      #break
      
  center_x = format["x"] + (format["w"] / 2.0)
  right_x  = format["x"] + format["w"]
  
  for i in range(len(lines)):
    line = lines[i]
    
    # Only bother if we actually see the line.
    if y > -line_height and y < img_h:
      # Hack the line up a bit to reflect how it'll show up in-game
      # based on some in-game quirks.
      if mangle:
        line, lengths = mangle_line(line, lengths, i, scene_mode, cur_font, format["clt"])
      
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
        # painter.end()
        # stripped_len = line_length
        
        # Strip the widths of any leading and trailing spaces
        # for j in range(len(line)):
          # if line[j] == ' ' or line[j] == u'　':
            # stripped_len -= lengths[i][j]
          # else:
            # break
        # for j in reversed(range(len(line))):
          # if line[j] == ' ' or line[j] == u'　':
            # stripped_len -= lengths[i][j]
          # else:
            # break
          
        # out = draw_centering_guides(out, center_x, y, stripped_len, 40)
        # painter = QPainter(out)
        # painter.setCompositionMode(QPainter.CompositionMode_DestinationOver)
        # painter.setRenderHint(QPainter.Antialiasing, True)
      # if format["a"] == blah
      
      for j in range(len(line)):
        char = line[j]
        
        if j in clt_changes[i]:
          cur_clt = clt_changes[i][j]
        
        letter, (xshift, yshift, final_w, final_h) = get_letter(cur_clt, char)
        
        final_x = (x + xshift)
        final_y = (y + yshift) + max(0, (line_height - final_h)) + CLT[cur_clt]['yshift']
        
        # kind of hackish, lol, but the debate text
        # is centered vertically per line as well.
        if scene_mode == common.SCENE_MODES.debate:
          final_y -= (26 - final_h) / 2
        
        painter.drawImage(QRect(final_x, final_y, final_w, final_h), letter, letter.rect())
        
        x += lengths[i][j]# + CLT[cur_clt]['xshift']
      # for j in range(len(line))
      
    # if y > -line_height and y < img_h
    
    y = y + line_height
    
  # And, last but not least, draw the image underneath everything.
  if image:
    painter.drawImage(out.rect(), image, image.rect())
  
  painter.end()
  return out

##############################################################################
### @fn   draw_anagram(anagram)
### @desc Draws an Epiphany Anagram scene based on the given info.
##############################################################################
def draw_anagram(anagram):
  
  BOX_LEFT      = 4
  BOX_TOP       = 22
  BOX_X_OFFSET  = 31
  BOX_Y_OFFSET  = 61
  
  TEXT_X_OFFSET = 13
  TEXT_Y_OFFSET = 9
  TEXT_CLT      = 8
  FONT          = CLT[TEXT_CLT]['font']
  
  MAX_LETTERS   = 15
  
  BOX = QImage(os.path.join(ANAGRAM_DIR, "box.png"))
  QUESTION = QImage(os.path.join(ANAGRAM_DIR, "question.png"))
  out = QImage(os.path.join(ANAGRAM_DIR, "bg.png"))
  
  text = anagram.solution.translated
  
  if len(text) == 0:
    return out
  
  painter = QPainter(out)
  painter.setRenderHint(QPainter.Antialiasing, True)
  
  # Put them in a list so it's easier to loop.
  visible = [range(1, len(text) + 1), anagram.easy, anagram.normal, anagram.hard]
  
  x = BOX_LEFT
  y = BOX_TOP
  
  for row in range(len(visible)):
    
    if not visible[row] == None:
      for i, char in enumerate(text):
      
        if (i + 1) in visible[row]:
          
          painter.drawImage(QRect(x, y, BOX.width(), BOX.height()), BOX, BOX.rect())
          
          # Get info on our current letter.
          letter, (xshift, yshift, final_w, final_h) = get_letter(TEXT_CLT, char)
          painter.drawImage(QRect(x + TEXT_X_OFFSET + xshift, y + TEXT_Y_OFFSET + yshift, final_w, final_h), letter, letter.rect())
        
        else:
          painter.drawImage(QRect(x, y, QUESTION.width(), QUESTION.height()), QUESTION, QUESTION.rect())
        
        x += BOX_X_OFFSET
      
    x = BOX_LEFT
    y += BOX_Y_OFFSET
  
  painter.end()
  
  return out

##############################################################################
### @fn   draw_scene(scene_info, text = None)
### @desc Wrapper function for most of the above stuff.
###       Calls the necessary functions to construct the scene based on
###       the given scene information.
##############################################################################
def draw_scene(scene_info, text = None):
  bg = None
  max_length = 0
  kill_blanks = False
  
  if scene_info.mode == common.SCENE_MODES.normal:
    bg = get_normal(scene_info)
    
  elif scene_info.mode == common.SCENE_MODES.trial:
    bg = get_trial(scene_info)
  
  elif scene_info.mode == common.SCENE_MODES.rules:
    bg = QImage(os.path.join(MENU_DIR, "rules.png"))
  
  elif scene_info.mode in [common.SCENE_MODES.ammo, common.SCENE_MODES.ammoname, common.SCENE_MODES.present, common.SCENE_MODES.presentname]:
    bg = QImage(os.path.join(MENU_DIR, "ammo.png"))
    
    if scene_info.mode in [common.SCENE_MODES.ammo, common.SCENE_MODES.ammoname]:
      overlay = get_ammo_menu(scene_info.file_id)
    else:
      overlay = get_present_icon(scene_info.file_id)
    
    painter = QPainter(bg)
    painter.drawImage(bg.rect(), overlay, overlay.rect())
    painter.end()
  
  elif scene_info.mode == common.SCENE_MODES.menu:
    bg = QImage(os.path.join(MENU_DIR, "menu.png"))
  
  elif scene_info.mode == common.SCENE_MODES.report or scene_info.mode == common.SCENE_MODES.report2:
    bg = QImage(os.path.join(MENU_DIR, "report.png"))
  
  elif scene_info.mode == common.SCENE_MODES.skill or scene_info.mode == common.SCENE_MODES.skill2:
    bg = QImage(os.path.join(MENU_DIR, "skills.png"))
  
  elif scene_info.mode == common.SCENE_MODES.map:
    bg = QImage(os.path.join(MENU_DIR, "map.png"))
  
  elif scene_info.mode == common.SCENE_MODES.music:
    bg = QImage(os.path.join(MENU_DIR, "soundtest.png"))
  
  elif scene_info.mode == common.SCENE_MODES.eventname or scene_info.mode == common.SCENE_MODES.moviename:
    bg = QImage(os.path.join(MENU_DIR, "gallery.png"))
    
    if scene_info.mode == common.SCENE_MODES.eventname:
      overlay = get_event_icon(scene_info.file_id)
    else:
      overlay = get_movie_icon(scene_info.file_id)
    
    painter = QPainter(bg)
    painter.drawImage(bg.rect(), overlay, overlay.rect())
    painter.end()
  
  elif scene_info.mode == common.SCENE_MODES.theatre:
    bg = get_normal(scene_info)
  
  elif scene_info.mode == common.SCENE_MODES.debate:
    bg = get_trial(scene_info, show_box = False)
    
  else:
    bg = QImage(IMG_W, IMG_H, QImage.Format_ARGB32_Premultiplied)
    bg.fill(QColor(0, 0, 0, 255).rgba())
  
  if scene_info.cutin != -1:
    cutin = get_cutin(scene_info.cutin)
    
    painter = QPainter(bg)
    painter.drawImage(bg.rect(), cutin, cutin.rect())
    painter.end()
  
  if scene_info.ammo != -1:
    ammo = get_ammo_ingame(scene_info.ammo)
    
    painter = QPainter(bg)
    painter.drawImage(bg.rect(), ammo, ammo.rect())
    painter.end()
  
  if scene_info.special == common.SCENE_SPECIAL.option:
    overlay = QImage(os.path.join(TEXTBOX_DIR, "option_bar.png"))
    painter = QPainter(bg)
    painter.drawImage(bg.rect(), overlay, overlay.rect())
    painter.end()
    
    if not text == None and not text == "":
      bg = print_text(bg, text, common.SCENE_SPECIAL.option, False)
      
  if not text == None and not text == "":
    bg = print_text(bg, text, scene_info.mode)
  
  return bg

# Anyone using this needs the fonts, so let's go at it.
load_fonts()

if __name__ == "__main__":
  # def get_text(text, scene_mode = common.SCENE_MODES.normal)
  #test = get_text("<CLT 3>Who the hell do you\nthink you are?!", common.SCENE_MODES.normal, False)
  test = QImage(os.path.join(SPRITE_DIR, "bustup_05_13.png"))
  test = filter_image(test, IMG_FILTERS.sepia)
  test.save("ss/test.png")

### EOF ###