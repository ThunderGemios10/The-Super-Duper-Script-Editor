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

from bitstring import ConstBitStream
import logging
import os

import common
from script_pack import ScriptPack
from sprite import SpriteId, SPRITE_TYPE
from voice import VoiceId

_LOGGER_NAME = common.LOGGER_NAME + "." + __name__
_LOGGER = logging.getLogger(_LOGGER_NAME)

MTB_DIR = {
  "hs_mtb_s01.pak": "mtb_s01.pak",
  "hs_mtb_s02.pak": "mtb_s02.pak",
  "hs_mtb_s03.pak": "mtb_s03.pak",
  "hs_mtb_s04.pak": "mtb_s04.pak",
  "hs_mtb_s05.pak": "mtb_s05.pak",
  "hs_mtb_s06.pak": "mtb_s06.pak",
  "hs_mtb_s07.pak": "mtb_s07.pak",
  "hs_mtb_s08.pak": "mtb_s08.pak",
  "hs_mtb_s09.pak": "mtb_s09.pak",
  "hs_mtb_s10.pak": "mtb_s10.pak",
  "hs_mtb_s11.pak": "mtb_s11.pak",
  "hs_mtb_s21.pak": "mtb_s21.pak",
  "hs_mtb_s22.pak": "mtb_s22.pak",
  "hs_mtb_s23.pak": "mtb_s23.pak",
  "hs_mtb_s24.pak": "mtb_s24.pak",
  "hs_mtb_s25.pak": "mtb_s25.pak",
  "hs_mtb_s26.pak": "mtb_s26.pak",
  "hs_mtb_s27.pak": "mtb_s27.pak",
  "hs_mtb_s28.pak": "mtb_s28.pak",
  "hs_mtb_s29.pak": "mtb_s29.pak",
  "hs_mtb_s30.pak": "mtb_s30.pak",
  "hs_mtb_s31.pak": "mtb_s31.pak",
  "hs_mtb_s32.pak": "mtb_s32.pak",
  "hs_mtb_s33.pak": "mtb_s33.pak",
  "hs_mtb_s34.pak": "mtb_s34.pak",
  "hs_mtb_s35.pak": "mtb_s35.pak",
  "hs_mtb_s36.pak": "mtb_s36.pak",
  "hs_mtb_s37.pak": "mtb_s37.pak",
  "hs_mtb_s38.pak": "mtb_s38.pak",
  "hs_mtb_s39.pak": "mtb_s39.pak",
  "hs_mtb_s40.pak": "mtb_s40.pak",
}

class MTBParser():
  def __init__(self):
    self.script_pack = ScriptPack()
    self.filename = ""
  
  def load(self, filename):
    filename = filename.lower()
    
    if not filename in MTB_DIR:
      _LOGGER.error("Invalid MTB file: %s" % filename)
      return
    
    self.filename = filename
    
    script_dir = MTB_DIR[filename]
    self.script_pack = ScriptPack(script_dir, common.editor_config.umdimage_dir)
    
    # --- MTB FORMAT ---
    # 12 bytes     -- ???
    # XX XX XX XX  -- Table offset
    # 24 bytes     -- ???
    # 
    # XX XX        -- MTB Index
    # XX XX        -- Char ID for sprites
    # XX XX        -- Char ID for voices (chapter for voices is 0x63)
    # XX XX        -- Initial sprite ID (?)
    
    mtb = ConstBitStream(filename = os.path.join(common.editor_config.umdimage_dir, self.filename))
    
    mtb.read(12 * 8)
    table_offset = mtb.read("uintle:32")
    mtb.read(24 * 8)
    
    mtb_index   = mtb.read("uintle:16")
    sprite_char = mtb.read("uintle:16")
    voice_char  = mtb.read("uintle:16")
    sprite_id   = mtb.read("uintle:16")
    
    sprite = SpriteId(SPRITE_TYPE.stand, sprite_char, sprite_id)
    
    # --- TABLE FORMAT ---
    # XX XX XX XX -- Number of files
    # 
    # [for each line]
    # XX XX XX XX -- Offset (from table start) of voice info.
    # 
    # -- Voice Info --
    # XX XX -- File ID
    # XX XX -- Voice ID (with char ID above and the chapter ID 0x63, we know which voice file to use)
    
    mtb.bytepos = table_offset
    num_files   = mtb.read("uintle:32")
    
    for i in range(num_files):
      voice_offset = mtb.read("uintle:32")
      
      # Store our position in the table so we can jump back to it.
      table_pos = mtb.bytepos
      mtb.bytepos = table_offset + voice_offset
      
      file_id  = mtb.read("uintle:16")
      voice_id = mtb.read("uintle:16")
      
      # Chapter is 0x63, which is where the non-Trial voice samples are stored,
      # but I don't see the information actually recorded in the MTB files,
      # so I'm magic-numbering it here.
      voice = VoiceId(voice_char, 0x63, voice_id)
      
      self.script_pack[file_id].scene_info.sprite = sprite
      self.script_pack[file_id].scene_info.voice  = voice
      
      # Restore it to our old position.
      mtb.bytepos = table_pos

if __name__ == "__main__":
  
  print "starting"
  parser = MTBParser()
  parser.load("hs_mtb_s10.pak")

### EOF ###