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
                        PATCH: ConstBitStream(hex = "0x010000000097100000BE49000000000000200100002001000700000010000000")},
      {POS: 0x00000078, ORIG:  ConstBitStream(hex = "0x00971000"), PATCH: ConstBitStream(hex = "0x00B71100")},
      {POS: 0x00000098, ORIG:  ConstBitStream(hex = "0xE0331100"), PATCH: ConstBitStream(hex = "0xE0531200")},
    ]
  },
  {NAME: "Increase Number of Displayable Glyphs", ENABLED: True, CFG_ID: "final_boss", DATA:
    [
      {POS: 0x00008300, ORIG: ConstBitStream(hex = "0x31"),   PATCH: ConstBitStream(hex = "0x39")},
      {POS: 0x00008308, ORIG: ConstBitStream(hex = "0x3C3E"), PATCH: ConstBitStream(hex = "0xC027")},
      {POS: 0x00008614, ORIG: ConstBitStream(hex = "0x31"),   PATCH: ConstBitStream(hex = "0x39")},
      {POS: 0x00008618, ORIG: ConstBitStream(hex = "0x3C3E"), PATCH: ConstBitStream(hex = "0xC027")},
      {POS: 0x00008624, ORIG: ConstBitStream(hex = "0xF401"), PATCH: ConstBitStream(hex = "0xE803")},
      {POS: 0x000086C4, ORIG: ConstBitStream(hex = "0x31"),   PATCH: ConstBitStream(hex = "0x39")},
      {POS: 0x000086C8, ORIG: ConstBitStream(hex = "0x32"),   PATCH: ConstBitStream(hex = "0x3A")},
      {POS: 0x000086CC, ORIG: ConstBitStream(hex = "0x3C3E"), PATCH: ConstBitStream(hex = "0xC027")},
      {POS: 0x000086D4, ORIG: ConstBitStream(hex = "0xDCCA"), PATCH: ConstBitStream(hex = "0x0041")},
      {POS: 0x00008780, ORIG: ConstBitStream(hex = "0x31"),   PATCH: ConstBitStream(hex = "0x39")},
      {POS: 0x00008788, ORIG: ConstBitStream(hex = "0x3C3E"), PATCH: ConstBitStream(hex = "0xC027")},
      {POS: 0x00008A7C, ORIG: ConstBitStream(hex = "0x31"),   PATCH: ConstBitStream(hex = "0x39")},
      {POS: 0x00008A80, ORIG: ConstBitStream(hex = "0x32"),   PATCH: ConstBitStream(hex = "0x3A")},
      {POS: 0x00008A84, ORIG: ConstBitStream(hex = "0x3C3E"), PATCH: ConstBitStream(hex = "0xC027")},
      {POS: 0x00008A88, ORIG: ConstBitStream(hex = "0xDCCA"), PATCH: ConstBitStream(hex = "0x0041")},
      {POS: 0x00008AF0, ORIG: ConstBitStream(hex = "0x31"),   PATCH: ConstBitStream(hex = "0x39")},
      {POS: 0x00008AF4, ORIG: ConstBitStream(hex = "0x32"),   PATCH: ConstBitStream(hex = "0x3A")},
      {POS: 0x00008AFC, ORIG: ConstBitStream(hex = "0x3C3E"), PATCH: ConstBitStream(hex = "0xC027")},
      {POS: 0x00008B00, ORIG: ConstBitStream(hex = "0xDCCA"), PATCH: ConstBitStream(hex = "0x0041")},
      {POS: 0x00008CEC, ORIG: ConstBitStream(hex = "0x31"),   PATCH: ConstBitStream(hex = "0x39")},
      {POS: 0x00008CF8, ORIG: ConstBitStream(hex = "0x3C3E"), PATCH: ConstBitStream(hex = "0xC027")},
      {POS: 0x00008ED4, ORIG: ConstBitStream(hex = "0x31"),   PATCH: ConstBitStream(hex = "0x39")},
      {POS: 0x00008EE4, ORIG: ConstBitStream(hex = "0x3C3E"), PATCH: ConstBitStream(hex = "0xC027")},
      {POS: 0x00008EB4, ORIG: ConstBitStream(hex = "0x01"),   PATCH: ConstBitStream(hex = "0x31")},
      {POS: 0x00008EBC, ORIG: ConstBitStream(hex = "0x38AC"), PATCH: ConstBitStream(hex = "0x3C3E")},
      {POS: 0x000092F0, ORIG: ConstBitStream(hex = "0xF401"), PATCH: ConstBitStream(hex = "0xE803")},
      {POS: 0x00009B48, ORIG: ConstBitStream(hex = "0x31"),   PATCH: ConstBitStream(hex = "0x39")},
      {POS: 0x00009B54, ORIG: ConstBitStream(hex = "0x3C3E"), PATCH: ConstBitStream(hex = "0xC027")},
      {POS: 0x00009C78, ORIG: ConstBitStream(hex = "0x31"),   PATCH: ConstBitStream(hex = "0x39")},
      {POS: 0x00009C84, ORIG: ConstBitStream(hex = "0x3C3E"), PATCH: ConstBitStream(hex = "0xC027")},
      {POS: 0x00009B10, ORIG: ConstBitStream(hex = "0x01"),   PATCH: ConstBitStream(hex = "0x31")},
      {POS: 0x00009B20, ORIG: ConstBitStream(hex = "0x38AC"), PATCH: ConstBitStream(hex = "0x3C3E")},
      {POS: 0x00009B40, ORIG: ConstBitStream(hex = "0x01"),   PATCH: ConstBitStream(hex = "0x31")},
      {POS: 0x00009B44, ORIG: ConstBitStream(hex = "0x38AC"), PATCH: ConstBitStream(hex = "0x3C3E")},
      {POS: 0x00009BB0, ORIG: ConstBitStream(hex = "0x01"),   PATCH: ConstBitStream(hex = "0x31")},
      {POS: 0x00009BB4, ORIG: ConstBitStream(hex = "0x3AAC"), PATCH: ConstBitStream(hex = "0x3E3E")},
      {POS: 0x00009BE4, ORIG: ConstBitStream(hex = "0x38AC"), PATCH: ConstBitStream(hex = "0x3C3E")},
      {POS: 0x00009C3C, ORIG: ConstBitStream(hex = "0x38AC"), PATCH: ConstBitStream(hex = "0x3C3E")},
      {POS: 0x00009C64, ORIG: ConstBitStream(hex = "0x38AC"), PATCH: ConstBitStream(hex = "0x3C3E")},
      {POS: 0x00009B18, ORIG: ConstBitStream(hex = "0x01"),   PATCH: ConstBitStream(hex = "0x31")},
      {POS: 0x00009B1C, ORIG: ConstBitStream(hex = "0x20B0"), PATCH: ConstBitStream(hex = "0x0C46")},
      {POS: 0x00009BAC, ORIG: ConstBitStream(hex = "0x38AC"), PATCH: ConstBitStream(hex = "0x3C3E")},
      {POS: 0x0000A5D4, ORIG: ConstBitStream(hex = "0x38AC"), PATCH: ConstBitStream(hex = "0x3C3E")},
      {POS: 0x0000A600, ORIG: ConstBitStream(hex = "0x38AC"), PATCH: ConstBitStream(hex = "0x3C3E")},
      {POS: 0x00009B64, ORIG: ConstBitStream(hex = "0xF401"), PATCH: ConstBitStream(hex = "0xE803")},
      {POS: 0x0000A01C, ORIG: ConstBitStream(hex = "0xF401"), PATCH: ConstBitStream(hex = "0xE803")},
      {POS: 0x00009A3C, ORIG: ConstBitStream(hex = "0xB0FC"), PATCH: ConstBitStream(hex = "0xBCFA")},
      {POS: 0x00009B08, ORIG: ConstBitStream(hex = "0x5003"), PATCH: ConstBitStream(hex = "0x4405")},
      {POS: 0x0000A094, ORIG: ConstBitStream(hex = "0x5003"), PATCH: ConstBitStream(hex = "0x4405")},
      {POS: 0x00009A44, ORIG: ConstBitStream(hex = "0x1403"), PATCH: ConstBitStream(hex = "0x0805")},
      {POS: 0x00009A50, ORIG: ConstBitStream(hex = "0x1003"), PATCH: ConstBitStream(hex = "0x0405")},
      {POS: 0x00009A54, ORIG: ConstBitStream(hex = "0x0C03"), PATCH: ConstBitStream(hex = "0x0005")},
      {POS: 0x00009A58, ORIG: ConstBitStream(hex = "0x0803"), PATCH: ConstBitStream(hex = "0xFC04")},
      {POS: 0x00009A5C, ORIG: ConstBitStream(hex = "0x0403"), PATCH: ConstBitStream(hex = "0xF804")},
      {POS: 0x00009A60, ORIG: ConstBitStream(hex = "0x0003"), PATCH: ConstBitStream(hex = "0xF404")},
      {POS: 0x00009A64, ORIG: ConstBitStream(hex = "0xFC02"), PATCH: ConstBitStream(hex = "0xF004")},
      {POS: 0x00009A68, ORIG: ConstBitStream(hex = "0xF802"), PATCH: ConstBitStream(hex = "0xEC04")},
      {POS: 0x00009A6C, ORIG: ConstBitStream(hex = "0xF402"), PATCH: ConstBitStream(hex = "0xE804")},
      {POS: 0x00009A70, ORIG: ConstBitStream(hex = "0xF002"), PATCH: ConstBitStream(hex = "0xE404")},
      {POS: 0x00009A74, ORIG: ConstBitStream(hex = "0x4403"), PATCH: ConstBitStream(hex = "0x3805")},
      {POS: 0x00009A78, ORIG: ConstBitStream(hex = "0x4003"), PATCH: ConstBitStream(hex = "0x3405")},
      {POS: 0x00009A7C, ORIG: ConstBitStream(hex = "0x3C03"), PATCH: ConstBitStream(hex = "0x3005")},
      {POS: 0x00009A80, ORIG: ConstBitStream(hex = "0x3803"), PATCH: ConstBitStream(hex = "0x2C05")},
      {POS: 0x00009A84, ORIG: ConstBitStream(hex = "0x3403"), PATCH: ConstBitStream(hex = "0x2805")},
      {POS: 0x00009A88, ORIG: ConstBitStream(hex = "0x3003"), PATCH: ConstBitStream(hex = "0x2405")},
      {POS: 0x00009A8C, ORIG: ConstBitStream(hex = "0x2C03"), PATCH: ConstBitStream(hex = "0x2005")},
      {POS: 0x00009A90, ORIG: ConstBitStream(hex = "0x2803"), PATCH: ConstBitStream(hex = "0x1C05")},
      {POS: 0x00009A94, ORIG: ConstBitStream(hex = "0x2403"), PATCH: ConstBitStream(hex = "0x1805")},
      {POS: 0x00009A98, ORIG: ConstBitStream(hex = "0x2003"), PATCH: ConstBitStream(hex = "0x1405")},
      {POS: 0x00009AB0, ORIG: ConstBitStream(hex = "0x1403"), PATCH: ConstBitStream(hex = "0x0805")},
      {POS: 0x00009AB4, ORIG: ConstBitStream(hex = "0x1003"), PATCH: ConstBitStream(hex = "0x0405")},
      {POS: 0x00009AB8, ORIG: ConstBitStream(hex = "0x0C03"), PATCH: ConstBitStream(hex = "0x0005")},
      {POS: 0x00009ABC, ORIG: ConstBitStream(hex = "0x0803"), PATCH: ConstBitStream(hex = "0xFC04")},
      {POS: 0x00009AC0, ORIG: ConstBitStream(hex = "0x0403"), PATCH: ConstBitStream(hex = "0xF804")},
      {POS: 0x00009AC4, ORIG: ConstBitStream(hex = "0x0003"), PATCH: ConstBitStream(hex = "0xF404")},
      {POS: 0x00009AC8, ORIG: ConstBitStream(hex = "0xFC02"), PATCH: ConstBitStream(hex = "0xF004")},
      {POS: 0x00009ACC, ORIG: ConstBitStream(hex = "0xF802"), PATCH: ConstBitStream(hex = "0xEC04")},
      {POS: 0x00009AD0, ORIG: ConstBitStream(hex = "0xF402"), PATCH: ConstBitStream(hex = "0xE804")},
      {POS: 0x00009AD4, ORIG: ConstBitStream(hex = "0xF002"), PATCH: ConstBitStream(hex = "0xE404")},
      {POS: 0x00009AD8, ORIG: ConstBitStream(hex = "0x4403"), PATCH: ConstBitStream(hex = "0x3805")},
      {POS: 0x00009ADC, ORIG: ConstBitStream(hex = "0x4003"), PATCH: ConstBitStream(hex = "0x3405")},
      {POS: 0x00009AE0, ORIG: ConstBitStream(hex = "0x3C03"), PATCH: ConstBitStream(hex = "0x3005")},
      {POS: 0x00009AE4, ORIG: ConstBitStream(hex = "0x3803"), PATCH: ConstBitStream(hex = "0x2C05")},
      {POS: 0x00009AE8, ORIG: ConstBitStream(hex = "0x3403"), PATCH: ConstBitStream(hex = "0x2805")},
      {POS: 0x00009AEC, ORIG: ConstBitStream(hex = "0x3003"), PATCH: ConstBitStream(hex = "0x2405")},
      {POS: 0x00009AF0, ORIG: ConstBitStream(hex = "0x2C03"), PATCH: ConstBitStream(hex = "0x2005")},
      {POS: 0x00009AF4, ORIG: ConstBitStream(hex = "0x2803"), PATCH: ConstBitStream(hex = "0x1C05")},
      {POS: 0x00009AF8, ORIG: ConstBitStream(hex = "0x2403"), PATCH: ConstBitStream(hex = "0x1805")},
      {POS: 0x00009AFC, ORIG: ConstBitStream(hex = "0x2003"), PATCH: ConstBitStream(hex = "0x1405")},
      {POS: 0x00009B14, ORIG: ConstBitStream(hex = "0xDC02"), PATCH: ConstBitStream(hex = "0xD004")},
      {POS: 0x00009DB4, ORIG: ConstBitStream(hex = "0xD802"), PATCH: ConstBitStream(hex = "0xCC04")},
      {POS: 0x00009DDC, ORIG: ConstBitStream(hex = "0xCC02"), PATCH: ConstBitStream(hex = "0xC004")},
      {POS: 0x00009DF4, ORIG: ConstBitStream(hex = "0xEC02"), PATCH: ConstBitStream(hex = "0xE004")},
      {POS: 0x00009E08, ORIG: ConstBitStream(hex = "0xD002"), PATCH: ConstBitStream(hex = "0xC404")},
      {POS: 0x00009E14, ORIG: ConstBitStream(hex = "0xD402"), PATCH: ConstBitStream(hex = "0xC804")},
      {POS: 0x00009EDC, ORIG: ConstBitStream(hex = "0xCC02"), PATCH: ConstBitStream(hex = "0xC004")},
      {POS: 0x00009EE8, ORIG: ConstBitStream(hex = "0xD002"), PATCH: ConstBitStream(hex = "0xC404")},
      {POS: 0x00009EF8, ORIG: ConstBitStream(hex = "0xD402"), PATCH: ConstBitStream(hex = "0xC804")},
      {POS: 0x00009F50, ORIG: ConstBitStream(hex = "0xCC02"), PATCH: ConstBitStream(hex = "0xC004")},
      {POS: 0x00009F60, ORIG: ConstBitStream(hex = "0xD002"), PATCH: ConstBitStream(hex = "0xC404")},
      {POS: 0x00009F6C, ORIG: ConstBitStream(hex = "0xE802"), PATCH: ConstBitStream(hex = "0xDC04")},
      {POS: 0x00009F78, ORIG: ConstBitStream(hex = "0xE402"), PATCH: ConstBitStream(hex = "0xD804")},
      {POS: 0x00009F84, ORIG: ConstBitStream(hex = "0xE002"), PATCH: ConstBitStream(hex = "0xD404")},
      {POS: 0x00009FC8, ORIG: ConstBitStream(hex = "0xD402"), PATCH: ConstBitStream(hex = "0xC804")},
      {POS: 0x00009FCC, ORIG: ConstBitStream(hex = "0xD802"), PATCH: ConstBitStream(hex = "0xCC04")},
      {POS: 0x00009FE0, ORIG: ConstBitStream(hex = "0xEC02"), PATCH: ConstBitStream(hex = "0xE004")},
      {POS: 0x00009FF8, ORIG: ConstBitStream(hex = "0xEC02"), PATCH: ConstBitStream(hex = "0xE004")},
      {POS: 0x0000A030, ORIG: ConstBitStream(hex = "0xDC02"), PATCH: ConstBitStream(hex = "0xD004")},
      {POS: 0x0000A034, ORIG: ConstBitStream(hex = "0x1403"), PATCH: ConstBitStream(hex = "0x0805")},
      {POS: 0x0000A038, ORIG: ConstBitStream(hex = "0x1003"), PATCH: ConstBitStream(hex = "0x0405")},
      {POS: 0x0000A03C, ORIG: ConstBitStream(hex = "0x0C03"), PATCH: ConstBitStream(hex = "0x0005")},
      {POS: 0x0000A040, ORIG: ConstBitStream(hex = "0x0803"), PATCH: ConstBitStream(hex = "0xFC04")},
      {POS: 0x0000A044, ORIG: ConstBitStream(hex = "0x0403"), PATCH: ConstBitStream(hex = "0xF804")},
      {POS: 0x0000A048, ORIG: ConstBitStream(hex = "0x0003"), PATCH: ConstBitStream(hex = "0xF404")},
      {POS: 0x0000A04C, ORIG: ConstBitStream(hex = "0xFC02"), PATCH: ConstBitStream(hex = "0xF004")},
      {POS: 0x0000A050, ORIG: ConstBitStream(hex = "0xF802"), PATCH: ConstBitStream(hex = "0xEC04")},
      {POS: 0x0000A054, ORIG: ConstBitStream(hex = "0xF402"), PATCH: ConstBitStream(hex = "0xE804")},
      {POS: 0x0000A058, ORIG: ConstBitStream(hex = "0xF002"), PATCH: ConstBitStream(hex = "0xE404")},
      {POS: 0x0000A05C, ORIG: ConstBitStream(hex = "0x4403"), PATCH: ConstBitStream(hex = "0x3805")},
      {POS: 0x0000A060, ORIG: ConstBitStream(hex = "0x4003"), PATCH: ConstBitStream(hex = "0x3405")},
      {POS: 0x0000A064, ORIG: ConstBitStream(hex = "0x3C03"), PATCH: ConstBitStream(hex = "0x3005")},
      {POS: 0x0000A068, ORIG: ConstBitStream(hex = "0x3803"), PATCH: ConstBitStream(hex = "0x2C05")},
      {POS: 0x0000A06C, ORIG: ConstBitStream(hex = "0x3403"), PATCH: ConstBitStream(hex = "0x2805")},
      {POS: 0x0000A070, ORIG: ConstBitStream(hex = "0x3003"), PATCH: ConstBitStream(hex = "0x2405")},
      {POS: 0x0000A074, ORIG: ConstBitStream(hex = "0x2C03"), PATCH: ConstBitStream(hex = "0x2005")},
      {POS: 0x0000A078, ORIG: ConstBitStream(hex = "0x2803"), PATCH: ConstBitStream(hex = "0x1C05")},
      {POS: 0x0000A07C, ORIG: ConstBitStream(hex = "0x2403"), PATCH: ConstBitStream(hex = "0x1805")},
      {POS: 0x0000A080, ORIG: ConstBitStream(hex = "0x2003"), PATCH: ConstBitStream(hex = "0x1405")},
      {POS: 0x0000A0C8, ORIG: ConstBitStream(hex = "0xD802"), PATCH: ConstBitStream(hex = "0xCC04")},
      {POS: 0x0000A0D8, ORIG: ConstBitStream(hex = "0xC402"), PATCH: ConstBitStream(hex = "0xB804")},
      {POS: 0x0000A114, ORIG: ConstBitStream(hex = "0xE802"), PATCH: ConstBitStream(hex = "0xDC04")},
      {POS: 0x0000A118, ORIG: ConstBitStream(hex = "0xE402"), PATCH: ConstBitStream(hex = "0xD804")},
      {POS: 0x0000A144, ORIG: ConstBitStream(hex = "0xE002"), PATCH: ConstBitStream(hex = "0xD404")},
      {POS: 0x0000A154, ORIG: ConstBitStream(hex = "0xC402"), PATCH: ConstBitStream(hex = "0xB804")},
      {POS: 0x0000A21C, ORIG: ConstBitStream(hex = "0xD802"), PATCH: ConstBitStream(hex = "0xCC04")},
      {POS: 0x0000A22C, ORIG: ConstBitStream(hex = "0xC802"), PATCH: ConstBitStream(hex = "0xBC04")},
      {POS: 0x0000A268, ORIG: ConstBitStream(hex = "0xE802"), PATCH: ConstBitStream(hex = "0xDC04")},
      {POS: 0x0000A26C, ORIG: ConstBitStream(hex = "0xE402"), PATCH: ConstBitStream(hex = "0xD804")},
      {POS: 0x0000A298, ORIG: ConstBitStream(hex = "0xE002"), PATCH: ConstBitStream(hex = "0xD404")},
      {POS: 0x0000A2A8, ORIG: ConstBitStream(hex = "0xC802"), PATCH: ConstBitStream(hex = "0xBC04")},
      {POS: 0x0000A368, ORIG: ConstBitStream(hex = "0xD802"), PATCH: ConstBitStream(hex = "0xCC04")},
      {POS: 0x0000A398, ORIG: ConstBitStream(hex = "0xC002"), PATCH: ConstBitStream(hex = "0xB404")},
      {POS: 0x0000A3C0, ORIG: ConstBitStream(hex = "0xE802"), PATCH: ConstBitStream(hex = "0xDC04")},
      {POS: 0x0000A3CC, ORIG: ConstBitStream(hex = "0xC002"), PATCH: ConstBitStream(hex = "0xB404")},
      {POS: 0x0000A3EC, ORIG: ConstBitStream(hex = "0xE402"), PATCH: ConstBitStream(hex = "0xD804")},
      {POS: 0x0000A3FC, ORIG: ConstBitStream(hex = "0xE002"), PATCH: ConstBitStream(hex = "0xD404")},
      {POS: 0x0000A484, ORIG: ConstBitStream(hex = "0xEC02"), PATCH: ConstBitStream(hex = "0xE004")},
      {POS: 0x0000A4F8, ORIG: ConstBitStream(hex = "0xC002"), PATCH: ConstBitStream(hex = "0xB404")},
      {POS: 0x0000A518, ORIG: ConstBitStream(hex = "0xE802"), PATCH: ConstBitStream(hex = "0xDC04")},
      {POS: 0x0000A51C, ORIG: ConstBitStream(hex = "0xE402"), PATCH: ConstBitStream(hex = "0xD804")},
      {POS: 0x0000A528, ORIG: ConstBitStream(hex = "0xE002"), PATCH: ConstBitStream(hex = "0xD404")},
      {POS: 0x0000A628, ORIG: ConstBitStream(hex = "0x31"),   PATCH: ConstBitStream(hex = "0x39")},
      {POS: 0x0000A654, ORIG: ConstBitStream(hex = "0xF401"), PATCH: ConstBitStream(hex = "0xE803")},
      {POS: 0x0000A65C, ORIG: ConstBitStream(hex = "0x3C3E"), PATCH: ConstBitStream(hex = "0xC027")},
      {POS: 0x0000A9FC, ORIG: ConstBitStream(hex = "0x31"),   PATCH: ConstBitStream(hex = "0x39")},
      {POS: 0x0000AA08, ORIG: ConstBitStream(hex = "0x3C3E"), PATCH: ConstBitStream(hex = "0xC027")},
      {POS: 0x0000AE8C, ORIG: ConstBitStream(hex = "0x31"),   PATCH: ConstBitStream(hex = "0x39")},
      {POS: 0x0000AE94, ORIG: ConstBitStream(hex = "0x3C3E"), PATCH: ConstBitStream(hex = "0xC027")},
      {POS: 0x0000B178, ORIG: ConstBitStream(hex = "0x31"),   PATCH: ConstBitStream(hex = "0x39")},
      {POS: 0x0000B188, ORIG: ConstBitStream(hex = "0x3C3E"), PATCH: ConstBitStream(hex = "0xC027")},
      {POS: 0x0000B1A0, ORIG: ConstBitStream(hex = "0x32"),   PATCH: ConstBitStream(hex = "0x3A")},
      {POS: 0x0000B1A8, ORIG: ConstBitStream(hex = "0xDCCA"), PATCH: ConstBitStream(hex = "0x0041")},
      {POS: 0x0000B32C, ORIG: ConstBitStream(hex = "0x31"),   PATCH: ConstBitStream(hex = "0x39")},
      {POS: 0x0000B330, ORIG: ConstBitStream(hex = "0x32"),   PATCH: ConstBitStream(hex = "0x3A")},
      {POS: 0x0000B334, ORIG: ConstBitStream(hex = "0x3C3E"), PATCH: ConstBitStream(hex = "0xC027")},
      {POS: 0x0000B338, ORIG: ConstBitStream(hex = "0xDCCA"), PATCH: ConstBitStream(hex = "0x0041")},
      {POS: 0x0000B384, ORIG: ConstBitStream(hex = "0x31"),   PATCH: ConstBitStream(hex = "0x39")},
      {POS: 0x0000B390, ORIG: ConstBitStream(hex = "0x3C3E"), PATCH: ConstBitStream(hex = "0xC027")},
      {POS: 0x0000B39C, ORIG: ConstBitStream(hex = "0x32"),   PATCH: ConstBitStream(hex = "0x3A")},
      {POS: 0x0000B3A4, ORIG: ConstBitStream(hex = "0xDCCA"), PATCH: ConstBitStream(hex = "0x0041")},
      {POS: 0x0000B554, ORIG: ConstBitStream(hex = "0x31"),   PATCH: ConstBitStream(hex = "0x39")},
      {POS: 0x0000B55C, ORIG: ConstBitStream(hex = "0x32"),   PATCH: ConstBitStream(hex = "0x3A")},
      {POS: 0x0000B560, ORIG: ConstBitStream(hex = "0x3C3E"), PATCH: ConstBitStream(hex = "0xC027")},
      {POS: 0x0000B564, ORIG: ConstBitStream(hex = "0xDCCA"), PATCH: ConstBitStream(hex = "0x0041")},
      {POS: 0x0002B898, ORIG: ConstBitStream(hex = "0x31"),   PATCH: ConstBitStream(hex = "0x39")},
      {POS: 0x0002B89C, ORIG: ConstBitStream(hex = "0x32"),   PATCH: ConstBitStream(hex = "0x3A")},
      {POS: 0x0002B8A0, ORIG: ConstBitStream(hex = "0xDCCA"), PATCH: ConstBitStream(hex = "0x0041")},
      {POS: 0x0002B8A8, ORIG: ConstBitStream(hex = "0x3C3E"), PATCH: ConstBitStream(hex = "0xC027")},
      {POS: 0x0002B930, ORIG: ConstBitStream(hex = "0x3C3E"), PATCH: ConstBitStream(hex = "0xC027")},
      {POS: 0x000B4C9C, ORIG: ConstBitStream(hex = "0x31"),   PATCH: ConstBitStream(hex = "0x39")},
      {POS: 0x000B4CD8, ORIG: ConstBitStream(hex = "0x3C3E"), PATCH: ConstBitStream(hex = "0xC027")},
    ]
  },
  {NAME: "Swap O/X Buttons", ENABLED: True, CFG_ID: "swap_ox", DATA:
    [
      {POS: 0x0001B404, ORIG:  ConstBitStream(hex = "0x21108000"), PATCH: ConstBitStream(hex = "0x01000224")},
      {POS: 0x0000E2A4, ORIG:  ConstBitStream(hex = "0x0400B18F"), PATCH: ConstBitStream(hex = "0x5CC6320A")},
      {POS: 0x0011B270, ORIG:  ConstBitStream(hex = "0x000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"),
                        PATCH: ConstBitStream(hex = "0x0400B18F21202002002025320200A014004031360040313A0040843002008014002031360020313A7B48200A00000000")},
    ]
  },
  {NAME: "Glyph Height Fix", ENABLED: True, CFG_ID: "glyph_height", DATA:
    [
      {POS: 0x00082F1C, ORIG:  ConstBitStream(hex = "0x10001724"), PATCH: ConstBitStream(hex = "0x19001724")},
      {POS: 0x00082F38, ORIG:  ConstBitStream(hex = "0x2110E202"), PATCH: ConstBitStream(hex = "0x10004224")},
      {POS: 0x00082FF8, ORIG:  ConstBitStream(hex = "0x2110E202"), PATCH: ConstBitStream(hex = "0x10004224")},
      {POS: 0x00082F14, ORIG:  ConstBitStream(hex = "0x03"),       PATCH: ConstBitStream(hex = "0x00")},
      {POS: 0x00082F40, ORIG:  ConstBitStream(hex = "0x06"),       PATCH: ConstBitStream(hex = "0x09")},
      {POS: 0x00082F64, ORIG:  ConstBitStream(hex = "0xC3370200"), PATCH: ConstBitStream(hex = "0xD0C5320E")},
      {POS: 0x0011B040, ORIG:  ConstBitStream(hex = "0x0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"),
                        PATCH: ConstBitStream(hex = "0xFCFFBD270000B3AF4B00132403005316DC0513240100535091050224C33702000000B38F0800E0030400BD27")},
    ]
  },
  {NAME: "Map Label Centering", ENABLED: True, CFG_ID: "map_centering", DATA:
    [
      {POS: 0x000833A0, ORIG:  ConstBitStream(hex = "0x0200144602000146"),
                        PATCH: ConstBitStream(hex = "0xDCC5320A02001446")},
      {POS: 0x0011B070, ORIG:  ConstBitStream(hex = "0x0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"),
                        PATCH: ConstBitStream(hex = "0x1400BF8F1000B4AF8808143CD47594260600F41302000146D40094260300F41300000000BA1C220A1000B48F0D000046E5C5320A20008046")},
      {POS: 0x00083738, ORIG:  ConstBitStream(hex = "0x42060246"), PATCH: ConstBitStream(hex = "0x42161446")},
      {POS: 0x0008EA34, ORIG:  ConstBitStream(hex = "0x84000624"), PATCH: ConstBitStream(hex = "0x8A000624")},
      {POS: 0x0008EA9C, ORIG:  ConstBitStream(hex = "0x84000624"), PATCH: ConstBitStream(hex = "0x8A000624")},
      {POS: 0x0008EAD0, ORIG:  ConstBitStream(hex = "0x84000624"), PATCH: ConstBitStream(hex = "0x8A000624")},
      {POS: 0x0008EB70, ORIG:  ConstBitStream(hex = "0x84000624"), PATCH: ConstBitStream(hex = "0x8A000624")},
      {POS: 0x0008EBD8, ORIG:  ConstBitStream(hex = "0x84000624"), PATCH: ConstBitStream(hex = "0x8A000624")},
      {POS: 0x0008EC0C, ORIG:  ConstBitStream(hex = "0x84000624"), PATCH: ConstBitStream(hex = "0x8A000624")},
      {POS: 0x0009008C, ORIG:  ConstBitStream(hex = "0x84000624"), PATCH: ConstBitStream(hex = "0x8A000624")},
      {POS: 0x00090318, ORIG:  ConstBitStream(hex = "0x84000624"), PATCH: ConstBitStream(hex = "0x8A000624")},
      {POS: 0x00090378, ORIG:  ConstBitStream(hex = "0x84000624"), PATCH: ConstBitStream(hex = "0x8A000624")},
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
                        PATCH: ConstBitStream(hex = "0xECB5120800000000")},
      {POS: 0x0008A3F4, ORIG:  ConstBitStream(hex = "0x2130A0022A00C7262140600221200000212800002620092421500000750B020C12000B245B27020800000000"), 
                        PATCH: ConstBitStream(hex = "0xFCC5320EDA005326FCC5320E00000000FCC5320E00000000000000005B270208000000000000000000000000")},
      {POS: 0x0008D1F0, ORIG:  ConstBitStream(hex = "0x1D000224"), 
                        PATCH: ConstBitStream(hex = "0xFF000224")},
      {POS: 0x0008D1FC, ORIG:  ConstBitStream(hex = "0x0F000224"), 
                        PATCH: ConstBitStream(hex = "0xFF000224")},
      {POS: 0x0008D21C, ORIG:  ConstBitStream(hex = "0x3F34020800300924"), 
                        PATCH: ConstBitStream(hex = "0xF4B5120800000000")},
      {POS: 0x0008D304, ORIG:  ConstBitStream(hex = "0x2130A0022A00C7262140600221200000212800002620092421500000750B020C12000B24FB31020800000000"), 
                        PATCH: ConstBitStream(hex = "0xFCC5320EDA005326FCC5320E00000000FCC5320E0000000000000000FB310208000000000000000000000000")},
      {POS: 0x0011B0B0, ORIG:  ConstBitStream(hex = "0x0000000000000000000000000000000000000000000000000000000000000000"), 
                        PATCH: ConstBitStream(hex = "0x0300401200000000CD38220A000000002190540221B000007638220A01003126")},
      {POS: 0x0011B0D0, ORIG:  ConstBitStream(hex = "0x0000000000000000000000000000000000000000000000000000000000000000"), 
                        PATCH: ConstBitStream(hex = "0x03004012000000009144220A000000002190540221B000003344220A01003126")},
      {POS: 0x0011B0F0, ORIG:  ConstBitStream(hex = "0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"), 
                        PATCH: ConstBitStream(hex = "0xF8FFBD270400BFAF2130A0022A00C726214060022120A003212800002E00092421500000751B220E12000B240000A28F21B0C2020400BF8F0800E0030800BD27")},
    ]
  },
  {NAME: "Ammo/Present Menu (Long File Fix)", ENABLED: True, CFG_ID: "ammo_file_size", DATA:
    [
      {POS: 0x0008C86C, ORIG: ConstBitStream(hex = "0x0000A384"),         PATCH: ConstBitStream(hex = "0x0000A394")},
      {POS: 0x0008C128, ORIG: ConstBitStream(hex = "0x0000658402006484"), PATCH: ConstBitStream(hex = "0x0000659402006494")},
      {POS: 0x0008BB64, ORIG: ConstBitStream(hex = "0x0000648402006284"), PATCH: ConstBitStream(hex = "0x0000649402006294")},
    ]
  },
  {NAME: "Ammo/Present Menu (Total Line Limit)", ENABLED: True, CFG_ID: "ammo_line_limit", DATA:
    [
      {POS: 0x0008BB94, ORIG: ConstBitStream(hex = "0x0B108300"), PATCH: ConstBitStream(hex = "0x21108000")},
    ]
  },
  {NAME: "Ammo Menu (Updated Preview Descriptions)", ENABLED: True, CFG_ID: "ammo_updated_desc", DATA:
    [
      {POS: 0x0008C85C, ORIG:  ConstBitStream(hex = "0x4401068E"), PATCH: ConstBitStream(hex = "0x0CC6320E")},
      {POS: 0x0011B130, ORIG:  ConstBitStream(hex = "0x00000000000000000000000000000000000000000000000000000000000000000000000000000000"),
                        PATCH: ConstBitStream(hex = "0xC808053C1C28A524212865000000A680FFFFC62480300600213006023401C58C0800E0034401C68C")},
    ]
  },
  {NAME: "Help Menu (31-Character/Line Limit)", ENABLED: True, CFG_ID: "help_line_length", DATA:
    [
      {POS: 0x000768A0, ORIG: ConstBitStream(hex = "0x80"), PATCH: ConstBitStream(hex = "0x10")},
      {POS: 0x000768A4, ORIG: ConstBitStream(hex = "0x4C"), PATCH: ConstBitStream(hex = "0xBC")},
      {POS: 0x000768B4, ORIG: ConstBitStream(hex = "0x64"), PATCH: ConstBitStream(hex = "0xD4")},
      {POS: 0x000768BC, ORIG: ConstBitStream(hex = "0x60"), PATCH: ConstBitStream(hex = "0xD0")},
      {POS: 0x000768C0, ORIG: ConstBitStream(hex = "0x5C"), PATCH: ConstBitStream(hex = "0xCC")},
      {POS: 0x000768C4, ORIG: ConstBitStream(hex = "0x58"), PATCH: ConstBitStream(hex = "0xC8")},
      {POS: 0x000768C8, ORIG: ConstBitStream(hex = "0x54"), PATCH: ConstBitStream(hex = "0xC4")},
      {POS: 0x000768CC, ORIG: ConstBitStream(hex = "0x50"), PATCH: ConstBitStream(hex = "0xC0")},
      {POS: 0x000768D0, ORIG: ConstBitStream(hex = "0x48"), PATCH: ConstBitStream(hex = "0xB8")},
      {POS: 0x000768D4, ORIG: ConstBitStream(hex = "0x44"), PATCH: ConstBitStream(hex = "0xB4")},
      {POS: 0x000768D8, ORIG: ConstBitStream(hex = "0x40"), PATCH: ConstBitStream(hex = "0xB0")},
      {POS: 0x000768DC, ORIG: ConstBitStream(hex = "0x78"), PATCH: ConstBitStream(hex = "0xE8")},
      {POS: 0x000768E0, ORIG: ConstBitStream(hex = "0x74"), PATCH: ConstBitStream(hex = "0xE4")},
      {POS: 0x000768E8, ORIG: ConstBitStream(hex = "0x70"), PATCH: ConstBitStream(hex = "0xE0")},
      {POS: 0x00076910, ORIG: ConstBitStream(hex = "0x64"), PATCH: ConstBitStream(hex = "0xD4")},
      {POS: 0x00076914, ORIG: ConstBitStream(hex = "0x60"), PATCH: ConstBitStream(hex = "0xD0")},
      {POS: 0x00076918, ORIG: ConstBitStream(hex = "0x5C"), PATCH: ConstBitStream(hex = "0xCC")},
      {POS: 0x0007691C, ORIG: ConstBitStream(hex = "0x58"), PATCH: ConstBitStream(hex = "0xC8")},
      {POS: 0x00076920, ORIG: ConstBitStream(hex = "0x54"), PATCH: ConstBitStream(hex = "0xC4")},
      {POS: 0x00076924, ORIG: ConstBitStream(hex = "0x50"), PATCH: ConstBitStream(hex = "0xC0")},
      {POS: 0x00076928, ORIG: ConstBitStream(hex = "0x4C"), PATCH: ConstBitStream(hex = "0xBC")},
      {POS: 0x0007692C, ORIG: ConstBitStream(hex = "0x48"), PATCH: ConstBitStream(hex = "0xB8")},
      {POS: 0x00076930, ORIG: ConstBitStream(hex = "0x44"), PATCH: ConstBitStream(hex = "0xB4")},
      {POS: 0x00076934, ORIG: ConstBitStream(hex = "0x40"), PATCH: ConstBitStream(hex = "0xB0")},
      {POS: 0x00076938, ORIG: ConstBitStream(hex = "0x78"), PATCH: ConstBitStream(hex = "0xE8")},
      {POS: 0x0007693C, ORIG: ConstBitStream(hex = "0x74"), PATCH: ConstBitStream(hex = "0xE4")},
      {POS: 0x00076940, ORIG: ConstBitStream(hex = "0x70"), PATCH: ConstBitStream(hex = "0xE0")},
      {POS: 0x0007694C, ORIG: ConstBitStream(hex = "0x80"), PATCH: ConstBitStream(hex = "0xF0")},
      {POS: 0x00076D98, ORIG: ConstBitStream(hex = "0x1E"), PATCH: ConstBitStream(hex = "0x56")},
    ]
  },
  {NAME: "Dialogue Box (54-Character/Line Limit)", ENABLED: True, CFG_ID: "dialog_54", DATA:
    [
      {POS: 0x00059C04, ORIG: ConstBitStream(hex = "0x36"),   PATCH: ConstBitStream(hex = "0x42")},
      {POS: 0x0005106C, ORIG: ConstBitStream(hex = "0xDA4B"), PATCH: ConstBitStream(hex = "0x0F3E")},
      {POS: 0x00051070, ORIG: ConstBitStream(hex = "0xF712"), PATCH: ConstBitStream(hex = "0x83E1")},
      {POS: 0x00051090, ORIG: ConstBitStream(hex = "0xC0"),   PATCH: ConstBitStream(hex = "0x80")},
      {POS: 0x00051098, ORIG: ConstBitStream(hex = "0xC020"), PATCH: ConstBitStream(hex = "0x4021")},
      {POS: 0x00050F20, ORIG: ConstBitStream(hex = "0xDA4B"), PATCH: ConstBitStream(hex = "0x0F3E")},
      {POS: 0x00051288, ORIG: ConstBitStream(hex = "0xF712"), PATCH: ConstBitStream(hex = "0x83E1")},
      {POS: 0x00051320, ORIG: ConstBitStream(hex = "0xC0"),   PATCH: ConstBitStream(hex = "0x80")},
      {POS: 0x00051328, ORIG: ConstBitStream(hex = "0xC018"), PATCH: ConstBitStream(hex = "0x4019")},
      {POS: 0x000513D4, ORIG: ConstBitStream(hex = "0xC0"),   PATCH: ConstBitStream(hex = "0x80")},
      {POS: 0x000513DC, ORIG: ConstBitStream(hex = "0xC018"), PATCH: ConstBitStream(hex = "0x4019")},
      {POS: 0x00051134, ORIG: ConstBitStream(hex = "0xC0"),   PATCH: ConstBitStream(hex = "0x80")},
      {POS: 0x0005113C, ORIG: ConstBitStream(hex = "0xC018"), PATCH: ConstBitStream(hex = "0x4019")},
      {POS: 0x0005A050, ORIG: ConstBitStream(hex = "0xC0"),   PATCH: ConstBitStream(hex = "0x80")},
      {POS: 0x0005A05C, ORIG: ConstBitStream(hex = "0xC010"), PATCH: ConstBitStream(hex = "0x4011")},
      {POS: 0x00059D74, ORIG: ConstBitStream(hex = "0xC0"),   PATCH: ConstBitStream(hex = "0xB4")},
      {POS: 0x00059D80, ORIG: ConstBitStream(hex = "0x6C"),   PATCH: ConstBitStream(hex = "0x84")},
      {POS: 0x00059DDC, ORIG: ConstBitStream(hex = "0x36"),   PATCH: ConstBitStream(hex = "0x42")},
      {POS: 0x00059DEC, ORIG: ConstBitStream(hex = "0xC0"),   PATCH: ConstBitStream(hex = "0x80")},
      {POS: 0x00059DF8, ORIG: ConstBitStream(hex = "0x00"),   PATCH: ConstBitStream(hex = "0x80")},
      {POS: 0x00059E2C, ORIG: ConstBitStream(hex = "0xC0"),   PATCH: ConstBitStream(hex = "0x80")},
      {POS: 0x00059E34, ORIG: ConstBitStream(hex = "0x00"),   PATCH: ConstBitStream(hex = "0x80")},
      {POS: 0x00059E38, ORIG: ConstBitStream(hex = "0xC018"), PATCH: ConstBitStream(hex = "0x4019")},
      {POS: 0x00059E60, ORIG: ConstBitStream(hex = "0x36"),   PATCH: ConstBitStream(hex = "0x42")},
      {POS: 0x00059ECC, ORIG: ConstBitStream(hex = "0x6C"),   PATCH: ConstBitStream(hex = "0x84")},
      {POS: 0x00059ED4, ORIG: ConstBitStream(hex = "0x36"),   PATCH: ConstBitStream(hex = "0x42")},
      {POS: 0x000515B0, ORIG: ConstBitStream(hex = "0x36"),   PATCH: ConstBitStream(hex = "0x42")},
      {POS: 0x000515B4, ORIG: ConstBitStream(hex = "0xC0"),   PATCH: ConstBitStream(hex = "0x80")},
      {POS: 0x000515C0, ORIG: ConstBitStream(hex = "0x00"),   PATCH: ConstBitStream(hex = "0x80")},
      {POS: 0x00051600, ORIG: ConstBitStream(hex = "0xC0"),   PATCH: ConstBitStream(hex = "0x80")},
      {POS: 0x00051608, ORIG: ConstBitStream(hex = "0x00"),   PATCH: ConstBitStream(hex = "0x80")},
      {POS: 0x0005160C, ORIG: ConstBitStream(hex = "0xC018"), PATCH: ConstBitStream(hex = "0x4019")},
      {POS: 0x00051630, ORIG: ConstBitStream(hex = "0x36"),   PATCH: ConstBitStream(hex = "0x42")},
      {POS: 0x0005149C, ORIG: ConstBitStream(hex = "0x36"),   PATCH: ConstBitStream(hex = "0x42")},
      {POS: 0x000514A0, ORIG: ConstBitStream(hex = "0xC0"),   PATCH: ConstBitStream(hex = "0x80")},
      {POS: 0x000514AC, ORIG: ConstBitStream(hex = "0x00"),   PATCH: ConstBitStream(hex = "0x80")},
      {POS: 0x000514E0, ORIG: ConstBitStream(hex = "0xC0"),   PATCH: ConstBitStream(hex = "0x80")},
      {POS: 0x000514EC, ORIG: ConstBitStream(hex = "0xC020"), PATCH: ConstBitStream(hex = "0x4021")},
      {POS: 0x0005155C, ORIG: ConstBitStream(hex = "0xC0"),   PATCH: ConstBitStream(hex = "0x80")},
      {POS: 0x00051568, ORIG: ConstBitStream(hex = "0xC020"), PATCH: ConstBitStream(hex = "0x4021")},
      {POS: 0x00094D0C, ORIG: ConstBitStream(hex = "0x36"),   PATCH: ConstBitStream(hex = "0x42")},
      {POS: 0x00094D44, ORIG: ConstBitStream(hex = "0xC0"),   PATCH: ConstBitStream(hex = "0x80")},
      {POS: 0x00094D50, ORIG: ConstBitStream(hex = "0xC020"), PATCH: ConstBitStream(hex = "0x4021")},
      {POS: 0x00059EB8, ORIG: ConstBitStream(hex = "0x0002"), PATCH: ConstBitStream(hex = "0xA001")},
      {POS: 0x00059EE8, ORIG: ConstBitStream(hex = "0x0002"), PATCH: ConstBitStream(hex = "0xA001")},
      {POS: 0x00059EF0, ORIG: ConstBitStream(hex = "0x0002"), PATCH: ConstBitStream(hex = "0xA001")},
      {POS: 0x00059F10, ORIG: ConstBitStream(hex = "0x0002"), PATCH: ConstBitStream(hex = "0xA001")},
      {POS: 0x00051680, ORIG: ConstBitStream(hex = "0x0002"), PATCH: ConstBitStream(hex = "0xA001")},
      {POS: 0x00051438, ORIG: ConstBitStream(hex = "0x0002"), PATCH: ConstBitStream(hex = "0xA001")},
      {POS: 0x00051444, ORIG: ConstBitStream(hex = "0x0002"), PATCH: ConstBitStream(hex = "0xA001")},
      {POS: 0x0005144C, ORIG: ConstBitStream(hex = "0x0002"), PATCH: ConstBitStream(hex = "0xA001")},
      {POS: 0x000516D0, ORIG: ConstBitStream(hex = "0x0002"), PATCH: ConstBitStream(hex = "0xA001")},
      {POS: 0x00095578, ORIG: ConstBitStream(hex = "0x0002"), PATCH: ConstBitStream(hex = "0xA001")},
      {POS: 0x00095528, ORIG: ConstBitStream(hex = "0x0002"), PATCH: ConstBitStream(hex = "0xA001")},
    ]
  },
  {NAME: "Options Centering", ENABLED: True, CFG_ID: "option_center", DATA:
    [
      {POS: 0x001041DE, ORIG: ConstBitStream(hex = "0x09"), PATCH: ConstBitStream(hex = "0x0A")},
      {POS: 0x001041E0, ORIG: ConstBitStream(hex = "0x66"), PATCH: ConstBitStream(hex = "0x6A")},
      {POS: 0x001041E2, ORIG: ConstBitStream(hex = "0x37"), PATCH: ConstBitStream(hex = "0x3A")},
    ]
  },
  {NAME: "Leftover Characters in Multiple-Choice Questions", ENABLED: True, CFG_ID: "mc_leftover_chars", DATA:
    [
      {POS: 0x0005B2E4, ORIG: ConstBitStream(hex = "0x36"), PATCH: ConstBitStream(hex = "0x6C")},
    ]
  },
  {NAME: "Substitute Glyphs on Bullets", ENABLED: True, CFG_ID: "bullet_glyph_sub", DATA:
    [
      {POS: 0x0009F6E0, ORIG: ConstBitStream(hex = "0x0200D626"), PATCH: ConstBitStream(hex = "0x18C6320E")},
      {POS: 0x0011B160, ORIG: ConstBitStream(hex = "0x0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"), PATCH: ConstBitStream(hex = "0x200004243D00835053210324210004243A00835054210324220004243700835055210324270004243400835056210324280004243100835057210324290004242E008350582103242C0004242B008350592103242D000424280083505A2103242E000424250083505B2103243A000424220083505C2103243B0004241F0083505D210324490004241C0083505E21032466000424190083505F2103246900042416008350602103246A00042413008350612103246C00042410008350622103247C0004240D00835063210324122004240A00835064210324132004240700835065210324142004240400835066210324152004240100835067210324212060000800E0030200D6260000000000000000")},
    ]
  },
  {NAME: "Fix Bullet Width", ENABLED: True, CFG_ID: "bullet_width", DATA:
    [
      {POS: 0x0009FA68, ORIG:  ConstBitStream(hex = "0x203E077C000087440402A2C40100C624600080460400A524400802464D080046000802440E0022A6000064902A10C400F3FF401400080744"),
                        PATCH: ConstBitStream(hex = "0x00008744600080460402A2C40100C624400802462A10C400FBFF40140400A5244D08004600080244FCFF42240E0022A62138400000000000")},
    ]
  },
  {NAME: "Anagram String End Fix", ENABLED: True, CFG_ID: "anagram_00", DATA:
    [
      {POS: 0x0005CEFC, ORIG: ConstBitStream(hex = "0x01"), PATCH: ConstBitStream(hex = "0x02")},
      {POS: 0x0005CEE3, ORIG: ConstBitStream(hex = "0x90"), PATCH: ConstBitStream(hex = "0x94")},
      {POS: 0x0005CF03, ORIG: ConstBitStream(hex = "0xA0"), PATCH: ConstBitStream(hex = "0xA4")},
      {POS: 0x0005CF0B, ORIG: ConstBitStream(hex = "0x90"), PATCH: ConstBitStream(hex = "0x94")},
    ]
  },
  {NAME: "CLT Tweaks", ENABLED: True, CFG_ID: "clt_tweak", DATA:
    [
      {POS: 0x00101400, ORIG: ConstBitStream(hex = "0x66E6FFFF"), PATCH: ConstBitStream(hex = "0xFFE600FF")},
      {POS: 0x00101404, ORIG: ConstBitStream(hex = "0x66E6FFFF"), PATCH: ConstBitStream(hex = "0xFFE600FF")},
      {POS: 0x00101408, ORIG: ConstBitStream(hex = "0x236EFFFF"), PATCH: ConstBitStream(hex = "0xB4640FFF")},
    ]
  },
]

