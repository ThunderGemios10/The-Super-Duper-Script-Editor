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

import os

# import mecab_parser
import re
from text_files import load_text, save_text
from scene_info import SceneInfo

# Some regexes for our enjoyment.
LINE_BREAKS = re.compile(ur"\r\n?", re.UNICODE | re.DOTALL)
TEXT_PARSER = re.compile(ur"([^\u0000\u0001]+)[\u0000\u0001]+[\n\r]*([^\[]+)?[\n\r]*(\[(.+)\])?", re.UNICODE | re.DOTALL)
TAG_KILLER  = re.compile(ur"\<CLT\>|\<CLT (?P<CLT_INDEX>\d+)\>|<DIG.*?>", re.UNICODE | re.DOTALL)

class ScriptFile():
  def __init__(self, filename = None, scene_info = None):
    self.translated = ""
    self.translated_notags = ""
    self.original = ""
    self.original_notags = ""
    self.comments = ""
    
    self.filename = None
    
    if not filename == None:
      self.open(filename)
    
      if scene_info == None:
        # Squeeze the file ID out of the filename.
        scene_info = SceneInfo(file_id = int(os.path.splitext(os.path.basename(filename))[0]))
    
    self.scene_info = scene_info
  
  def open(self, filename):
    
    if not filename or not os.path.isfile(filename):
      return
    
    text = load_text(filename)
    
    self.from_data(text)
    
    self.filename = filename
  
  def from_data(self, data):
    
    self.filename = None
    self.translated = ""
    self.translated_notags = ""
    self.original = ""
    self.original_notags = ""
    self.comments = ""
    
    # Sanitize our line-breaks. The game handles \r\n in some instances,
    # but not all. It always handles \n properly.
    text = LINE_BREAKS.sub("\n", data)
    
    match = TEXT_PARSER.search(text)
    
    if match:
      # Remove any trailing linebreaks, because 
      first_part = match.group(1)
      second_part = match.group(2)
      third_part = match.group(4)
      
      if not second_part:
        self.original = first_part
      else:
        self.translated = first_part
        self.original = second_part
      
      if third_part:
        self.comments = third_part
    
    self.original_notags = TAG_KILLER.sub("", self.original)
    self.translated_notags = TAG_KILLER.sub("", self.translated)
  
  ##############################################################################
  ### @fn    pack()
  ### @desc  Converts all the data into the script file format.
  ### @param for_game -- Whether to include the original, untranslated data.
  ###                    True = exclude untranslated, since we don't need it.
  ##############################################################################
  def pack(self, for_game = False):
  
    if self.translated == "":
      output = u"\ufeff" + self.original + u"\u0000"
      
      if self.comments != "" and not for_game:
        output += "\n[" + self.comments + "]"
    else:
      output = u"\ufeff" + self.translated + u"\u0000"
      
      if not for_game:
        output +=  "\n" + self.original
        if self.comments != "":
          # We want a newline, but not a thousand.
          if not self.original[-1] == '\n':
            output += "\n"
          
          output += "[" + self.comments + "]"
    
    # Sanitize our line breaks, just in case.
    output = LINE_BREAKS.sub("\n", output)
    
    return output
  
  def save(self, filename = None):
    
    if filename == None:
      if self.filename == None:
        return
      else:
        filename = self.filename
    
    output = self.pack(for_game = False)
    
    save_text(output, filename)

### EOF ###