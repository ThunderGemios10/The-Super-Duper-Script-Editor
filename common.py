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
import re

from config import EditorConfig

SCENE_MODES   = Enum("normal", "trial", "rules", "ammo", "ammoname", "ammosummary", "present", "presentname", "debate", "mtb", "climax", "anagram", "menu", "map", "report", "report2", "skill", "skill2", "music", "eventname", "moviename", "theatre", "help", "other")
SCENE_SPECIAL = Enum("option", "showopt", "react", "debate", "chatter", "checkobj")
BOX_COLORS    = Enum("orange", "green", "blue")
BOX_TYPES     = Enum("normal", "flat")

CHAPTER_MONOKUMA = 9
CHAPTER_FREETIME = 10

CHAR_IDS = {
  0x00 : u"Makoto Naegi",
  0x01 : u"Kiyotaka Ishimaru",
  0x02 : u"Byakuya Togami",
  0x03 : u"Mondo Oowada",
  0x04 : u"Leon Kuwata",
  0x05 : u"Hifumi Yamada",
  0x06 : u"Yasuhiro Hagakure",
  0x07 : u"Sayaka Maizono",
  0x08 : u"Kyouko Kirigiri",
  0x09 : u"Aoi Asahina",
  0x0A : u"Touko Fukawa",
  0x0B : u"Sakura Oogami",
  0x0C : u"Celestia Ludenberg",
  0x0D : u"Junko Enoshima",
  0x0E : u"Chihiro Fujisaki",
  0x0F : u"Monokuma",
  0x10 : u"Junko Enoshima (黒幕)",
  0x11 : u"Alter Ego",
  0x12 : u"Genocider Shou",
  0x13 : u"The Principal",
  0x14 : u"Naegi's Mother",
  0x15 : u"Naegi's Father",
  0x16 : u"Naegi's Little Sister",
  #0x17 : u"",
  0x18 : u"Ishimaru + Oowada",
  0x19 : u"Daia Oowada",
  #0x1A : u"",
  #0x1B : u"",
  #0x1C : u"",
  #0x1D : u"",
  0x1E : u"???",
  0x1F : u"Narration",
}

editor_config     = EditorConfig()

RE_DIRNAME = re.compile(ur".*?e(?P<chapter>\d\d)_(?P<scene>\d\d\d)_(?P<room>\d\d\d)\.lin", re.I)
RE_SYSDIR  = re.compile(ur"(?P<index>\d\d)_(?P<name>.*?)\.pak", re.I)

