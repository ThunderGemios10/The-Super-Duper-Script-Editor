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

from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtGui import QFileDialog, QProgressDialog
from ui_wizard import Ui_SetupWizard

import os
import shutil
from bitstring import ConstBitStream

import common
from dialog_fns import get_save_file, get_open_file, get_existing_dir
from extract import extract_umdimage, UMDIMAGE_TYPE, extract_pak


UMDIMAGE_DAT    = os.path.join("PSP_GAME", "USRDIR", "umdimage.dat")
UMDIMAGE2_DAT   = os.path.join("PSP_GAME", "USRDIR", "umdimage2.dat")
VOICE_PAK       = os.path.join("PSP_GAME", "USRDIR", "voice.pak")

UMDIMAGE_DIR    = "umdimage"
UMDIMAGE2_DIR   = "umdimage2"
VOICE_DIR       = "voice"
TOC_FILE        = "!toc.txt"
TOC2_FILE       = "!toc2.txt"
CHANGES_DIR     = "!changes"
BACKUP_DIR      = "!backup"
EDITED_ISO_DIR  = "!ISO_EDITED"

class SetupWizard(QtGui.QDialog):
  def __init__(self, parent=None):
    super(SetupWizard, self).__init__(parent)
    
    self.ui = Ui_SetupWizard()
    self.ui.setupUi(self)
    self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    
    self.iso_dir          = None
    self.workspace_dir    = None
    self.eboot_path       = None
    self.terminology_path = None
    
    # Don't really feel like doing all this in Designer.
    self.connect(self.ui.btnIsoBrowse,          QtCore.SIGNAL("clicked()"), self.get_iso)
    self.connect(self.ui.btnIsoOK,              QtCore.SIGNAL("clicked()"), self.check_iso)
    self.connect(self.ui.btnWorkspaceBrowse,    QtCore.SIGNAL("clicked()"), self.get_workspace)
    self.connect(self.ui.btnWorkspaceOK,        QtCore.SIGNAL("clicked()"), self.check_workspace)
    self.connect(self.ui.btnEbootOK,            QtCore.SIGNAL("clicked()"), self.check_eboot)
    self.connect(self.ui.btnSetupWorkspace,     QtCore.SIGNAL("clicked()"), self.setup_workspace)
    self.connect(self.ui.btnWorkspaceSkip,      QtCore.SIGNAL("clicked()"), self.skip_setup)
    self.connect(self.ui.btnCopyGfx,            QtCore.SIGNAL("clicked()"), self.copy_gfx)
    self.connect(self.ui.btnTerminologyNew,     QtCore.SIGNAL("clicked()"), self.create_terminology)
    self.connect(self.ui.btnTerminologyBrowse,  QtCore.SIGNAL("clicked()"), self.get_terminology)
    self.connect(self.ui.btnTerminologyOK,      QtCore.SIGNAL("clicked()"), self.check_terminology)
  
  def show_error(self, message):
    QtGui.QMessageBox.critical(self, "Error", message)
  
  def show_info(self, message):
    QtGui.QMessageBox.information(self, "Info", message)
    
  ##############################################################################
  ### STEP 1
  ##############################################################################
  def get_iso(self):
    dir = get_existing_dir(self, self.ui.txtIso.text())
    if not dir == "":
      self.ui.txtIso.setText(dir)
  
  def check_iso(self):
  
    iso_dir = unicode(self.ui.txtIso.text().toUtf8(), "UTF-8")
    if not os.path.isdir(iso_dir):
      self.show_error("ISO directory does not exist.")
      return
    
    validated = True
    with open("data/file_order.txt", "rb") as file_order:
      # Since we're reappropriating this from the file used by mkisofs,
      # we need to do a little bit of work on it to be useful here.
      # Split it up on the tab, take the first entry, and chop the slash
      # off the beginning so we can use it in os.path.join
      file_list = [line.split('\t')[0][1:] for line in file_order.readlines() if not line == ""]
      
      for filename in file_list:
        full_name = os.path.join(iso_dir, filename)
        if not os.path.isfile(full_name):
          validated = False
          self.show_error("%s missing from ISO directory." % full_name)
          break
    
    if not validated:
      return
    
    self.iso_dir = iso_dir
    self.show_info("ISO directory looks good.")
    self.ui.grpStep1.setEnabled(False)
    self.ui.grpStep2.setEnabled(True)
    
  ##############################################################################
  ### STEP 2
  ##############################################################################
  def get_workspace(self):
    dir = get_existing_dir(self, self.ui.txtWorkspace.text())
    if not dir == "":
      self.ui.txtWorkspace.setText(dir)
  
  def check_workspace(self):
    workspace_dir = unicode(self.ui.txtWorkspace.text().toUtf8(), "UTF-8")
    
    if not os.path.isdir(workspace_dir):
      try:
        os.makedirs(workspace_dir)
        self.show_info("Workspace directory created.")
      except:
        self.show_error("Error creating workspace directory.")
        return
    else:
      self.show_info("Workspace directory already exists.\n\nExisting data will be overwritten.")
    
    self.workspace_dir = workspace_dir
    self.ui.grpStep2.setEnabled(False)
    self.ui.grpStep3.setEnabled(True)
    
  ##############################################################################
  ### STEP 3
  ##############################################################################
  def check_eboot(self):
    eboot_path = os.path.join(self.workspace_dir, "EBOOT.BIN")
    if not os.path.isfile(eboot_path):
      self.show_error("EBOOT.BIN not found in workspace directory.")
      return
    
    eboot = ConstBitStream(filename = eboot_path)
    if not eboot[:32] == ConstBitStream(hex = "0x7F454C46"):
      self.show_error("EBOOT.BIN is encrypted.")
      return
    
    self.eboot_path = eboot_path
    self.show_info("EBOOT.BIN looks good.")
    self.ui.grpStep3.setEnabled(False)
    self.ui.grpStep4.setEnabled(True)
    
  ##############################################################################
  ### STEP 4
  ##############################################################################
  def skip_setup(self):
    
    answer = QtGui.QMessageBox.warning(
      self,
      "Skip Setup",
      "Are you sure you want to skip setting up your workspace?\n\nYou should only do this if you already have a workspace generated by the setup wizard.",
      buttons = QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
      defaultButton = QtGui.QMessageBox.No
    )
    
    if answer == QtGui.QMessageBox.No:
      return
    
    self.ui.grpStep4.setEnabled(False)
    self.ui.grpStep5.setEnabled(True)
  
  def setup_workspace(self):
    umdimage  = os.path.join(self.iso_dir, UMDIMAGE_DAT)
    umdimage2 = os.path.join(self.iso_dir, UMDIMAGE2_DAT)
    voice     = os.path.join(self.iso_dir, VOICE_PAK)
    
    umdimage_dir    = os.path.join(self.workspace_dir, UMDIMAGE_DIR)
    umdimage2_dir   = os.path.join(self.workspace_dir, UMDIMAGE2_DIR)
    voice_dir       = os.path.join(self.workspace_dir, VOICE_DIR)
    toc_file        = os.path.join(self.workspace_dir, TOC_FILE)
    toc2_file       = os.path.join(self.workspace_dir, TOC2_FILE)
    changes_dir     = os.path.join(self.workspace_dir, CHANGES_DIR)
    backup_dir      = os.path.join(self.workspace_dir, BACKUP_DIR)
    edited_iso_dir  = os.path.join(self.workspace_dir, EDITED_ISO_DIR)
    
    # Do the easy stuff first.
    if not os.path.isdir(changes_dir):
      os.makedirs(changes_dir)
    if not os.path.isdir(backup_dir):
      os.makedirs(backup_dir)
    
    # Now, extract our archives.
    # extract_umdimage(umdimage,  out_dir = umdimage_dir,   eboot = self.eboot_path, type = UMDIMAGE_TYPE.best,   toc_filename = toc_file)
    # extract_umdimage(umdimage2, out_dir = umdimage2_dir,  eboot = self.eboot_path, type = UMDIMAGE_TYPE.best2,  toc_filename = toc2_file)
    # extract_pak(voice, out_dir = voice_dir)
    
    # ISO directory needs to not exist for copytree.
    if os.path.isdir(edited_iso_dir):
      shutil.rmtree(edited_iso_dir)
    
    # Give us an ISO directory for the editor to place modified files in.
    shutil.copytree(self.iso_dir, edited_iso_dir)
    
    # Files we want to make blank, because they're unnecessary.
    blank_files = [
      os.path.join(edited_iso_dir, "PSP_GAME", "INSDIR", "UMDIMAGE.DAT"),
      os.path.join(edited_iso_dir, "PSP_GAME", "SYSDIR", "UPDATE", "DATA.BIN"),
      os.path.join(edited_iso_dir, "PSP_GAME", "SYSDIR", "UPDATE", "EBOOT.BIN"),
      os.path.join(edited_iso_dir, "PSP_GAME", "SYSDIR", "UPDATE", "PARAM.SFO"),
    ]
    
    for blank in blank_files:
      with open(blank, "wb") as f:
        pass
    
    # Copy the decrypted EBOOT into the ISO folder so the builder can use it.
    shutil.copy(self.eboot_path, os.path.join(edited_iso_dir, "PSP_GAME", "SYSDIR", "EBOOT.BIN"))
    
    self.ui.grpStep4.setEnabled(False)
    self.ui.grpStep5.setEnabled(True)
    
  ##############################################################################
  ### STEP 5
  ##############################################################################
  def copy_gfx(self):
    self.ui.grpStep5.setEnabled(False)
    self.ui.grpStep6.setEnabled(True)
    
  ##############################################################################
  ### STEP 6
  ##############################################################################
  def create_terminology(self):
    dir = get_save_file(self, self.ui.txtTerminology.text(), filter = "Terminology.csv (*.csv)")
    if not dir == "":
      self.ui.txtTerminology.setText(dir)
  
  def get_terminology(self):
    dir = get_open_file(self, self.ui.txtTerminology.text(), filter = "Terminology.csv (*.csv)")
    if not dir == "":
      self.ui.txtTerminology.setText(dir)
  
  def check_terminology(self):
    self.ui.grpStep6.setEnabled(False)
    self.ui.btnClose.setText("Finish")
  
  ##############################################################################
  ### @fn   accept()
  ### @desc Overrides the OK button.
  ##############################################################################
  def accept(self):
    super(SetupWizard, self).accept()
  
  ##############################################################################
  ### @fn   reject()
  ### @desc Overrides the Cancel button.
  ##############################################################################
  def reject(self):
    super(SetupWizard, self).reject()

if __name__ == '__main__':
  import sys

  app = QtGui.QApplication(sys.argv)
  app.connect(app, QtCore.SIGNAL("lastWindowClosed()"),
              app,
              QtCore.SLOT("quit()")
             )
  
  form = SetupWizard()
  form.show()
  sys.exit(app.exec_())

### EOF ###