﻿################################################################################
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

CMD_MARKER = 0x70

WRD_HEADER          = 0x00
#???                = 0x01
WRD_SHOW_LINE       = 0x02
WRD_CLT             = 0x03
WRD_FILTER_IMG      = 0x04
WRD_MOVIE           = 0x05
WRD_FLASH           = 0x06
#???                = 0x07
WRD_VOICE           = 0x08
WRD_BGM             = 0x09
WRD_SFX_A           = 0x0A
WRD_SFX_B           = 0x0B
WRD_SET_AMMO        = 0x0C
#???                = 0x0D
#???                = 0x0E
WRD_CHAR_TITLE      = 0x0F

WRD_REPORT_INFO     = 0x10
#???                = 0x11
#???                = 0x12
#???                = 0x13
WRD_TRIAL_CAM       = 0x14
WRD_LOAD_MAP        = 0x15
#???                = 0x16
#???                = 0x17
#???                = 0x18
WRD_GOTO_SCRIPT     = 0x19
#???                = 0x1A
WRD_CALL_SCRIPT     = 0x1B
#???                = 0x1C
#???                = 0x1D
WRD_SPRITE          = 0x1E
#???                = 0x1F

#???                = 0x20
WRD_SPEAKER         = 0x21
#???                = 0x22
#???                = 0x23
#???                = 0x24
WRD_CHANGE_UI       = 0x25
WRD_SET_FLAG        = 0x26
WRD_CHECK_CHAR      = 0x27
#???                = 0x28
WRD_CHECK_OBJ       = 0x29
WRD_SET_LABEL       = 0x2A
WRD_CHOICE          = 0x2B
#???                = 0x2C
#???                = 0x2D
#???                = 0x2E
#???                = 0x2F

WRD_BGD             = 0x30
#???                = 0x31
#???                = 0x32
#???                = 0x33
WRD_GOTO_LABEL      = 0x34
WRD_CHECKFLAG_A     = 0x35
WRD_CHECKFLAG_B     = 0x36
#???                = 0x37
#???                = 0x38
#???                = 0x39
WRD_WAIT_INPUT      = 0x3A
WRD_WAIT_FRAME      = 0x3B
WRD_FLAG_CHECK_END  = 0x3C
#???                = 0x3D
#???                = 0x3E
#???                = 0x3F

WRD_INVALID         = 0xFFFF

