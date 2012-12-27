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
from ui_fontgenwidget import Ui_FontGenWidget

# import common
from font_generator import FontConfig, gen_font

class FontGenWidget(QtGui.QWidget):
  def __init__(self, parent=None):
    super(FontGenWidget, self).__init__(parent)
    
    self.ui = Ui_FontGenWidget()
    self.ui.setupUi(self)
    self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
  
  def get_data(self):
    return FontConfig(
      family    = self.ui.cboFont.currentFont().family(),
      size      = self.ui.spnFontSize.value(),
      weight    = self.ui.spnFontWeight.value(),
      x_offset  = self.ui.spnXOffset.value(),
      y_offset  = self.ui.spnYOffset.value(),
      x_margin  = self.ui.spnXMargin.value(),
      y_margin  = self.ui.spnYMargin.value(),
      chars     = unicode(self.ui.txtChars.toPlainText().toUtf8(), "utf-8"),
      subs      = {u"\t": u'  ', u"…":  u"..."},
    )
  
  def chars_changed(self):
    
    if self.ui.chkAutoRefresh.isChecked():
      self.update_preview()
  
  def font_changed(self):
  
    cursor = self.ui.txtChars.textCursor()
    
    self.ui.txtChars.selectAll()
    self.ui.txtChars.setFontFamily(self.ui.cboFont.currentFont().family())
    self.ui.txtChars.setFontPointSize(self.ui.spnFontSize.value())
    self.ui.txtChars.setFontWeight(self.ui.spnFontWeight.value())
    
    self.ui.txtChars.setTextCursor(cursor)
    if self.ui.chkAutoRefresh.isChecked():
      self.update_preview()
  
  def adv_changed(self):
  
    if self.ui.chkAutoRefresh.isChecked():
      self.update_preview()
  
  def update_preview(self):
    config = self.get_data()
    config.chars = config.chars[:256]
    
    font = gen_font([config], img_width = 256, draw_outlines = self.ui.chkBoundingBoxes.isChecked())
    # font.save("debug/test")
    
    qt_pixmap = QtGui.QPixmap.fromImage(font.trans.copy(0, 0, 256, 256))
    self.ui.lblPreview.setPixmap(qt_pixmap)

if __name__ == '__main__':
  import sys

  app = QtGui.QApplication(sys.argv)
  app.connect(app, QtCore.SIGNAL("lastWindowClosed()"),
              app,
              QtCore.SLOT("quit()")
             )
  
  form = FontGenWidget()
  form.show()
  sys.exit(app.exec_())

### EOF ###