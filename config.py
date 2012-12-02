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

import ast
import ConfigParser
import os

try:
  import cPickle as pickle
except:
  import pickle

DEFAULT_SETTINGS = {
  "iso_dir":            "./!ISO_EDITED",
  "iso_file":           "./DANGANRONPA_EDITED.iso",
  "umdimage_dir":       "./umdimage",
  "umdimage2_dir":      "./umdimage2",
  "eboot_orig":         "./EBOOT-ORIG.BIN",
  "toc":                "./!toc.txt",
  "toc2":               "./!toc2.txt",
  "voice_dir":          "./voice",
  "bgm_dir":            "./bgm",
  "changes_dir":        "./!changes",
  "backup_dir":         "./!backup",
  "terminology":        "X:/My Dropbox/Danganronpa/Terminology.csv",
  "highlight_terms":    "True",
  "auto_expand":        "True",
  "auto_play_voice":    "True",
  "auto_play_bgm":      "True",
  "last_opened":        "e00_001_000.lin",
  "last_imported":      "./!changes",
  "last_import_target": "./!imported",
  "last_checked_with":  "./umdimage-orig",
}

CONFIG_DIR      = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILENAME = os.path.join(CONFIG_DIR, "config.ini")
DEFAULT_SECTION = "DEFAULT"

HISTORY_FILE    = os.path.join(CONFIG_DIR, "data/history.bin")

class EditorConfig:
  def __init__(self):
    self.load_config()
  
  def load_config(self):
    config = ConfigParser.ConfigParser(DEFAULT_SETTINGS)
    config.read(CONFIG_FILENAME)
    
    for item in DEFAULT_SETTINGS.keys():
      vars(self)[item] = config.get(DEFAULT_SECTION, item)
    
    # Got a couple non-strings
    self.highlight_terms  = ast.literal_eval(self.highlight_terms)
    self.auto_expand      = ast.literal_eval(self.auto_expand)
    self.auto_play_voice  = ast.literal_eval(self.auto_play_voice)
    self.auto_play_bgm    = ast.literal_eval(self.auto_play_bgm)
    
    # To migrate the old setting.
    if config.has_option(DEFAULT_SECTION, "auto_play"):
      self.auto_play_voice = ast.literal_eval(config.get(DEFAULT_SECTION, "auto_play"))
    
    # Load our last-viewed-file history.
    if os.path.isfile(HISTORY_FILE):
      f = open(HISTORY_FILE, "rb")
      self.last_file = pickle.load(f)
      f.close()
    else:
      self.last_file = {}
  
  def save_config(self):
    outfile = open(CONFIG_FILENAME, "w")
    
    config = ConfigParser.ConfigParser()
    
    for item in DEFAULT_SETTINGS.keys():
      config.set(DEFAULT_SECTION, item, str(vars(self)[item]))
    
    config.write(outfile)
    
    outfile.close()
    
    # Load our last-opened history.
    f = open(HISTORY_FILE, "wb")
    pickle.dump(self.last_file, f)
    f.close()

### EOF ###