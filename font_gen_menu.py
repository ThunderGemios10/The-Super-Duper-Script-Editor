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

from PyQt4 import Qt, QtGui, QtCore
from ui_fontgenerator import Ui_FontGenerator

# import common
from font_gen_widget import FontGenWidget

class FontGenMenu(QtGui.QDialog):
  def __init__(self, parent=None):
    super(FontGenMenu, self).__init__(parent)
    
    self.ui = Ui_FontGenerator()
    self.ui.setupUi(self)
    self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    
    self.add_tab()
  
  def add_tab(self):
    self.ui.tabFonts.addTab(FontGenWidget(), "Subfont")
  
  def remove_tab(self):
    answer = QtGui.QMessageBox.warning(
      self,
      "Remove Tab",
      "Are you sure you want to remove this tab?\n\n" +
      "This action cannot be undone. Proceed?",
      buttons = QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
      defaultButton = QtGui.QMessageBox.No
    )
    
    if answer == QtGui.QMessageBox.No:
      return
    
    self.ui.tabFonts.removeTab(self.ui.tabFonts.currentIndex())
  
  def generate_font(self):
    pass

if __name__ == '__main__':
  import sys

  app = QtGui.QApplication(sys.argv)
  app.connect(app, QtCore.SIGNAL("lastWindowClosed()"),
              app,
              QtCore.SLOT("quit()")
             )
  
  form = FontGenMenu()
  form.show()
  sys.exit(app.exec_())

### EOF ###