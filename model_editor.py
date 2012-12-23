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
from PyQt4.QtGui import QColorDialog, QColor
from ui_modeleditor import Ui_ModelEditor

import glob
import os

import common
import tree

from gmo_file import GmoFile
from model_pak import ModelPak

class ModelEditor(QtGui.QDialog):
  def __init__(self, parent=None):
    super(ModelEditor, self).__init__(parent)
    
    self.ui = Ui_ModelEditor()
    self.ui.setupUi(self)
    self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    
    self.ui.btnExtract.addAction(self.ui.actionExtractSelected)
    self.ui.btnExtract.addAction(self.ui.actionExtractUnique)
    self.ui.btnExtract.addAction(self.ui.actionExtractAll)
    
    self.ui.btnImport.addAction(self.ui.actionImportTexture)
    self.ui.btnImport.addAction(self.ui.actionImportGMO)
    self.ui.btnImport.addAction(self.ui.actionImportFull)
    
    # self.ui.lblTexture.setPixmap(QtGui.QPixmap("X:/Danganronpa/Danganronpa_BEST/image-editing/umdimage2-base-clean/bg_051.pak/bg_051_p00/0006.png"))
    self.ui.lblTexture.setPixmap(QtGui.QPixmap("X:/Danganronpa/Danganronpa_BEST/image-editing/umdimage2-base/bg_222.pak/bg_217_p00/0000.png"))
    
    # self.ui.chkScaleTex.clicked.connect(lambda: self.ui.lblTexture.setScaledContents(self.ui.chkScaleTex.isChecked()))
    
    self.cur_color = QColor(240, 240, 240)
    self.model_paks = {}
    self.cur_pak = None
    
    self.populate_tree()
  
  def populate_tree(self):
    
    self.ui.treePaks.clear()
    self.ui.treeModels.clear()
    
    self.cur_pak = None
    
    for model_pak in glob.iglob(os.path.join(common.editor_config.umdimage2_dir, "bg_*.pak")):
      # basename = os.path.basename(model_pak)
      # model = ModelPak(model_pak)
      # items = [tree.path_to_tree(os.path.join(basename, name)) for name in model.get_names()]
      # tree_items.extend(items)
      model_pak = tree.path_to_tree(os.path.basename(model_pak))
      self.ui.treePaks.addTopLevelItem(model_pak)
    
    # tree_items = tree.consolidate_tree_items(tree_items)
    # self.ui.treeModels.addTopLevelItems(tree_items)
  
  def model_pak_selected(self, tree_item):
    self.ui.treeModels.clear()
    
    pak_name = tree.tree_item_to_path(tree_item)
    if not pak_name in self.model_paks:
      self.model_paks[pak_name] = ModelPak(os.path.join(common.editor_config.umdimage2_dir, pak_name))
    
    model_pak = self.model_paks[pak_name]
    
    for i in range(model_pak.gmo_count()):
      name = model_pak.get_name(i)
      gmo  = model_pak.get_gmo(i)
      
      tree_item = QtGui.QTreeWidgetItem()
      tree_item.setText(0, name)
      tree_item.setData(0, Qt.Qt.UserRole, i)
      
      for j in range(gmo.gim_count()):
        gim_name = "%04d.gim" % j
        gim_item = QtGui.QTreeWidgetItem()
        gim_item.setText(0, gim_name)
        gim_item.setData(0, Qt.Qt.UserRole, j)
        
        tree_item.addChild(gim_item)
      
      self.ui.treeModels.addTopLevelItem(tree_item)
    
    self.cur_pak = pak_name
  
  def texture_selected(self, tree_item):
    if not self.cur_pak:
      return
    
    
  
  def set_background_color(self):
    
    color = QColorDialog.getColor(self.cur_color, self)
    
    if color.isValid():
      self.cur_color = color
      self.ui.lblTexture.setStyleSheet("background-color: %s;" % color.name())
    
  def clear_background_color(self):
    self.ui.lblTexture.setStyleSheet("background-color: none;")
  
  ##############################################################################
  ### @fn   accept()
  ### @desc Overrides the Save button.
  ##############################################################################
  def accept(self):
    super(ModelEditor, self).accept()
  
  ##############################################################################
  ### @fn   reject()
  ### @desc Overrides the Cancel button.
  ##############################################################################
  def reject(self):
    super(ModelEditor, self).reject()

if __name__ == '__main__':
  import sys

  app = QtGui.QApplication(sys.argv)
  app.connect(app, QtCore.SIGNAL("lastWindowClosed()"),
              app,
              QtCore.SLOT("quit()")
             )
  
  form = ModelEditor()
  form.show()
  sys.exit(app.exec_())

### EOF ###