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

from enum import Enum

from .unique_postfix import add_unique_postfix

START       = "start"
COUNT       = "count"
NAME_OFFSET = "name_offset"

GAMES     = Enum("demo", "full", "best", "hack_v1", "hack_v2")
UMDIMAGES = Enum("umdimage", "umdimage2")

EBOOT_SIZES  = {
  GAMES.demo:     1962344,
  GAMES.full:     1559120,
  GAMES.best:     1566304,
  GAMES.hack_v1:  1570400, # Pre 500-char hack
  GAMES.hack_v2:  1640032, # Post 500-char hack
}

TOC_INFO = {
  UMDIMAGES.umdimage: {
    GAMES.demo:     {START: 0x00145C24, COUNT: 0x00145C1C, NAME_OFFSET: 0xC0},
    GAMES.full:     {START: 0x000F8248, COUNT: 0x000F8240, NAME_OFFSET: 0xC0},
    GAMES.best:     {START: 0x000F5A18, COUNT: 0x00100EB4, NAME_OFFSET: 0xA0},
    GAMES.hack_v1:  {START: 0x000F5A38, COUNT: 0x00100ED4, NAME_OFFSET: 0xC0},
    GAMES.hack_v2:  {START: 0x000F5A38, COUNT: 0x00100ED4, NAME_OFFSET: 0xC0},
  },
  UMDIMAGES.umdimage2: {
    GAMES.full:     {START: 0x00103C5C, COUNT: 0x00103C54, NAME_OFFSET: 0xC0},
    GAMES.best:     {START: 0x000F5200, COUNT: 0x000F5A10, NAME_OFFSET: 0xA0},
    GAMES.hack_v1:  {START: 0x000F5220, COUNT: 0x000F5A30, NAME_OFFSET: 0xC0},
    GAMES.hack_v2:  {START: 0x000F5220, COUNT: 0x000F5A30, NAME_OFFSET: 0xC0},
  }
}

############################################################
### FUNCTIONS
############################################################

##################################################
### 
##################################################
def guess_game(eboot_data):
  len = eboot_data.len / 8
  
  for game in EBOOT_SIZES:
    if EBOOT_SIZES[game] == len:
      return game
  
  return None

##################################################
### 
##################################################
def get_toc(eboot_data, umdimage):
  
  game = guess_game(eboot_data)
  
  if game == None:
    raise ValueError("EBOOT size doesn't match any known game.")
  
  toc_start     = TOC_INFO[umdimage][game][START]
  toc_count_pos = TOC_INFO[umdimage][game][COUNT]
  toc_name_off  = TOC_INFO[umdimage][game][NAME_OFFSET]
  
  eboot_data.bytepos = toc_count_pos
  toc_count = eboot_data.read("uintle:32")
  
  eboot_data.bytepos = toc_start
  
  toc         = []
  file_starts = []
  filenames   = []
  
  for i in xrange(toc_count):
    name_pos = eboot_data.read("uintle:32")
    
    file_pos_pos  = eboot_data.bytepos
    file_pos      = eboot_data.read("uintle:32")
    file_len_pos  = eboot_data.bytepos
    file_len      = eboot_data.read("uintle:32")
    
    name_pos += toc_name_off
    
    temp_pos = eboot_data.bytepos
    eboot_data.bytepos = name_pos
    
    filename = eboot_data.readto("0x00", bytealigned = True).bytes
    # Strip the null character.
    filename = filename[:-1]
    
    # Ensure the filenames don't conflict.
    filename = add_unique_postfix(filename, check_fn = (lambda fn: fn in filenames))
    filenames.append(filename)
    
    eboot_data.bytepos = temp_pos
    
    entry = {
      "filename":     filename,
      "file_pos_pos": file_pos_pos,
      "file_pos":     file_pos,
      "file_len_pos": file_len_pos,
      "file_len":     file_len,
    }
    
    toc.append(entry)
  
  return toc

### EOF ###