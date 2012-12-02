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

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QTextCharFormat, QColor

import enchant
from enchant.checker import SpellChecker
from enchant.tokenize import HTMLChunker

class SpellCheckHighlighter(QtGui.QSyntaxHighlighter):
  def __init__(self, parent = None):
    super(SpellCheckHighlighter, self).__init__(parent)
    
    dict = enchant.DictWithPWL("en_US", "data/dict/enchant.txt")
    self.checker = SpellChecker(dict, chunkers = (HTMLChunker,))
    
    self.format = QTextCharFormat()
    self.format.setUnderlineColor(QColor(255, 0, 0))
    self.format.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)
    
    self.errors = []
  
  def highlightBlock(self, text):
    
    # If there is no previous state, then it's -1, which makes the first line 0.
    # And every line after that increases as expected.
    line = self.previousBlockState() + 1
    self.setCurrentBlockState(line)
    
    # Make sure our error list is long enough to hold this line.
    for i in range(len(self.errors), line + 1):
      self.errors.append([])
    
    self.errors[line] = []
    self.checker.set_text(unicode(text.toUtf8(), "UTF-8"))
    
    for err in self.checker:
      self.setFormat(err.wordpos, len(err.word), self.format)
      self.errors[line].append((err.word, err.wordpos))
  
  def add(self, word):
    self.checker.add(word)
    self.rehighlight()
  
  def ignore(self, word):
    self.checker.ignore_always(word)
    self.rehighlight()

### EOF ###