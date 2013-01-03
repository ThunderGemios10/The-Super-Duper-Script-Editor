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

import bitstring
from bitstring import BitStream, ConstBitStream
import os.path

WRD_HEADER     = ConstBitStream(hex='0x7000')
WRD_SHOW_TEXT  = ConstBitStream(hex='0x7002')
WRD_END_TEXT   = ConstBitStream(hex='0x703B703A')
WRD_END_MARKER = ConstBitStream(hex='0x703A')

################################################################################
### @fn   insert_line(wrd_file, insert_after)
### @desc Inserts a new line into the .scp.wrd file wrd_file after the line
###       insert_after.
### @retn The modified file's data and the index of the inserted line.
################################################################################
def insert_line(wrd_file, insert_after):
  
  if not os.path.isfile(wrd_file):
    raise Exception("File not found.")
  
  wrd = BitStream(filename = wrd_file)
  
  header = wrd.read(16)
  
  if header != WRD_HEADER:
    raise Exception("Not a valid .wrd file")
  
  num_files = wrd.read('uintle:16')
  
  if num_files == 0:
    raise Exception("No text files referenced in this .wrd file.")
  
  # Zero-indexed means the next index we need = the number of files already here.
  new_line = num_files
  
  # Weirdly, the header uses uintle:16 for the number of files, but the
  # tag to show the text is uintbe:16. *shrug*
  target_line = WRD_SHOW_TEXT + ConstBitStream(uintbe = insert_after, length = 16)
  target_pos = list(wrd.findall(target_line, bytealigned = True))
  
  if len(target_pos) == 0:
    raise Exception("ERROR: Could not insert line %d. Line %d not referenced in this .wrd file." % (new_line, insert_after))
  elif len(target_pos) > 1:
    raise Exception("ERROR: Could not insert line %d. Line %d referenced multiple times in this .wrd file." % (new_line, insert_after))
  
  target_pos = target_pos[0]
  
  # First half of our line tag, to make sure it's not already here.
  to_insert = WRD_SHOW_TEXT + ConstBitStream(uintbe = new_line, length = 16)
  
  if wrd.find(to_insert, bytealigned = True):
    raise Exception("ERROR: Could not insert line %d. Line ID already referenced in this .wrd file." % new_line)
  
  # Second half of our line tag, what we actually need to make it work.
  to_insert = to_insert + WRD_END_TEXT
  
  # Find where we want to put it.
  target_pos = target_pos + target_line.len
  
  # Find the first line-close tag AFTER the line we're looking at.
  target_pos = wrd.find(WRD_END_MARKER, bytealigned = True, start = target_pos)
  
  if not target_pos:
    raise Exception("ERROR: Could not insert line %d. Reference to line %d not closed properly." % (new_line, insert_after))
  
  # Then move to the point just after the end tag.
  target_pos = target_pos[0] + WRD_END_MARKER.len
  
  # Insert our line tag.
  wrd.insert(to_insert, target_pos)
  
  # Fix our file count.
  num_files = ConstBitStream(uintle = new_line + 1, length = 16)
  wrd.overwrite(num_files, 16)
  
  return wrd, new_line

### EOF ###