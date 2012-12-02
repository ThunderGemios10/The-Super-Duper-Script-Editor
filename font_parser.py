﻿################################################################################
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

from bitstring import ConstBitStream
import os.path
import re

BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
FONT_FOLDER   = os.path.join(BASE_DIR, "data/gfx/font")
FONT1_TABLE   = "Font01.font"
FONT2_TABLE   = "Font02.font"

SPFT_MAGIC     = ConstBitStream(hex='0x7446705304000000')

RE_DEFAULT_CLT = re.compile(ur"<CLT>", re.UNICODE | re.S)
RE_CLT         = re.compile(ur"\<CLT (?P<CLT_INDEX>\d+)\>", re.UNICODE | re.S)
RE_DIG         = re.compile(ur"<DIG.*?>", re.UNICODE | re.S)

FONT_DATA = { 1: {}, 2: {}}

CLT = {
         0: {'font': 1, 'hscale': 1.00,       'vscale': 1.00,       'xshift': 0.00,   'yshift': 0.00},
         1: {'font': 1, 'hscale': 1.00,       'vscale': 1.00,       'xshift': 0.00,   'yshift': 0.00},
         2: {'font': 1, 'hscale': 1.00,       'vscale': 1.00,       'xshift': 0.00,   'yshift': 0.00},
         3: {'font': 1, 'hscale': 1.00,       'vscale': 1.00,       'xshift': 0.00,   'yshift': 0.00},
         4: {'font': 1, 'hscale': 1.00,       'vscale': 1.00,       'xshift': 0.00,   'yshift': 0.00},
         5: {'font': 2, 'hscale': 0.69,       'vscale': 0.69,       'xshift': 0.00,   'yshift': 0.00},
         6: {'font': 1, 'hscale': 0.80,       'vscale': 0.80,       'xshift': -1.00,  'yshift': 0.00},
         7: {'font': 1, 'hscale': 0.80,       'vscale': 0.80,       'xshift': -1.00,  'yshift': 0.00},
         8: {'font': 2, 'hscale': 5.0 / 6.0,  'vscale': 5.0 / 6.0,  'xshift': -1.00,  'yshift': 1.00},
         9: {'font': 2, 'hscale': 1.00,       'vscale': 1.00,       'xshift': 0.00,   'yshift': 0.00},
        10: {'font': 2, 'hscale': 1.00,       'vscale': 1.00,       'xshift': 0.00,   'yshift': 0.00},
        11: {'font': 2, 'hscale': 1.00,       'vscale': 1.00,       'xshift': 0.00,   'yshift': 0.00},
        12: {'font': 2, 'hscale': 5.0 / 6.0,  'vscale': 5.0 / 6.0,  'xshift': -1.00,  'yshift': 0.00},
        13: {'font': 1, 'hscale': 0.80,       'vscale': 0.80,       'xshift': -1.00,  'yshift': 0.00},
        14: {'font': 1, 'hscale': 0.80,       'vscale': 0.80,       'xshift': -1.00,  'yshift': 0.00},
        15: {'font': 1, 'hscale': 1.00,       'vscale': 1.00,       'xshift': 0.00,   'yshift': 0.00},
        16: {'font': 2, 'hscale': 1.00,       'vscale': 1.00,       'xshift': 0.00,   'yshift': 0.00},
        17: {'font': 2, 'hscale': 2.0 / 3.0,  'vscale': 2.0 / 3.0,  'xshift': 0.00,   'yshift': 0.00},
        18: {'font': 1, 'hscale': 0.80,       'vscale': 0.80,       'xshift': -1.00,  'yshift': 0.00},
        19: {'font': 1, 'hscale': 0.80,       'vscale': 0.80,       'xshift': -1.00,  'yshift': 0.00},
        20: {'font': 1, 'hscale': 1.00,       'vscale': 1.00,       'xshift': 0.00,   'yshift': 0.00},
        21: {'font': 1, 'hscale': 0.80,       'vscale': 0.80,       'xshift': -1.00,  'yshift': 0.00},
        22: {'font': 1, 'hscale': 0.80,       'vscale': 0.80,       'xshift': -1.00,  'yshift': 0.00},
        23: {'font': 1, 'hscale': 1.00,       'vscale': 1.00,       'xshift': 0.00,   'yshift': 0.00},
        24: {'font': 1, 'hscale': 0.80,       'vscale': 0.80,       'xshift': -1.00,  'yshift': 0.00},
        25: {'font': 1, 'hscale': 1.00,       'vscale': 1.00,       'xshift': 0.00,   'yshift': 0.00},
        26: {'font': 2, 'hscale': 1.00,       'vscale': 1.00,       'xshift': 0.00,   'yshift': 0.00},
        98: {'font': 1, 'hscale': 1.00,       'vscale': 1.00,       'xshift': 0.00,   'yshift': 0.00},
        99: {'font': 2, 'hscale': 1.00,       'vscale': 1.00,       'xshift': 0.00,   'yshift': 0.00},
      }