OP_PARAMS = {

  WRD_HEADER:         [("lines", "uintle:16")],
  0x01:               [(None, "uint:8")] * 3,
  WRD_SHOW_LINE:      [("line",  "uint:16")],
  WRD_CLT:            [("clt", "uint:8")], # Something to do with CLT'd text
  WRD_FILTER_IMG:     [("unk1", "uint:8"), ("filter", "uint:8"), ("unk2", "uint:16")],
  WRD_MOVIE:          [("id", "uint:8"), ("state", "uint:8"), ],
  WRD_FLASH:          [("id", "uint:16"), ("padding", "uint:32"), ("unk", "uint:8"), ("state", "int:8")],
  WRD_VOICE:          [("char_id", "uint:8"), ("chapter", "uint:8"), ("voice_id", "uint:16"), ("unk", "uint:8")],
  WRD_BGM:            [("id", "int:8"), ("transition", "uint:8"), ("unk", "uint:8")],
  WRD_SFX_A:          [("id", "uint:16"), ("volume", "uint:8")],
  WRD_SFX_B:          [("id", "uint:8"), ("volume", "uint:8")],
  WRD_SET_AMMO:       [("id", "uint:8"), ("state", "uint:8")],
  0x0D:               [(None, "uint:8")] * 3, # Something to do with presents
  0x0E:               [(None, "uint:8")] * 2, 
  WRD_CHAR_TITLE:     [("id", "uint:8"), ("unk", "uint:8"), ("title", "uint:8")],
  WRD_REPORT_INFO:    [("id", "uint:8"), ("unk", "uint:8"), ("info_known", "uint:8")],
  0x11:               [(None, "uint:8")] * 4, # Something to do with multiple-choice
  WRD_TRIAL_CAM:      [("char_id", "uint:8"), ("unk", "uint:8"), ("motion", "uint:8")],
  WRD_LOAD_MAP:       [("room", "uint:8"), ("state", "uint:8"), ("padding", "uint:8")],
  WRD_GOTO_SCRIPT:    [("chapter", "uint:8"), ("scene", "uint:8"), ("room", "uint:8")],
  0x1A:               [], # Cleanup?
  WRD_CALL_SCRIPT:    [("chapter", "uint:8"), ("scene", "uint:8"), ("room", "uint:8")],
  0x1C:               [], # Cleanup?
  WRD_SPRITE:         [("obj_id", "uint:8"), ("char_id", "uint:8"), ("sprite_id", "uint:8"), ("sprite_state", "uint:8"), ("sprite_type", "uint:8")],
  0x1F:               [(None, "uint:8")] * 7, # Screen flash effect?
  0x20:               [(None, "uint:8")] * 5,
  WRD_SPEAKER:        [("id", "uint:8")],
  0x22:               [(None, "uint:8")] * 3,
  0x23:               [(None, "uint:8")] * 5,
  WRD_CHANGE_UI:      [("element", "uint:8"), ("state", "uint:8")],
  WRD_SET_FLAG:       [("group", "uint:8"), ("id", "uint:8"), ("state", "uint:8")],
  WRD_CHECK_CHAR:     [("id", "uint:8")],
  WRD_CHECK_OBJ:      [("id", "uint:8")],
  WRD_SET_LABEL:      [("id", "uint:16")],
  WRD_CHOICE:         [("flag", "uint:8")],
  0x2E:               [(None, "uint:8")] * 2,
  WRD_BGD:            [("id", "uint:16"), ("state", "uint:8")],
  0x33:               [(None, "uint:8")] * 4, # Set values checked by WRD_CHECKFLAG_B?
  WRD_GOTO_LABEL:     [("id", "uint:16")],
  WRD_CHECKFLAG_A:    "parse_checkflag_a",
  WRD_CHECKFLAG_B:    "parse_checkflag_b",
  0x38:               [(None, "uint:8")] * 5,
  0x39:               [(None, "uint:8")] * 5,
  WRD_WAIT_INPUT:     [],
  WRD_WAIT_FRAME:     "parse_wait_frame",
  WRD_FLAG_CHECK_END: [],
  WRD_INVALID:        "byte",

}

OP_FUNCTIONS = {

  # WRD_HEADER:         None,
  0x01:               None,
  WRD_SHOW_LINE:      "show_line",
  WRD_CLT:            "clt",
  WRD_FILTER_IMG:     "filter_img",
  WRD_MOVIE:          "play_movie",
  WRD_FLASH:          "show_flash",
  WRD_VOICE:          "play_voice",
  WRD_BGM:            "play_bgm",
  WRD_SFX_A:          "play_sfx_a",
  WRD_SFX_B:          "play_sfx_b",
  WRD_SET_AMMO:       "set_ammo",
  0x0D:               None,               # Something to do with presents
  0x0E:               None,
  WRD_CHAR_TITLE:     "set_title",
  WRD_REPORT_INFO:    "set_report_info",
  0x11:               None,               # Something to do with multiple-choice
  WRD_TRIAL_CAM:      "trial_cam",
  WRD_LOAD_MAP:       "load_map",
  WRD_GOTO_SCRIPT:    "goto_script",
  0x1A:               None,               # Cleanup?
  WRD_CALL_SCRIPT:    "call_script",
  0x1C:               None,               # Cleanup?
  WRD_SPRITE:         "show_sprite",
  0x1F:               None,               # Screen flash effect?
  0x20:               None,
  WRD_SPEAKER:        "set_speaker",
  0x22:               None,
  0x23:               None,
  WRD_CHANGE_UI:      "change_ui",
  WRD_SET_FLAG:       "set_flag",
  WRD_CHECK_CHAR:     "check_char",
  WRD_CHECK_OBJ:      "check_obj",
  WRD_SET_LABEL:      "set_label",
  WRD_CHOICE:         "choice",
  0x2E:               None, 
  WRD_BGD:            "show_bgd",
  0x33:               None, 
  WRD_GOTO_LABEL:     "goto_label",
  WRD_CHECKFLAG_A:    "check_flag_a",
  WRD_CHECKFLAG_B:    "check_flag_b",
  0x38:               None,
  0x39:               None,
  WRD_WAIT_INPUT:     "wait_for_input",
  WRD_WAIT_FRAME:     "wait_frames",
  WRD_FLAG_CHECK_END: "flag_check_end",
  WRD_INVALID:        "byte",             # For anything that doesn't parse correctly

}

### EOF ###