def get_dir_info(directory):

  dir_info = RE_DIRNAME.match(directory)
  sys_info = RE_SYSDIR.match(directory)
  
  chapter = -1
  scene = -1
  room = -1
  mode = SCENE_MODES.other
  
  if not dir_info == None:
    chapter, scene, room = dir_info.group("chapter", "scene", "room")
    chapter = int(chapter)
    scene = int(scene)
    room = int(room)
    
    # Misc text.
    if chapter == 8:
      
      if scene == 0:
        mode = SCENE_MODES.theatre
        chapter = CHAPTER_MONOKUMA
        # Because the "room" portion of the directory name actually distinguishes
        # between different Monokuma Theatre events, so it makes more sense to
        # refer to that as the "scene" than the "room"
        scene = room
        room = 0
      
      elif scene >= 1 and scene <= 15:
        mode = SCENE_MODES.normal
        chapter = CHAPTER_FREETIME
        scene = 0
        room = 0
      
      else:
        mode = SCENE_MODES.normal
        chapter = -1
        scene = 0
        room = 0
    
    else:
    
      if chapter == 5 and scene in [153, 154]:
        mode = SCENE_MODES.normal
        room = 207
        
      #if (scene >= 100 and scene < 200) or (chapter in [1, 2] and scene in [200, 201]):
      elif scene >= 100 and scene < 200:
        if room == 0:
          mode = SCENE_MODES.trial
        elif room == 1:
          mode = SCENE_MODES.debate
        room = 216 + chapter # Courtroom, lol
        
      elif scene == 255:
        mode = SCENE_MODES.normal
        room = 0
        
      else:
        mode = SCENE_MODES.normal
  
  elif not sys_info == None:
  
    index, name = sys_info.group("index", "name")
    name = name.lower()
    
    chapter = -1
    scene = -1
    room = -1
    
    if name in ["kotodamadesc1", "kotodamadesc2", "kotodamadesc3"]:
      mode = SCENE_MODES.ammo
      
    elif name == "kotodamaname":
      mode = SCENE_MODES.ammoname
    
    elif name == "itemdescription":
      mode = SCENE_MODES.present
      
    elif name == "itemname":
      mode = SCENE_MODES.presentname
    
    elif name == "rule":
      mode = SCENE_MODES.rules
    
    elif name == "report":
      mode = SCENE_MODES.report
    
    elif name in ["special", "skilldeschb"]:
      mode = SCENE_MODES.report2
    
    elif name == "skilldesc":
      mode = SCENE_MODES.skill
    
    elif name == "skillname":
      mode = SCENE_MODES.skill2
    
    elif name in ["floorname", "mapname"]:
      mode = SCENE_MODES.map
    
    elif name == "eventname":
      mode = SCENE_MODES.eventname
    
    elif name == "moviename":
      mode = SCENE_MODES.moviename
    
    elif name == "bgmname":
      mode = SCENE_MODES.music
    
    elif name == "operatesysr":
      mode = SCENE_MODES.help
    
    elif name in ["system", "contents", "briefing", "credit"]:
      mode = SCENE_MODES.other
    
    else:
      mode = SCENE_MODES.menu
  
  elif directory[:5] == "mtb_s":
    chapter = -1
    scene = -1
    room = 203 # Courtroom, lol
    mode = SCENE_MODES.mtb
    
  elif directory[:7] == "anagram":
    chapter = -1
    scene = -1
    room = 203 # Courtroom, lol
    mode = SCENE_MODES.anagram
  
  elif directory[:7] == "nonstop":
    chapter = -1
    scene = -1
    room = 203 # Courtroom, lol
    mode = SCENE_MODES.debate
  
  elif directory[:10] == "script_pak":
    chapter = -1
    scene = -1
    room = 0
    mode = SCENE_MODES.normal
  
  return chapter, scene, room, mode

def mode_to_text(scene_mode):
  
  text = ""
  
  if scene_mode == SCENE_MODES.normal:
    text = "Normal"
  elif scene_mode == SCENE_MODES.trial:
    text = "Class Trial"
  elif scene_mode == SCENE_MODES.rules:
    text = "Rules"
  elif scene_mode in [SCENE_MODES.ammo, SCENE_MODES.ammoname, SCENE_MODES.present, SCENE_MODES.presentname]:
    text = "Ammunition/Presents"
  elif scene_mode == SCENE_MODES.debate:
    text = "Nonstop Debate"
  elif scene_mode == SCENE_MODES.mtb:
    text = "Machinegun Talk Battle"
  elif scene_mode == SCENE_MODES.climax:
    text = "Climax Logic"
  elif scene_mode == SCENE_MODES.anagram:
    text = "Epiphany Anagram"
  elif scene_mode == SCENE_MODES.menu:
    text = "Menu"
  elif scene_mode == SCENE_MODES.map:
    text = "Room/Item Names"
  elif scene_mode == SCENE_MODES.report or scene_mode == SCENE_MODES.report2:
    text = "Report Cards"
  elif scene_mode == SCENE_MODES.skill or scene_mode == SCENE_MODES.skill2:
    text = "Skills"
  elif scene_mode == SCENE_MODES.music:
    text = "Sound Test"
  elif scene_mode == SCENE_MODES.eventname or scene_mode == SCENE_MODES.moviename:
    text = "Event/Movie Gallery"
  elif scene_mode == SCENE_MODES.help:
    text = "Help"
  elif scene_mode == SCENE_MODES.other:
    text = "Other"
  else:
    text = "N/A"
  
  return text
  
def chapter_to_text(chapter):

  text = ""
  
  if chapter == 0:
    text = "Prologue"
  elif chapter >= 1 and chapter <= 6:
    text = "Chapter %d" % chapter
  elif chapter == 7:
    text = "Epilogue"
  elif chapter == CHAPTER_MONOKUMA:
    text = "Monokuma Theatre"
    #text = u"モノクマ劇場"
    #text = "M. Theatre"
  elif chapter == CHAPTER_FREETIME:
    text = "Free Time"
  elif chapter == -1 or chapter == None:
    text = "N/A"
  else:
    text = "Other"
  
  return text

### EOF ###