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

from bitstring import BitStream, ConstBitStream

GIM_MAGIC       = ConstBitStream(hex='0x4D49472E') # MIG.
GIM_SIZE_OFFSET = 0x14
# The size in the GIM excludes the first 0x10 bytes of the
# header, so we have to include them to get the whole thing.
GIM_SIZE_DIFF   = 0x10

GMO_MAGIC       = ConstBitStream(hex='0x4F4D472E') # OMG.
GMO_SIZE_OFFSET = 0x14
# The size in the GMO excludes the first 0x18 bytes of the
# header, so we have to include them to get the whole thing.
GMO_SIZE_DIFF   = 0x18

################################################################################
### A very simplified GMO parser, just intended to provide access
### to the GIM textures inside a model.
################################################################################
class GmoFile():
  def __init__(self, data = None, offset = 0, filename = None):
    self.data = None
    self.__gim_files = []
    
    if not data == None:
      self.load_data(data, offset)
    elif not filename == None:
      self.load_file(filename)
  
  def load_file(self, filename):
    data = BitStream(filename = filename)
    self.load_data(data)
  
  def load_data(self, data, offset = 0):
    if not data[offset * 8 : offset * 8 + GMO_MAGIC.len] == GMO_MAGIC:
      print "GMO header not found at 0x%04X." % offset
      return
    
    data.bytepos = offset + GMO_SIZE_OFFSET
    gmo_size = data.read("uintle:32") + GMO_SIZE_DIFF
    
    self.data = BitStream(data[offset * 8 : (offset + gmo_size) * 8])
    
    self.__find_gims()
  
  def save(self, filename):
    with open(filename, "wb") as f:
      self.data.tofile(f)
  
  def __find_gims(self):
    if self.data == None:
      return
    
    self.__gim_files = []
    
    for gim_start in self.data.findall(GIM_MAGIC, bytealigned = True):
      gim_size_pos  = gim_start + (GIM_SIZE_OFFSET * 8) # Bit pos.
      gim_size      = self.data[gim_size_pos : gim_size_pos + 32].uintle + GIM_SIZE_DIFF
      
      # And turn it into a byte position.
      gim_start /= 8
      self.__gim_files.append((gim_start, gim_size))
  
  def gim_count(self):
    return len(self.__gim_files)
  
  def get_gim(self, gim_id):
    if gim_id >= self.gim_count():
      print "Invalid GIM ID."
      return None
    
    gim_start, gim_size = self.__gim_files[gim_id]
    gim_data = self.data[gim_start * 8 : (gim_start + gim_size) * 8]
    
    return gim_data
  
  def replace_gim_file(self, gim_id, filename):
    gim_data = BitStream(filename = filename)
    self.replace_gim(gim_id, gim_data)
  
  def replace_gim(self, gim_id, gim_data):
    if gim_id >= self.gim_count():
      print "Invalid GIM ID."
      return
    
    gim_start, gim_size = self.__gim_files[gim_id]
    
    if gim_data.len / 8 > gim_size:
      print "GIM too large. %d bytes > %d bytes" % (gim_data.len / 8, gim_size)
      return
    
    self.data.overwrite(gim_data, gim_start * 8)
    
    # Leave the length alone, though, because we know we have that much space
    # to work with from the original GIM file that was there, and there's no
    # point in shrinking that down if someone happens to want to re-replace
    # this GIM file without reloading the whole thing.

if __name__ == "__main__":
  gmo = GmoFile(filename = "X:\\Danganronpa\\Danganronpa_BEST\\umdimage2-sfx-tex\\bg_160.pak\\0007.gmo")
  gim = gmo.get_gim(4)
  gmo.replace_gim_file(4,  "X:\\Danganronpa\\Danganronpa_BEST\\image-editing\\Models\\!done\\0166_bg_160.pak\\0007\\0004-2-fs8.gim")
  gmo.replace_gim_file(24, "X:\\Danganronpa\\Danganronpa_BEST\\image-editing\\Models\\!done\\0166_bg_160.pak\\0007\\0024-2-fs8.gim")
  gmo.replace_gim_file(25, "X:\\Danganronpa\\Danganronpa_BEST\\image-editing\\Models\\!done\\0166_bg_160.pak\\0007\\0025-2-fs8.gim")
  gmo.replace_gim_file(26, "X:\\Danganronpa\\Danganronpa_BEST\\image-editing\\Models\\!done\\0166_bg_160.pak\\0007\\0026-2-fs8.gim")
  gmo.replace_gim_file(27, "X:\\Danganronpa\\Danganronpa_BEST\\image-editing\\Models\\!done\\0166_bg_160.pak\\0007\\0027-2-fs8.gim")
  gmo.replace_gim_file(28, "X:\\Danganronpa\\Danganronpa_BEST\\image-editing\\Models\\!done\\0166_bg_160.pak\\0007\\0028-2-fs8.gim")
  
  gmo.save("debug/test.gmo")
  with open("debug/test.gim", "wb") as f:
    gim.tofile(f)
  
  from gim_to_png import GimConverter
  gimconv = GimConverter()
  gimconv.convert("debug/test.gim", "debug/test.png")
  
  print gmo.gim_count()

### EOF ###