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

import os

VOICE_OFFSETS = {
  # Naegi
  0x00: {0x63: 1107, 0x01:    0, 0x02:  146, 0x03:  321, 0x04:  543, 0x05:  727, 0x06:  860},
  # Ishimaru
  0x01: {0x63: 1304, 0x01: 1214, 0x02: 1242},
  # Togami
  0x02: {0x63: 1995, 0x01: 1383, 0x02: 1402, 0x03: 1520, 0x04: 1627, 0x05: 1769, 0x06: 1895},
  # Oowada
  0x03: {0x63: 2126, 0x01: 2057, 0x02: 2082},
  # Leon
  0x04: {0x63: 2250, 0x01: 2183},
  # Yamada
  0x05: {0x63: 2405, 0x01: 2315, 0x02: 2353},
  # Hagakure
  0x06: {0x63: 2953, 0x01: 2512, 0x02: 2529, 0x03: 2562, 0x04: 2618, 0x05: 2746, 0x06: 2831},
  # Maizono
  0x07: {0x63: 3039, 0x01: 3029},
  # Kirigiri
  0x08: {0x63: 3684, 0x01: 3087, 0x02: 3185, 0x03: 3247, 0x04: 3324, 0x05: 3477, 0x06: 3561},
  # Asahina
  0x09: {0x63: 4174, 0x01: 3764, 0x02: 3792, 0x03: 3832, 0x04: 3902, 0x05: 4019, 0x06: 4083},
  # Fukawa
  0x0A: {0x63: 4492, 0x01: 4275, 0x02: 4300, 0x03: 6381, 0x04: 4315, 0x05: 4374, 0x06: 4420},
  # Oogami
  0x0B: {0x63: 4720, 0x01: 4588, 0x02: 4613, 0x03: 4649},
  # Celes
  0x0C: {0x63: 5037, 0x01: 4788, 0x02: 4831, 0x03: 4886},
  # Enoshima
  0x0D: {0x63: 5105, 0x01: 5103},
  # Chihiro
  0x0E: {0x63: 5186, 0x01: 5146},
  # Monokuma
  0x0F: {0x63: 5527, 0x01: 5287, 0x02: 5313, 0x03: 5362, 0x04: 5375, 0x05: 5389, 0x06: 5417},
  # Enoshima (黒幕)
  0x10: {0x63: 6260, 0x06: 5875},
  # Alter Ego
  #0x11: {},
  # Genocider Shou
  0x12: {                        0x02: 6302, 0x03: 6381, 0x04: 6418,             0x06: 6456},
  # The Principal
  #0x13: {},
  # Naegi's Mother
  #0x14: {},
  # Naegi's Father
  #0x15: {},
  # Naegi's Little Sister
  #0x16: {},
  # Ishimaru Oowada
  #0x17: {},
  # Daia Oowada
  #0x18: {},
}

class VoiceId():
  def __init__(
    self,
    char_id = -1,
    chapter = -1,
    voice_id = -1
  ):
    self.char_id  = char_id
    self.chapter  = chapter
    self.voice_id = voice_id

def get_voice_file(voice):
  
  if voice.char_id in VOICE_OFFSETS and voice.chapter in VOICE_OFFSETS[voice.char_id]:
    return VOICE_OFFSETS[voice.char_id][voice.chapter] + voice.voice_id - 1
  else:
    return None

### EOF ###