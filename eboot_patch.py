################################################################################
### Copyright © 2012-2013 BlackDragonHunt
### Copyright © 2012-2013 /a/nonymous scanlations
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

from bitstring import ConstBitStream, BitStream
# from enum import Enum

import common

NAME    = "name"
ENABLED = "enabled"
CFG_ID  = "cfg_id"
DATA    = "data"
POS     = "pos"
ORIG    = "orig"
PATCH   = "patch"

# LANGUAGES   = [u"Japanese", u"English", u"French", u"Spanish", u"German", u"Italian", u"Dutch", u"Portuguese", u"Russian", u"Korean", u"Traditional Chinese", u"Simplified Chinese"]
LANGUAGES   = [u"日本語", u"English", u"Français", u"Español", u"Deutsch", u"Italiano", u"Nederlands", u"Português", u"Русский", u"한국어", u"繁體中文", u"简体中文"]
LANG_CFG_ID = "sys_menu_lang"

EBOOT_PATCHES = [
  {NAME: "Extend EBOOT", ENABLED: True, CFG_ID: None, DATA:
    [
      {POS: 0x0000002C, ORIG:  ConstBitStream(hex = "0x0300"),     PATCH: ConstBitStream(hex = "0x0400")},
      {POS: 0x00000038, ORIG:  ConstBitStream(hex = "0xA0000000"), PATCH: ConstBitStream(hex = "0xC0000000")},
      {POS: 0x00000040, ORIG:  ConstBitStream(hex = "0x84C70D00"), PATCH: ConstBitStream(hex = "0xA4C70D00")},
      {POS: 0x00000054, ORIG:  ConstBitStream(hex = "0x0000000000000000000000000000000000000000000000000000000000000000"),
                        PATCH: ConstBitStream(hex = "0x010000000097100000BE49000000000000100000001000000700000010000000")},
      {POS: 0x00000078, ORIG:  ConstBitStream(hex = "0x00971000"), PATCH: ConstBitStream(hex = "0x00A71000")},
      {POS: 0x00000098, ORIG:  ConstBitStream(hex = "0xE0331100"), PATCH: ConstBitStream(hex = "0xE0431100")},
    ]
  },
  {NAME: "Swap O/X Buttons", ENABLED: True, CFG_ID: "swap_ox", DATA:
    [
      {POS: 0x0001B404, ORIG:  ConstBitStream(hex = "0x21108000"), PATCH: ConstBitStream(hex = "0x01000224")},
      {POS: 0x0000E2A4, ORIG:  ConstBitStream(hex = "0x0400B18F"), PATCH: ConstBitStream(hex = "0xB07F320A")},
      {POS: 0x001097C0, ORIG:  ConstBitStream(hex = "0x0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"),
                        PATCH: ConstBitStream(hex = "0x0400B18F21202002002025320200A014004031360040313A0040843002008014002031360020313A7B48200A")},
    ]
  },
  {NAME: "Map Label Centering", ENABLED: True, CFG_ID: "map_centering", DATA:
    [
      {POS: 0x000833A0, ORIG:  ConstBitStream(hex = "0x0200144602000146"),
                        PATCH: ConstBitStream(hex = "0x807F320A02001446")},
      {POS: 0x00109700, ORIG:  ConstBitStream(hex = "0x0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"),
                        PATCH: ConstBitStream(hex = "0x1400BF8F1000B4AF8808143CD47594260600F41302000146D40094260300F41300000000BA1C220A1000B48F0D000046897F320A20008046")},
      {POS: 0x00083738, ORIG: ConstBitStream(hex = "0x42060246"), PATCH: ConstBitStream(hex = "0x42161446")},
      {POS: 0x0008EA34, ORIG: ConstBitStream(hex = "0x84000624"), PATCH: ConstBitStream(hex = "0x8A000624")},
      {POS: 0x0008EA9C, ORIG: ConstBitStream(hex = "0x84000624"), PATCH: ConstBitStream(hex = "0x8A000624")},
      {POS: 0x0008EAD0, ORIG: ConstBitStream(hex = "0x84000624"), PATCH: ConstBitStream(hex = "0x8A000624")},
      {POS: 0x0008EB70, ORIG: ConstBitStream(hex = "0x84000624"), PATCH: ConstBitStream(hex = "0x8A000624")},
      {POS: 0x0008EBD8, ORIG: ConstBitStream(hex = "0x84000624"), PATCH: ConstBitStream(hex = "0x8A000624")},
      {POS: 0x0008EC0C, ORIG: ConstBitStream(hex = "0x84000624"), PATCH: ConstBitStream(hex = "0x8A000624")},
      {POS: 0x0009008C, ORIG: ConstBitStream(hex = "0x84000624"), PATCH: ConstBitStream(hex = "0x8A000624")},
      {POS: 0x00090318, ORIG: ConstBitStream(hex = "0x84000624"), PATCH: ConstBitStream(hex = "0x8A000624")},
      {POS: 0x00090378, ORIG: ConstBitStream(hex = "0x84000624"), PATCH: ConstBitStream(hex = "0x8A000624")},
    ]
  },
  {NAME: "Ammo/Present Menu (Name Positioning)", ENABLED: True, CFG_ID: "ammo_names", DATA:
    [
      {POS: 0x0000AAE4, ORIG: ConstBitStream(hex = "0x02180046"), PATCH: ConstBitStream(hex = "0x01000046")},
      {POS: 0x000DDEDC, ORIG: ConstBitStream(hex = "0x00000343"), PATCH: ConstBitStream(hex = "0x00000443")},
      {POS: 0x00083E54, ORIG: ConstBitStream(hex = "0xC2070246"), PATCH: ConstBitStream(hex = "0xC2171446")},
      {POS: 0x00083C4C, ORIG: ConstBitStream(hex = "0xC2070246"), PATCH: ConstBitStream(hex = "0xC2171446")},
    ]
  },
  {NAME: "Ammo/Present Menu (Line Length)", ENABLED: True, CFG_ID: "ammo_line_len", DATA:
    [
      {POS: 0x00088F58, ORIG: ConstBitStream(hex = "0xC0FFBD27"), PATCH: ConstBitStream(hex = "0x60FFBD27")},
      {POS: 0x0008C130, ORIG: ConstBitStream(hex = "0xC0FFBD27"), PATCH: ConstBitStream(hex = "0x60FFBD27")},
      {POS: 0x00088F8C, ORIG: ConstBitStream(hex = "0x11000B24"), PATCH: ConstBitStream(hex = "0x3D000B24")},
      {POS: 0x0008C164, ORIG: ConstBitStream(hex = "0x11000D24"), PATCH: ConstBitStream(hex = "0x3D000D24")},
    ]
  },
  {NAME: "Ammo/Present Menu (Previews)", ENABLED: True, CFG_ID: "ammo_previews", DATA:
    [
      {POS: 0x0008A2F8, ORIG:  ConstBitStream(hex = "0x1D000224"),
                        PATCH: ConstBitStream(hex = "0xFF000224")},
      {POS: 0x0008A304, ORIG:  ConstBitStream(hex = "0x0F000224"),
                        PATCH: ConstBitStream(hex = "0xFF000224")},
      {POS: 0x0008A31C, ORIG:  ConstBitStream(hex = "0x8128020800300924"),
                        PATCH: ConstBitStream(hex = "0x906F120800000000")},
      {POS: 0x0008A3F4, ORIG:  ConstBitStream(hex = "0x2130A0022A00C7262140600221200000212800002620092421500000750B020C12000B245B27020800000000"),
                        PATCH: ConstBitStream(hex = "0xA07F320EDA005326A07F320E00000000A07F320E00000000000000005B270208000000000000000000000000")},
      {POS: 0x0008D1F0, ORIG:  ConstBitStream(hex = "0x1D000224"),
                        PATCH: ConstBitStream(hex = "0xFF000224")},
      {POS: 0x0008D1FC, ORIG:  ConstBitStream(hex = "0x0F000224"),
                        PATCH: ConstBitStream(hex = "0xFF000224")},
      {POS: 0x0008D21C, ORIG:  ConstBitStream(hex = "0x3F34020800300924"),
                        PATCH: ConstBitStream(hex = "0x986F120800000000")},
      {POS: 0x0008D304, ORIG:  ConstBitStream(hex = "0x2130A0022A00C7262140600221200000212800002620092421500000750B020C12000B24FB31020800000000"),
                        PATCH: ConstBitStream(hex = "0xA07F320EDA005326A07F320E00000000A07F320E0000000000000000FB310208000000000000000000000000")},
      {POS: 0x00109740, ORIG:  ConstBitStream(hex = "0x0000000000000000000000000000000000000000000000000000000000000000"),
                        PATCH: ConstBitStream(hex = "0x0300401200000000CD38220A000000002190540221B000007638220A01003126")},
      {POS: 0x00109760, ORIG:  ConstBitStream(hex = "0x0000000000000000000000000000000000000000000000000000000000000000"),
                        PATCH: ConstBitStream(hex = "0x03004012000000009144220A000000002190540221B000003344220A01003126")},
      {POS: 0x00109780, ORIG:  ConstBitStream(hex = "0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"),
                        PATCH: ConstBitStream(hex = "0xF8FFBD270400BFAF2130A0022A00C726214060022120A003212800002E00092421500000751B220E12000B240000A28F21B0C2020400BF8F0800E0030800BD27")},
    ]
  },
  {NAME: "Ammo/Present Menu (Long File Fix)", ENABLED: True, CFG_ID: "ammo_file_size", DATA:
    [
      {POS: 0x0008C86C, ORIG: ConstBitStream(hex = "0x0000A384"), PATCH: ConstBitStream(hex = "0x0000A394")},
      {POS: 0x0008C128, ORIG: ConstBitStream(hex = "0x0000658402006484"), PATCH: ConstBitStream(hex = "0x0000659402006494")},
      {POS: 0x0008BB64, ORIG: ConstBitStream(hex = "0x0000648402006284"), PATCH: ConstBitStream(hex = "0x0000649402006294")},
    ]
  },
  {NAME: "Ammo/Present Menu (Total Line Limit)", ENABLED: True, CFG_ID: "ammo_line_limit", DATA:
    [
      {POS: 0x0008BB94, ORIG: ConstBitStream(hex = "0x0B108300"), PATCH: ConstBitStream(hex = "0x21108000")},
    ]
  },
  {NAME: "Fix Glyph Height", ENABLED: False, CFG_ID: "glyph_height", DATA:
    [
      {POS: 0x00082F1C, ORIG: ConstBitStream(hex = "0x10001724"), PATCH: ConstBitStream(hex = "0x18001724")},
      {POS: 0x00082F38, ORIG: ConstBitStream(hex = "0x2110E202"), PATCH: ConstBitStream(hex = "0x10004224")},
      {POS: 0x00083010, ORIG: ConstBitStream(hex = "0x10180000"), PATCH: ConstBitStream(hex = "0x00020324")},
    ]
  },
]

