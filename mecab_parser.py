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

import MeCab

MECAB_OPTIONS = "-u data/dict/danganronpa.dic"

def get_readings(text):
  tagger = MeCab.Tagger(MECAB_OPTIONS + ' -Oyomi')
  result = tagger.parse(text.encode('utf-8'))
  result = result.decode('utf-8')
  
  return result
  
def get_spaced(text):
  tagger = MeCab.Tagger(MECAB_OPTIONS + ' -Owakati')
  result = tagger.parse(text.encode('utf-8'))
  result = result.decode('utf-8')
  
  return result

if __name__ == "__main__":

  text = u'すももも\nももももものうち'

  print get_readings(text)
  print get_spaced(text)

### EOF ###