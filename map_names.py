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

import os, codecs
from list_files import list_all_files
from script_file import ScriptFile

import common

def get_map_name(map_id, umdimage = common.editor_config.umdimage_dir):
  dir = os.path.join(umdimage, "18_mapname.pak")
  filename = os.path.join(dir, "%04d.txt" % map_id)
  
  if not os.path.isfile(filename):
    return None
  
  map_file = ScriptFile(filename)
  
  room_name = map_file.translated
  if room_name == "":
    room_name = map_file.original
  
  if room_name == u"※" or room_name == "":
    return None
  
  room_name = room_name.strip()
  
  return room_name

class MapNames():
  def __init__(self, umdimage = common.editor_config.umdimage_dir):
    self.map_names    = {}
    self.untranslated = {}
    
    if not umdimage == None:
      self.load(umdimage)
  
  def keys(self):
    return sorted(self.map_names.keys())
  
  def __getitem__(self, key):
    return self.map_names[key]
  
  def load(self, umdimage):
    dir = os.path.join(umdimage, "18_mapname.pak")
    
    self.map_names.clear()
    
    try:
      files = list_all_files(dir)
    except:
      return
    
    for file in files:
      name = os.path.basename(file)
      index = int(os.path.splitext(name)[0])
      
      script = ScriptFile(file)
      
      room_name = script.translated
      if room_name == "":
        room_name = script.original
      
      if room_name == u"※" or room_name == "":
        continue
      
      self.map_names[index]    = room_name
      self.untranslated[index] = script.original

if __name__ == "__main__":
  map_names = MapNames()
  
  seen = {}
  
  for item in map_names.map_names:
    if not map_names[item] in seen:
      print ("Rooms," + map_names.untranslated[item].strip() + "," + map_names[item].strip()).encode("UTF-8")
      seen[map_names[item]] = True

### EOF ###