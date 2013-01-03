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

from csv import DictReader, DictWriter
import os

import common

class Term():
  def __init__(self, word = "", meaning = "", section = ""):
    self.word    = word
    self.meaning = meaning
    self.section = section

def load_csv():
  terminology_csv = DictReader(open(common.editor_config.terminology, 'rb'))
  return terminology_csv

def save_csv(rows):
  
  out_rows = []
  
  for row in rows:
    if not row in out_rows:
      out_rows.append(row)
  
  field_names = ['Section', 'Word', 'Meaning']
  
  terminology_csv = DictWriter(open(common.editor_config.terminology, 'wb'), fieldnames = field_names)
  terminology_csv.writerow({x:x for x in field_names})
  terminology_csv.writerows(out_rows)

def last_edited():
  file_stats = os.stat(common.editor_config.terminology)
  return file_stats.st_mtime

def add_term(section, term):
  
  section = str(section)#.title()
  
  new_row = {'Section': section, 'Word': term.word, 'Meaning': term.meaning}
  
  rows = load_csv()
  out_rows = []
  
  for row in rows:
    out_rows.append(row)
  
  if not new_row in out_rows:
    out_rows.append(new_row)
  
  save_csv(out_rows)

def replace_term(section, old_term, new_term):
  
  section = str(section)#.title()
  
  old_row = {'Section': section, 'Word': old_term.word, 'Meaning': old_term.meaning}
  new_row = {'Section': section, 'Word': new_term.word, 'Meaning': new_term.meaning}
  
  rows = load_csv()
  out_rows = []
  
  for row in rows:
    if row == old_row:
      row = new_row
    out_rows.append(row)
  
  save_csv(out_rows)

def remove_term(section, term):
  
  section = str(section)#.title()
  
  to_kill = {'Section': section, 'Word': term.word, 'Meaning': term.meaning}
  
  rows = load_csv()
  out_rows = []
  
  for row in rows:
    if not row == to_kill:
      out_rows.append(row)
  
  save_csv(out_rows)

def rename_section(oldname, newname):
  
  newname = str(newname)#.title()
  oldname = str(oldname)#.title()
  
  rows = load_csv()
  out_rows = []
  renamed_rows = []
  
  for row in rows:
    if row['Section'] == oldname:
      row['Section'] = newname
    
    out_rows.append(row)
  
  save_csv(out_rows)

def remove_section(section):
  
  section = str(section)#.title()
  
  rows = load_csv()
  out_rows = []
  
  for row in rows:
    if not row['Section'] == section:
      out_rows.append(row)
  
  save_csv(out_rows)

def section_exists(section):
  
  section = str(section)#.title()
  
  rows = load_csv()
  out_rows = []
  
  for row in rows:
    if row['Section'] == section:
      return True
  
  return False

def term_exists(section, term):
  
  section = str(section)#.title()
  to_find = {'Section': section, 'Word': term.word, 'Meaning': term.meaning}
  
  rows = load_csv()
  out_rows = []
  
  for row in rows:
    if row == to_find:
      return True
  
  return False

### EOF ###