def apply_sys_lang(eboot):
  sys_menu_lang = 1
  if LANG_CFG_ID in common.editor_config.hacks:
    sys_menu_lang = common.editor_config.hacks[LANG_CFG_ID]
  
  patch_loc = 0x1B300
  patch = ConstBitStream(uintle = sys_menu_lang, length = 8) + ConstBitStream(hex = "0x000224")
  eboot.overwrite(patch, patch_loc * 8)
  return eboot

def extend_eboot(eboot):

  HEADER_EXTEND_POS   = 0x54
  HEADER_EXTEND_SIZE  = 0x20
  
  NEW_SECTION_POS     = 0x109700
  NEW_SECTION_SIZE    = 4064
  
  ORIG_SIZE           = 1566304
  EXTENDED_SIZE       = ORIG_SIZE + HEADER_EXTEND_SIZE + NEW_SECTION_SIZE
  
  # Already extended, don't need to do it again.
  if eboot.len / 8 == EXTENDED_SIZE:
    return eboot, HEADER_EXTEND_SIZE
  elif eboot.len / 8 != ORIG_SIZE:
    raise ValueError("EBOOT neither matches original size nor extended size. No idea what to do with this.")
  
  eboot.insert(BitStream(length = HEADER_EXTEND_SIZE * 8), HEADER_EXTEND_POS * 8)
  eboot.insert(BitStream(length = NEW_SECTION_SIZE * 8),   NEW_SECTION_POS * 8)
  
  # Since we're adding another program segment between program segments 0 and 1,
  # we need to update references to program segment 1 on the relocation table
  # so that they point to program segment 2.
  #
  # The pseudocode for this step is:
  # 
  # For b = every 8 bytes from 0x1143E0 to the end of the file:
  #   If b[5] == 1, replace it with 2.
  #   If b[6] == 1, replace it with 2.
  TABLE_START = 0x1143E0
  eboot.bytepos = TABLE_START
  
  while True:
    
    eboot.bytepos += 5
    
    if eboot.peek(8) == "0x01":
      eboot.overwrite("0x02")
    else:
      eboot.bytepos += 1
    
    if eboot.peek(8) == "0x01":
      eboot.overwrite("0x02")
    else:
      eboot.bytepos += 1
    
    eboot.bytepos += 1
    
    if eboot.bytepos >= eboot.len / 8:
      break
  
  return eboot, HEADER_EXTEND_SIZE

def apply_eboot_patches(eboot):
  
  eboot, offset = extend_eboot(eboot)
  
  for patch in EBOOT_PATCHES:
  
    enabled = patch[ENABLED]
    if patch[CFG_ID] and patch[CFG_ID] in common.editor_config.hacks:
      enabled = common.editor_config.hacks[patch[CFG_ID]]
    
    # So we can undo patches if they've already been applied.
    key = PATCH if enabled else ORIG
    
    for item in patch[DATA]:
      eboot.overwrite(item[key], item[POS] * 8)
  
  eboot = apply_sys_lang(eboot)
  return eboot, offset

if __name__ == "__main__":
  src = "X:\\Danganronpa\\Danganronpa_BEST\\EBOOT-ORIG.BIN"
  dst = "X:\\Danganronpa\\Danganronpa_BEST\\EBOOT-TEST.BIN"
  test = BitStream(filename = src)
  test, offset = apply_eboot_patches(test)
  with open(dst, "wb") as f:
    test.tofile(f)

### EOF ###