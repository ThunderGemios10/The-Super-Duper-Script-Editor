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

import ast
import ConfigParser
import os

from collections import defaultdict

try:
  import cPickle as pickle
except:
  import pickle

# import eboot_patch
from eboot_patch import LANG_CFG_ID

DEFAULT_SETTINGS = {
  "auto_expand":        "True",
  "auto_play_bgm":      "True",
  "auto_play_sfx":      "True",
  "auto_play_voice":    "True",
  "backup_dir":         "./!backup",
  "bgm_dir":            "./bgm",
  "build_iso":          "True",
  "changes_dir":        "./!changes",
  "dupes_csv":          "./data/dupes.csv",
  "eboot_orig":         "./EBOOT-ORIG.BIN",
  "eboot_text":         "./data/eboot_text.csv",
  "gfx_dir":            "./data/gfx",
  "highlight_tags":     "True",
  "highlight_terms":    "True",
  "iso_dir":            "./!ISO_EDITED",
  "iso_file":           "./DANGANRONPA_EDITED.iso",
  "last_checked_with":  "./umdimage-orig",
  "last_exported":      "./umdimage2",
  "last_export_target": "./umdimage2-ex",
  "last_font":          "./debug/test.sdse-font",
  "last_imported":      "./!changes",
  "last_import_target": "./!imported",
  "last_opened":        "e00_001_000.lin",
  "log_level":          "Info",
  "mangle_text":        "True",
  "pack_bgm":           "False",
  "pack_umdimage":      "True",
  "pack_umdimage2":     "True",
  "pack_voice":         "False",
  "quick_clt":          "False",
  "similarity_db":      "./data/similarity-db.sql",
  "smart_quotes":       "False",
  "spell_check":        "True",
  "spell_check_lang":   "en_US",
  "terminology":        "X:/My Dropbox/Danganronpa/Terminology.csv",
  "text_repl":          "False",
  "toc":                "./!toc.txt",
  "toc2":               "./!toc2.txt",
  "umdimage2_dir":      "./umdimage2",
  "umdimage_dir":       "./umdimage",
  "voice_dir":          "./voice",
}

CONFIG_DIR      = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILENAME = os.path.join(CONFIG_DIR, "data/config.ini")
PREFS_SECTION   = "PREFS"
HACKS_SECTION   = "HACKS"
TAGS_SECTION    = "TAGS"
REPL_SECTION    = "REPL"

HISTORY_FILE    = os.path.join(CONFIG_DIR, "data/history.bin")
TAGS_FILE       = os.path.join(CONFIG_DIR, "data/tags.bin")
REPL_FILE       = os.path.join(CONFIG_DIR, "data/replacements.bin")

class EditorConfig:
  def __init__(self):
    # So I can keep track of what I have while still
    # making them available for direct access.
    self.__pref_names = set()
    
    # The other sections work just fine as dictionaries.
    self.hacks = defaultdict(bool)
    self.tags = []
    self.repl = []
    
    self.load_config()
  
  ########################################
  ### A few helper functions.
  ########################################
  def add_pref(self, name, val):
    vars(self)[name] = val
    self.__pref_names.add(name)
  
  def has_pref(self, name):
    return name in self.__pref_names
  
  def set_pref(self, name, val, add_new = True):
    if not self.has_pref(name):
      if not add_new:
        raise ValueError
      else:
        self.add_pref(name, val)
    else:
      vars(self)[name] = val
  
  def get_pref(self, name, default = None):
    if not self.has_pref(name):
      if default == None:
        raise ValueError
      else:
        return default
    
    return vars(self)[name]
  
  ########################################
  ### LOAD
  ########################################
  def load_config(self):
    config = ConfigParser.ConfigParser(DEFAULT_SETTINGS)
    config.read(CONFIG_FILENAME)
    
    ########################################
    ### PREFS
    ########################################
    
    # So we can at least pull the defaults.
    if not config.has_section(PREFS_SECTION):
      config.add_section(PREFS_SECTION)
    
    # Got a few boolean values
    to_bool = ["auto_expand", "auto_play_voice", "auto_play_bgm", "auto_play_sfx",
      "highlight_terms", "highlight_tags", "spell_check", "pack_umdimage", "pack_umdimage2", 
      "pack_voice", "pack_bgm", "mangle_text", "smart_quotes", "text_repl", "build_iso",
      "quick_clt"
    ]
    
    # for (name, val) in config.items(PREFS_SECTION):
    for option in config.options(PREFS_SECTION):
      val = None
      
      if option in to_bool:
        val = config.getboolean(PREFS_SECTION, option)
      else:
        val = config.get(PREFS_SECTION, option)
      
      self.add_pref(option, val)
    
    # To migrate the old setting.
    if "auto_play" in vars(self):
      if not "auto_play_voice" in vars(self):
        self.auto_play_voice = self.auto_play
      del self.auto_play
    
    ########################################
    ### HACKS
    ########################################
    
    if config.has_section(HACKS_SECTION):
      options = [option for option in config.options(HACKS_SECTION) if option not in DEFAULT_SETTINGS]
      
      for option in options:
        if option == LANG_CFG_ID:
          self.hacks[option] = config.getint(HACKS_SECTION, option)
        else:
          self.hacks[option] = config.getboolean(HACKS_SECTION, option)
    
    ########################################
    ### TAGS
    ########################################
    
    # Load our tags
    if os.path.isfile(TAGS_FILE):
      with open(TAGS_FILE, "rb") as f:
        self.tags = pickle.load(f)
    else:
      self.tags = []
    
    ########################################
    ### TEXT REPLACEMENT
    ########################################
    
    # Load our text replacements
    if os.path.isfile(REPL_FILE):
      with open(REPL_FILE, "rb") as f:
        self.repl = pickle.load(f)
    else:
      self.repl = []
    
    ########################################
    ### HISTORY
    ########################################
    
    # Load our last-viewed-file history.
    if os.path.isfile(HISTORY_FILE):
      with open(HISTORY_FILE, "rb") as f:
        self.last_file = pickle.load(f)
    else:
      self.last_file = {}
  
  ########################################
  ### SAVE
  ########################################
  def save_config(self):
    with open(CONFIG_FILENAME, "w") as outfile:
    
      config = ConfigParser.ConfigParser()
      
      to_output = [
        # -section-     -items-           -source-
        (PREFS_SECTION, self.__pref_names, vars(self)),
        (HACKS_SECTION, self.hacks.keys(), self.hacks),
        # (TAGS_SECTION,  self.tags.keys(),  self.tags),
        # (REPL_SECTION,  self.repl.keys(),  self.repl),
      ]
      
      for (section, items, source) in to_output:
        config.add_section(section)
        
        for item in sorted(items):
          config.set(section, item, str(source[item]))
      
      config.write(outfile)
    
    binary_files = [
      # -file-        -var-
      (TAGS_FILE,     self.tags),
      (REPL_FILE,     self.repl),
      (HISTORY_FILE,  self.last_file),
    ]
    
    for filename, var in binary_files:
      with open(filename, "wb") as f:
        pickle.dump(var, f, pickle.HIGHEST_PROTOCOL)

# if __name__ == "__main__":
  # test = EditorConfig()
  # test.hacks["mapcenter"] = True
  # test.add_section("tags")
  # test.tags["iffy"] = (1, "#FF0000")
  # test.save_config()

### EOF ###