def apply_sys_lang(eboot):
  
  if LANG_CFG_ID in common.editor_config.hacks:
    sys_menu_lang = common.editor_config.hacks[LANG_CFG_ID]
  else:
    sys_menu_lang = 1
    common.editor_config.hacks[LANG_CFG_ID] = sys_menu_lang
  
  patch_loc = 0x1B300
  patch = ConstBitStream(uintle = sys_menu_lang, length = 8) + ConstBitStream(hex = "0x000224")
  eboot.overwrite(patch, patch_loc * 8)
  return eboot

def extend_eboot(eboot):

  HEADER_EXTEND_POS   = 0x54
  HEADER_EXTEND_SIZE  = 0x20
  
  NEW_SECTION_POS     = 0x109700
  NEW_SECTION_SIZE    = 73696
  
  ORIG_SIZE           = 1566304
  EXTENDED_SIZE       = ORIG_SIZE + HEADER_EXTEND_SIZE + NEW_SECTION_SIZE
  
  # Already extended, don't need to do it again.
  if eboot.len / 8 == EXTENDED_SIZE:
    return eboot, HEADER_EXTEND_SIZE
  elif eboot.len / 8 != ORIG_SIZE:
    raise ValueError("EBOOT neither matches original nor extended size. Try restoring the original, decrypted EBOOT.BIN to PSP_GAME/SYSDIR, then repack everything.")
  
  eboot.insert(BitStream(length = HEADER_EXTEND_SIZE * 8), HEADER_EXTEND_POS * 8)
  eboot.insert(BitStream(length = NEW_SECTION_SIZE * 8),   NEW_SECTION_POS * 8)
  
  # Since we're adding another program segment between program segments 0 and 1,
  # we need to update references to program segment 1 on the relocation table
  # so that they point to program segment 2.
  #
  # The pseudocode for this step is:
  # 
  # For b = every 8 bytes from 0x1253E0 to the end of the file:
  #   If b[5] == 1, replace it with 2.
  #   If b[6] == 1, replace it with 2.
  TABLE_START = 0x1253E0
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