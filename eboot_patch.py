################################################################################
### Copyright © 2012 BlackDragonHunt
### Copyright © 2012 /a/nonymous scanlations
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

LANGUAGES   = [u"Japanese", u"English", u"French", u"Spanish", u"German", u"Italian", u"Dutch", u"Portuguese", u"Russian", u"Korean", u"Traditional Chinese", u"Simplified Chinese"]
# LANGUAGES   = [u"日本語", u"English", u"Français", u"Español", u"Deutsch", u"Italiano", u"Nederlands", u"Português", u"Русский", u"한국어", u"Traditional Chinese", u"Simplified Chinese"]
LANG_CFG_ID = "sys_menu_lang"

EBOOT_PATCHES = [
  {NAME: "Swap O/X Buttons", ENABLED: True, CFG_ID: "swap_ox", DATA:
    [
      {POS: 0x0001B3E4, ORIG: ConstBitStream(hex = "0x21108000"), PATCH: ConstBitStream(hex = "0x01000224")}, # li $v0, 1             ; Home/Save screen button order
      {POS: 0x0000E284, ORIG: ConstBitStream(hex = "0x0400B18F"), PATCH: ConstBitStream(hex = "0x9038240A")}, # j 0x0890E240          ; jump to an arbitrary piece of code that we'll insert
      {POS: 0x0010A300, ORIG: ConstBitStream(hex = "0x00000000"), PATCH: ConstBitStream(hex = "0x0400B18F")}, # lw $s1, 4($sp)        ; Load the results of sceCtrlReadBufferPositive to $s1
      {POS: 0x0010A304, ORIG: ConstBitStream(hex = "0x00000000"), PATCH: ConstBitStream(hex = "0x21202002")}, # addu $a0, $s1, $zr    ; Save $s1 to $a0
      {POS: 0x0010A308, ORIG: ConstBitStream(hex = "0x00000000"), PATCH: ConstBitStream(hex = "0x00202532")}, # andi $a1, $s1, 8192   ; Is the circle bit set in $s1?
      {POS: 0x0010A30C, ORIG: ConstBitStream(hex = "0x00000000"), PATCH: ConstBitStream(hex = "0x0200A014")}, # bne $a1, $zr, 2       ; If so, jump 1 instruction
      {POS: 0x0010A310, ORIG: ConstBitStream(hex = "0x00000000"), PATCH: ConstBitStream(hex = "0x00403136")}, # ori $s1, $s1, 16384   ; But not before setting the cross bit in $s1 (google "delay slot")
      {POS: 0x0010A314, ORIG: ConstBitStream(hex = "0x00000000"), PATCH: ConstBitStream(hex = "0x0040313A")}, # xori $s1, $s1, 16384  ; Unset the cross bit (may be jumped over)
      {POS: 0x0010A318, ORIG: ConstBitStream(hex = "0x00000000"), PATCH: ConstBitStream(hex = "0x00408430")}, # andi $a0, $a0, 16384  ; Is the cross bit set in $a0?
      {POS: 0x0010A31C, ORIG: ConstBitStream(hex = "0x00000000"), PATCH: ConstBitStream(hex = "0x02008014")}, # bne $a0, $zr, 2       ; If so, jump 1 instruction
      {POS: 0x0010A320, ORIG: ConstBitStream(hex = "0x00000000"), PATCH: ConstBitStream(hex = "0x00203136")}, # ori $s1, $s1, 8192    ; But not before setting the circle bit in $s1
      {POS: 0x0010A324, ORIG: ConstBitStream(hex = "0x00000000"), PATCH: ConstBitStream(hex = "0x0020313A")}, # xori $s1, $s1, 8192   ; Unset the circle bit (may be jumped over)
      {POS: 0x0010A328, ORIG: ConstBitStream(hex = "0x00000000"), PATCH: ConstBitStream(hex = "0x7B48200A")}, # j 0x088121EC          ; Jump back to function
    ]
  },
  {NAME: "Map Name Centering", ENABLED: True, CFG_ID: "map_centering", DATA:
    [
      {POS: 0x00083380, ORIG: ConstBitStream(hex = "0x02001446"), PATCH: ConstBitStream(hex = "0x8038240A")}, # j 0x0890E200          ; jump to a arbitrary piece of code
      {POS: 0x00083384, ORIG: ConstBitStream(hex = "0x02000146"), PATCH: ConstBitStream(hex = "0x02001446")}, # mul.s $f0, $f20
      {POS: 0x0010A2C0, ORIG: ConstBitStream(hex = "0x00000000"), PATCH: ConstBitStream(hex = "0x1400BF8F")}, # lw $ra, 20($sp)       ; round the widths of the glyphs down
      {POS: 0x0010A2C4, ORIG: ConstBitStream(hex = "0x00000000"), PATCH: ConstBitStream(hex = "0x1000B4AF")}, # sw $s4, 16($sp)
      {POS: 0x0010A2C8, ORIG: ConstBitStream(hex = "0x00000000"), PATCH: ConstBitStream(hex = "0x8808143C")}, # lui $s4, 0x0888
      {POS: 0x0010A2CC, ORIG: ConstBitStream(hex = "0x00000000"), PATCH: ConstBitStream(hex = "0xD4759426")}, # addiu $s4, $s4, 0x75D4
      {POS: 0x0010A2D0, ORIG: ConstBitStream(hex = "0x00000000"), PATCH: ConstBitStream(hex = "0x0600F413")}, # beq $ra, $s4, 0x0890E22C
      {POS: 0x0010A2D4, ORIG: ConstBitStream(hex = "0x00000000"), PATCH: ConstBitStream(hex = "0x02000146")}, # mul.s $f0, $f1
      {POS: 0x0010A2D8, ORIG: ConstBitStream(hex = "0x00000000"), PATCH: ConstBitStream(hex = "0xD4009426")}, # addiu $s4, $s4, 0xD4
      {POS: 0x0010A2DC, ORIG: ConstBitStream(hex = "0x00000000"), PATCH: ConstBitStream(hex = "0x0300F413")}, # beq $ra, $s4, 0x0890E22C
      {POS: 0x0010A2E0, ORIG: ConstBitStream(hex = "0x00000000"), PATCH: ConstBitStream(hex = "0x00000000")}, # nop
      {POS: 0x0010A2E4, ORIG: ConstBitStream(hex = "0x00000000"), PATCH: ConstBitStream(hex = "0xBA1C220A")}, # j 0x088872E8
      {POS: 0x0010A2E8, ORIG: ConstBitStream(hex = "0x00000000"), PATCH: ConstBitStream(hex = "0x1000B48F")}, # lw $s4, 16($sp)
      {POS: 0x0010A2EC, ORIG: ConstBitStream(hex = "0x00000000"), PATCH: ConstBitStream(hex = "0x0D000046")}, # trunc.w.s $f0, $f0
      {POS: 0x0010A2F0, ORIG: ConstBitStream(hex = "0x00000000"), PATCH: ConstBitStream(hex = "0x8938240A")}, # j 0x0890E224
      {POS: 0x0010A2F4, ORIG: ConstBitStream(hex = "0x00000000"), PATCH: ConstBitStream(hex = "0x20008046")}, # cvt.s.w $f0, $f0
      {POS: 0x00083718, ORIG: ConstBitStream(hex = "0x42060246"), PATCH: ConstBitStream(hex = "0x42161446")}, # mul.s $f25, $f2, $f20 ; make the game stop doing weird shit
      {POS: 0x0008EA14, ORIG: ConstBitStream(hex = "0x84000624"), PATCH: ConstBitStream(hex = "0x8A000624")}, # li $a2, 138           ; make the game use the right center coordinate
      {POS: 0x0008EA7C, ORIG: ConstBitStream(hex = "0x84000624"), PATCH: ConstBitStream(hex = "0x8A000624")}, # li $a2, 138
      {POS: 0x0008EAB0, ORIG: ConstBitStream(hex = "0x84000624"), PATCH: ConstBitStream(hex = "0x8A000624")}, # li $a2, 138
      {POS: 0x0008EB50, ORIG: ConstBitStream(hex = "0x84000624"), PATCH: ConstBitStream(hex = "0x8A000624")}, # li $a2, 138
      {POS: 0x0008EBB8, ORIG: ConstBitStream(hex = "0x84000624"), PATCH: ConstBitStream(hex = "0x8A000624")}, # li $a2, 138
      {POS: 0x0008EBEC, ORIG: ConstBitStream(hex = "0x84000624"), PATCH: ConstBitStream(hex = "0x8A000624")}, # li $a2, 138
      {POS: 0x0009006C, ORIG: ConstBitStream(hex = "0x84000624"), PATCH: ConstBitStream(hex = "0x8A000624")}, # li $a2, 138
      {POS: 0x000902F8, ORIG: ConstBitStream(hex = "0x84000624"), PATCH: ConstBitStream(hex = "0x8A000624")}, # li $a2, 138
      {POS: 0x00090358, ORIG: ConstBitStream(hex = "0x84000624"), PATCH: ConstBitStream(hex = "0x8A000624")}, # li $a2, 138
    ]
  },
  {NAME: "Ammo/Present Menu (Names)", ENABLED: True, CFG_ID: "ammo_names", DATA:
    [
      {POS: 0x0000AAC4, ORIG: ConstBitStream(hex = "0x02180046"), PATCH: ConstBitStream(hex = "0x01000046")}, # sub.s $f0, $f0, $f0   ; stop placing the glyphs in weird manner
      {POS: 0x00083C2C, ORIG: ConstBitStream(hex = "0xC2070246"), PATCH: ConstBitStream(hex = "0xC2171446")}, # mul.s $f31, $f2, $f20 ; stop doing strange things to the center coordinate
      {POS: 0x00083E34, ORIG: ConstBitStream(hex = "0xC2070246"), PATCH: ConstBitStream(hex = "0xC2171446")}, # mul.s $f31, $f2, $f20 ; stop doing strange things to the center coordinate
      {POS: 0x000DDEBC, ORIG: ConstBitStream(hex = "0x00000343"), PATCH: ConstBitStream(hex = "0x00000443")}, # 132.0                 ; fix the center coordinate
    ]
  },
  {NAME: "Ammo/Present Menu (Line Length)", ENABLED: True, CFG_ID: "ammo_line_len", DATA:
    [
      {POS: 0x00088F38, ORIG: ConstBitStream(hex = "0xC0FFBD27"), PATCH: ConstBitStream(hex = "0x60FFBD27")}, # addiu $sp, -0xA0 ; make the game allocate a larger array (presents)
      {POS: 0x0008C110, ORIG: ConstBitStream(hex = "0xC0FFBD27"), PATCH: ConstBitStream(hex = "0x60FFBD27")}, # addiu $sp, -0xA0 ; make the game allocate a larger array (ammo)
      {POS: 0x00088F6C, ORIG: ConstBitStream(hex = "0x11000B24"), PATCH: ConstBitStream(hex = "0x3D000B24")}, # li $t3, 0x3D     ; make the game copy more characters into the array (presents)
      {POS: 0x0008C144, ORIG: ConstBitStream(hex = "0x11000D24"), PATCH: ConstBitStream(hex = "0x3D000D24")}, # li $t5, 0x3D     ; make the game copy more characters into the array (ammo)
    ]
  },
  {NAME: "Ammo/Present Menu (Previews)", ENABLED: True, CFG_ID: "ammo_previews", DATA:
    [
      # Description length limit (presents)
      {POS: 0x0008A2D8, ORIG:  ConstBitStream(hex = "0x1D000224"), 
                        PATCH: ConstBitStream(hex = "0xFF000224")
      },
      # Line length limit (presents)
      {POS: 0x0008A2E4, ORIG:  ConstBitStream(hex = "0x0F000224"), 
                        PATCH: ConstBitStream(hex = "0xFF000224")
      },
      # Newline behavior (presents)
      {POS: 0x0008A2FC, ORIG:  ConstBitStream(hex = "0x8128020800300924"), 
                        PATCH: ConstBitStream(hex = "0x6028040800000000")
      },
      # Painting ellipsis (presents)
      {POS: 0x0008A3D4, ORIG:  ConstBitStream(hex = "0x2130A0022A00C7262140600221200000212800002620092421500000750B020C12000B245B27020800000000"), 
                        PATCH: ConstBitStream(hex = "0x7038240EDA0053267038240E000000007038240E00000000000000005B270208000000000000000000000000")
      },

      # Description length limit (ammo)
      {POS: 0x0008D1D0, ORIG:  ConstBitStream(hex = "0x1D000224"), 
                        PATCH: ConstBitStream(hex = "0xFF000224")
      },
      # Line length limit (ammo)
      {POS: 0x0008D1DC, ORIG:  ConstBitStream(hex = "0x0F000224"), 
                        PATCH: ConstBitStream(hex = "0xFF000224")
      },
      # Newline behavior (ammo)
      {POS: 0x0008D1FC, ORIG:  ConstBitStream(hex = "0x3F34020800300924"), 
                        PATCH: ConstBitStream(hex = "0x6828040800000000")
      },
      # Painting ellipsis (ammo)
      {POS: 0x0008D2E4, ORIG:  ConstBitStream(hex = "0x2130A0022A00C7262140600221200000212800002620092421500000750B020C12000B24FB31020800000000"), 
                        PATCH: ConstBitStream(hex = "0x7038240EDA0053267038240E000000007038240E0000000000000000FB310208000000000000000000000000")
      },
      
      # Newline behavior, continued (presents)
      {POS: 0x0010A240, ORIG:  ConstBitStream(hex = "0x0000000000000000000000000000000000000000000000000000000000000000"), 
                        PATCH: ConstBitStream(hex = "0x0300401200000000CD38220A000000002190540221B000007638220A01003126")
      },
      # Newline behavior, continued (ammo)
      {POS: 0x0010A260, ORIG:  ConstBitStream(hex = "0x0000000000000000000000000000000000000000000000000000000000000000"), 
                        PATCH: ConstBitStream(hex = "0x03004012000000009144220A000000002190540221B000003344220A01003126")
      },
      # Painting ellipsis, continued (both presents and ammo)
      {POS: 0x0010A280, ORIG:  ConstBitStream(hex = "0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"), 
                        PATCH: ConstBitStream(hex = "0xF8FFBD270400BFAF2130A0022A00C726214060022120A003212800002E00092421500000751B220E12000B240000A28F21B0C2020400BF8F0800E0030800BD27")
      },
    ]
  },
  {NAME: "Long Ammo File Fix", ENABLED: True, CFG_ID: "ammo_file_size", DATA:
    [
      # For description preview
      {POS: 0x0008C84C, ORIG: ConstBitStream(hex = "0x0000A384"), PATCH: ConstBitStream(hex = "0x0000A394")},
      # For full descriptions
      {POS: 0x0008C108, ORIG: ConstBitStream(hex = "0x0000658402006484"), PATCH: ConstBitStream(hex = "0x0000659402006494")},
      {POS: 0x0008BB44, ORIG: ConstBitStream(hex = "0x0000648402006284"), PATCH: ConstBitStream(hex = "0x0000649402006294")},
    ]
  },
  {NAME: "Ammo/Present Description Total Line Limit", ENABLED: True, CFG_ID: "ammo_line_limit", DATA:
    [
      {POS: 0x0008BB74, ORIG: ConstBitStream(hex = "0x0B108300"), PATCH: ConstBitStream(hex = "0x21108000")},
    ]
  },
  {NAME: "Fix Glyph Height", ENABLED: False, CFG_ID: "glyph_height", DATA:
    [
      {POS: 0x00082EFC, ORIG: ConstBitStream(hex = "0x10001724"), PATCH: ConstBitStream(hex = "0x19001724")}, # li $s7, 25         ; change glyph height
      {POS: 0x00082F18, ORIG: ConstBitStream(hex = "0x2110E202"), PATCH: ConstBitStream(hex = "0x10004224")}, # addiu $v0, $v0, 16 ; fix the offset
      {POS: 0x00082FF0, ORIG: ConstBitStream(hex = "0x10180000"), PATCH: ConstBitStream(hex = "0x00020324")}, # li $v1, 512        ; fix line spacing
    ]
  },
]