def parse_font(font_num):
  
  FONT_DATA[font_num] = {}
  
  spft_filename = ""
  
  if font_num == 1:
    spft_filename = os.path.join(FONT_FOLDER, FONT1_TABLE)
  elif font_num == 2:
    spft_filename = os.path.join(FONT_FOLDER, FONT2_TABLE)
  else:
    print "Invalid font number. Valid values: 1, 2"
    exit()
  
  # Header: 
  # 74467053 -- Magic
  # 04000000 -- Magic
  # XXXXXXXX -- Number of entries in font table
  # XXXXXXXX -- Position of first entry in font table
  # 
  # XXXXXXXX -- Number of chunks in the mappings table
  # XXXXXXXX -- Start position of mappings table (little-endian, as always)
  #             ***0x20000000 in both fonts I've seen
  # XXXXXXXX -- ????
  # XXXXXXXX -- ????
  # 
  # Character Mappings: from start pos (0x20) to (start pos + (# chunks * 2))
  #   * To avoid overcomplicating this, I'm just referring to the start pos as
  #     0x20 since I've only ever seen that value used.
  #   * Two-byte chunks (XXXX)
  #   * The position of each chunk, minus 0x20, divided by two (because they're
  #     two-byte chunks), equals the UTF-16 representation of a character.
  #     (i.e. pos 0x00A8: (0x00A8 - 0x20) / 2 = 0x0044 -> "A")
  #   * The value of each chunk is the index of that character in the font table,
  #     little-endian.
  #     (i.e. if the character "A" is the 35th entry, zero-indexed = 0x2200)
  #   * A chunk value of 0xFFFF means that character is not present in the font.
  spft = ConstBitStream(filename = spft_filename)
  
  magic = spft.read(64)
  
  if magic != SPFT_MAGIC:
    print "Didn't find SPFT magic."
    exit()
  
  num_entries = spft.read('uintle:32')
  table_start = spft.read('uintle:32')
  
  if num_entries == 0:
    print "No entries in SPFT table."
    exit()
  
  if table_start * 8 > spft.len:
    print "Invalid SPFT table position."
    exit()
  
  #print "Characters in font:", num_entries
  
  spft.pos = table_start * 8
  
  # Table:
  # * Entry:
  #   XXXX -- Character
  #   XXXX -- X Pos
  #   XXXX -- Y Pos
  #   XXXX -- Width
  #   XXXX -- Height
  #   0000 -- Dummy
  #   0000 -- Dummy
  #   FA08 -- Dummy
  
  #print "    XXXX YYYY WWW HHH"
  
  for i in range(0, num_entries):
    char = spft.read(16)
    char = char.bytes.decode('utf-16le')    
    xpos = spft.read('uintle:16')
    ypos = spft.read('uintle:16')
    width = spft.read('uintle:16')
    height = spft.read('uintle:16')
    dummy = spft.read('uintle:16')
    dummy = spft.read('uintle:16')
    dummy = spft.read('uintle:16')
    
    info = {'x': xpos, 'y': ypos, 'w': width, 'h': height}
    FONT_DATA[font_num][char] = info
    
    #print "%3s %4d %4d %3d %3d" % (char.encode('cp932'), xpos, ypos, width, height)

def parse_string(string, default_clt = 0):
  
  string = RE_DEFAULT_CLT.sub("<CLT %d>" % default_clt, string)
  string = RE_DIG.sub("00", string)
  
  clt_changes = {}
  
  while True:
    match = RE_CLT.search(string)
    
    if match == None:
      break
    
    clt_val = match.groupdict(default = default_clt)["CLT_INDEX"]
    
    if clt_val == None:
      clt_val = default_clt
    else:
      clt_val = int(clt_val)
    
    clt_changes[match.start()] = clt_val
    
    string = string[:match.start()] + string[match.end():]
    #print string
  
  return string, clt_changes
  
def get_len(string, default_clt = 0):
  
  string, clt_changes = parse_string(string, default_clt)
  
  cur_font = CLT[default_clt]['font']
  cur_scale = CLT[default_clt]['hscale']
  cur_xshift = CLT[default_clt]['xshift']
  
  total_width = 0
  
  lengths = []
  
  for i in range(len(string)):
    if i in clt_changes:
      clt = clt_changes[i]
      if not clt in CLT:
        clt = default_clt
        clt_changes[i] = default_clt
      cur_font = CLT[clt]['font']
      cur_scale = CLT[clt]['hscale']
      cur_xshift = CLT[clt]['xshift']
    
    if string[i] in FONT_DATA[cur_font]:
      char_width = FONT_DATA[cur_font][string[i]]['w'] * cur_scale
      #print string[i], char_width
    else:
      # This is the character the game uses to replace unknown characters.
      char_width = FONT_DATA[cur_font][u'\u2261']['w'] * cur_scale
    char_width += cur_xshift
    
    total_width = total_width + char_width
    
    lengths.append(char_width)
  
  return string, lengths, clt_changes

parse_font(1)
parse_font(2)

if __name__ == '__main__':
  #for char in sorted(FONT_DATA[1].keys()):
    #info = FONT_DATA[1][char]
    #print "%3s %4d %4d %3d %3d" % (char.encode('utf-8'), info['x'], info['y'], info['w'], info['h'])
  print ''.join(sorted(FONT_DATA[2].keys())).encode('utf-8')

### EOF ###