def apply_sys_lang(eboot):
  sys_menu_lang = 1
  if LANG_CFG_ID in common.editor_config.hacks:
    sys_menu_lang = common.editor_config.hacks[LANG_CFG_ID]
  
  patch_loc = 0x1B2E0
  patch = ConstBitStream(uintle = sys_menu_lang, length = 8) + ConstBitStream(hex = "0x000224")
  eboot.overwrite(patch, patch_loc * 8)
  return eboot

def apply_eboot_patches(eboot):
  
  for patch in EBOOT_PATCHES:
  
    enabled = patch[ENABLED]
    if patch[CFG_ID] in common.editor_config.hacks:
      enabled = common.editor_config.hacks[patch[CFG_ID]]
    
    # So we can undo patches if they've already been applied.
    key = PATCH if enabled else ORIG
    
    for item in patch[DATA]:
      eboot.overwrite(item[key], item[POS] * 8)
  
  eboot = apply_sys_lang(eboot)
  return eboot

if __name__ == "__main__":
  src = "X:\\Danganronpa\\Danganronpa_BEST\\EBOOT-ORIG.BIN"
  dst = "X:\\Danganronpa\\Danganronpa_BEST\\EBOOT-TEST.BIN"
  test = BitStream(filename = src)
  test = apply_eboot_patches(test)
  with open(dst, "wb") as f:
    test.tofile(f)

### EOF ###