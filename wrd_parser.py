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

import bitstring
from bitstring import ConstBitStream
import codecs
import os.path
import sys

import common
from scene_info import SceneInfo
from sprite import SpriteId, SPRITE_TYPE
from text_printer import IMG_FILTERS
from voice import VoiceId

WRD_HEADER        = ConstBitStream(hex='0x7000')
#???              = ConstBitStream(hex='0x7001')
WRD_TEXT          = ConstBitStream(hex='0x7002')
#???              = ConstBitStream(hex='0x7003')
WRD_IMGFILTER     = ConstBitStream(hex='0x7004')
WRD_MOVIE         = ConstBitStream(hex='0x7005')
WRD_CUTIN         = ConstBitStream(hex='0x7006')
#???              = ConstBitStream(hex='0x7007')
WRD_VOICE         = ConstBitStream(hex='0x7008')
WRD_BGM           = ConstBitStream(hex='0x7009')
WRD_SFX           = ConstBitStream(hex='0x700A')
WRD_SFX2          = ConstBitStream(hex='0x700B')
WRD_AMMO          = ConstBitStream(hex='0x700C')
#???              = ConstBitStream(hex='0x700D')
#???              = ConstBitStream(hex='0x700E')
WRD_CHAR_TITLE    = ConstBitStream(hex='0x700F')

WRD_REPORT_INFO   = ConstBitStream(hex='0x7010')
#???              = ConstBitStream(hex='0x7011')
#???              = ConstBitStream(hex='0x7012')
#???              = ConstBitStream(hex='0x7013')
WRD_TRIALCAM      = ConstBitStream(hex='0x7014')
#WRD_LOADTRIAL     = ConstBitStream(hex='0x7014')
WRD_LOADNORMAL    = ConstBitStream(hex='0x7015')
#???              = ConstBitStream(hex='0x7016')
#???              = ConstBitStream(hex='0x7017')
#???              = ConstBitStream(hex='0x7018')
#???              = ConstBitStream(hex='0x7019')
#???              = ConstBitStream(hex='0x701A')
WRD_GOTOFOLDER    = ConstBitStream(hex='0x701B')
#???              = ConstBitStream(hex='0x701C')
#???              = ConstBitStream(hex='0x701D')
WRD_SPRITE        = ConstBitStream(hex='0x701E')
#???              = ConstBitStream(hex='0x701F')

#???              = ConstBitStream(hex='0x7020')
WRD_SPEAKER       = ConstBitStream(hex='0x7021')
#???              = ConstBitStream(hex='0x7022')
#???              = ConstBitStream(hex='0x7023')
#???              = ConstBitStream(hex='0x7024')
WRD_CHANGEUI      = ConstBitStream(hex='0x7025')
WRD_SETFLAG       = ConstBitStream(hex='0x7026')
WRD_CHECKCHAR     = ConstBitStream(hex='0x7027')
#???              = ConstBitStream(hex='0x7028')
WRD_CHECKOBJ      = ConstBitStream(hex='0x7029')
WRD_SETLABEL      = ConstBitStream(hex='0x702A')
WRD_CHOICE        = ConstBitStream(hex='0x702B')
#???              = ConstBitStream(hex='0x702C')
#???              = ConstBitStream(hex='0x702D')
#???              = ConstBitStream(hex='0x702E')
#???              = ConstBitStream(hex='0x702F')

WRD_BGD           = ConstBitStream(hex='0x7030')
#???              = ConstBitStream(hex='0x7031')
#???              = ConstBitStream(hex='0x7032')
#???              = ConstBitStream(hex='0x7033')
WRD_GOTOLABEL     = ConstBitStream(hex='0x7034')
WRD_CHECKFLAG     = ConstBitStream(hex='0x7035')
#???              = ConstBitStream(hex='0x7036')
#???              = ConstBitStream(hex='0x7037')
#???              = ConstBitStream(hex='0x7038')
#???              = ConstBitStream(hex='0x7039')
WRD_WAIT          = ConstBitStream(hex='0x703A')
WRD_WAIT_FRAME    = ConstBitStream(hex='0x703B')
WRD_FLAGCHECK_END = ConstBitStream(hex='0x703C')
#???              = ConstBitStream(hex='0x703D')
#???              = ConstBitStream(hex='0x703E')
#???              = ConstBitStream(hex='0x703F')

unparsed_cmds = {}

def parse_wrd(in_file):
  
  # Magic
  wrd = ConstBitStream(filename = in_file)
  
  header = wrd.read(16)
  
  if header != WRD_HEADER:
    print "Not a valid wrd file"
    return None
  
  num_files = wrd.read('uintle:16')
  
  if num_files == 0:
    print "No text files referenced in this wrd file."
    return None
  
  cur_speaker   = 0x1F
  cur_sprite    = SpriteId()
  last_sprite   = -1
  cur_voice     = VoiceId()
  cur_bgm       = -1
  cur_trialcam  = None
  cur_portrait  = None
  is_option     = False
  is_option_pt  = False
  option_val    = None
  is_floating   = False
  show_tag      = True
  is_speaking   = True
  
  img_filter    = False
  
  cur_mode      = None
  cur_room      = -1
  
  cur_object    = -1
  
  cur_ammo      = -1
  cur_cutin     = -1
  cur_bgd       = -1
  cur_flash     = -1
  cur_movie     = -1
  
  # Because we can put flashes on top of flashes.
  flash_stack  = []
  
  # If we set the speaker with a speaker tag,
  # don't let a voice file/sprite override it.
  speaker_set = False
  
  loaded_sprites = {}
  
  box_color = common.BOX_COLORS.orange
  box_type  = common.BOX_TYPES.normal
  
  wrd_info = []
  
  # All commands start with 0x70, and have a second byte that signifies what they actually do.
  commands = wrd.findall('0x70', start = wrd.pos, bytealigned = True)
  
  for command_pos in commands:
    if wrd.pos > command_pos:
      continue
    
    wrd.pos = command_pos
    
    command = wrd.read(16)
    
    if command == WRD_CHANGEUI:
      # 70 25 XX YY <-- Change UI Elements?
      #   * XX YY
      #     * 00 00 = "Speaking" window
      #     * 00 01 = "Thoughts" window
      #     * 01 00 = Hide text box (?)
      #     * 01 01 = Show text box (?)
      #     * 02 00 = Hide nametag (?)
      #     * 02 01 = Show nametag (?)
      #     * 03 00 = Orange box (?)
      #     * 03 01 = Green box (?)
      #     * 03 02 = Blue box (?)
      #     * 04 YY = ??
      #     * 06 YY = ??
      #     * 07 YY = ??
      #     * 09 YY = ??
      #     * 0B YY = ??
      #     * 0D 00 = Stop shaking
      #     * 0D 01 = Start shaking
      #     * 33 00 = Normal, round text box (?)
      #     * 33 01 = Flat, black overlay (?)
      element = wrd.read('uint:8')
      state   = wrd.read('uint:8')
      
      # Text box
      if element == 0x00:
        if state == 0x00:
          is_speaking = True
        elif state == 0x01:
          is_speaking = False
        
        show_tag = True
      
      # Text box
      elif element == 0x01:
        if state == 0x00:
          # Is it safe to assume that when we kill the text box
          # we are also killing any existing BGDs and the like?
          #cur_bgd   = -1
          #cur_cutin = -1
          #cur_flash = -1
          #cur_movie = -1
          #cur_ammo  = -1
          pass
      
      # Speaker tag
      elif element == 0x02:
        if state == 0x00:
          show_tag = False
        elif state == 0x01:
          show_tag = True
      
      # Box color -- not really
      #elif element == 0x03:
        #if state == 0x00:
          #box_color = common.BOX_COLORS.orange
        #elif state == 0x01:
          #box_color = common.BOX_COLORS.green
        #elif state == 0x02:
          #box_color = common.BOX_COLORS.blue
      
      # Box type
      elif element == 0x33:
        if state == 0x00:
          box_type = common.BOX_TYPES.normal
        elif state == 0x01:
          box_type = common.BOX_TYPES.flat
    
    elif command == WRD_LOADNORMAL:
      # 70 15 XX YY FF <-- Load map XX in regular mode (?)
      #   * YY = Load/Show (?)
      #     * 00 = Show
      #     * 01 = Load
      room = wrd.read('uint:8')
      state = wrd.read('uint:8')
      wrd.read(8)
      
      if state == 0:
        cur_room = room
        cur_mode = common.SCENE_MODES.normal
        
    elif command == WRD_CHECKCHAR:
      # 70 27 XX -- Check object XX
      cur_object = wrd.read('uint:8')
    
    elif command == WRD_CHECKOBJ:
      # 70 29 XX -- Check object XX
      cur_object = wrd.read('uint:8')
    
    elif command == WRD_CHOICE:
      # 70 2B XX <-- Choice stuff?
      #   * XX = ??
      #     * 01 = Choice ID (?)
      #     * 02 = Choice ID (?)
      #     * 03 = Choice ID (?)
      #     * 12 = Out of time (?)
      #     * 13 = Options prompt (?)
      #     * FF = End of options section (?)
      option_flag = wrd.read('uint:8')
      
      if option_flag == 0x13:
        is_option_pt = True
        is_option    = False
        option_val   = "Prompt"
      
      elif option_flag == 0x12:
        is_option_pt = True
        is_option    = False
        option_val   = "Time Up"
      
      elif option_flag == 0xFF:
        is_option_pt = False
        is_option = False
        
      elif option_flag < 0x10:
        is_option = True
        is_option_pt = False
        option_val = option_flag
      
    elif command == WRD_TRIALCAM:
      # 70 14 XX YY ZZ
      #   * XX = ID of character we're pointing at
      #   * YY = ??
      #   * ZZ = The motion used to move the camera there?
      char_id = wrd.read('uint:8')
      wrd.read(16)
      
      cur_trialcam = char_id
      
      if not char_id in loaded_sprites:
        cur_sprite = SpriteId()
      else:
        cur_sprite = loaded_sprites[char_id]
      
    elif command == WRD_SPRITE:
      # 70 1E WW XX YY ZZ VV <-- Change sprite
      #   * WW = Portrait ID?
      #   * XX = Char ID
      #   * YY = Sprite #
      #   * ZZ = Sprite state?
      #     * 00 = Kill (?)
      #     * 01 = Show (?)
      #     * 03 = Fade out (?)
      #     * 04 = Hide (?)
      #   * VV = Sprite type?
      #   * Speaker tag + textbox set to "speaking" automatically?
      portrait_id  = wrd.read('uint:8')
      char_id      = wrd.read('uint:8')
      sprite_id    = wrd.read('uint:8')
      sprite_state = wrd.read('uint:8')
      sprite_type  = wrd.read('uint:8')
      
      cur_portrait = portrait_id
      
      sprite_info = SpriteId(SPRITE_TYPE.bustup, char_id, sprite_id)
      loaded_sprites[char_id] = sprite_info
      
      last_sprite = char_id
      
      # If we have a camera, that means we might not be showing a sprite
      # just because we loaded it. Wait for the camera flag to point at a sprite.
      if cur_trialcam == None:
        if sprite_state in [0x00, 0x03, 0x04, 0x05, 0x07, 0x0A]:
          cur_sprite = SpriteId()
          continue
        else:
          cur_sprite = sprite_info
      
      if not speaker_set:
        cur_speaker = char_id
        
    elif command == WRD_VOICE:
      # 70 08 XX YY ZZ ZZ 64 <-- Play Voice
      #   * XX    = Char ID
      #   * YY    = Chapter ID
      #     * 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, or 0x63
      #       The first six represent Class Trial numbers, and the last one is for misc voices.
      #   * ZZ ZZ = Voice ID
      char_id = wrd.read('uint:8')
      chapter = wrd.read('uint:8')
      voice_id = wrd.read('uint:16')
      wrd.read(8)
      
      cur_voice = VoiceId(char_id, chapter, voice_id)
      
      if not speaker_set:
        cur_speaker = char_id
    
    elif command == WRD_BGM:
      # 70 09 XX YY 00 <-- Play Voice
      #   * XX    = BGM ID
      #     * 0xFF = Off
      #   * YY    = Transition (?)
      #     * 0x00 = Stop
      #     * 0x3C = Fade Out
      #     * 0x64 = Fade In
      bgm_id     = wrd.read('uint:8')
      transition = wrd.read('uint:8')
      wrd.read(8)
      
      if bgm_id == 0xFF:
        cur_bgm = -1
      
      else:
        cur_bgm = bgm_id
    
    elif command == WRD_SFX or command == WRD_SFX2:
      # 70 0A XX YY <-- Play SFX
      # 70 0B XX YY <-- Play SFX
      #   * XX    = SFX ID
      #     * 0xFF = Off
      #   * YY    = Transition (?)
      #     * 0x00 = Stop
      #     * 0x3C = Fade Out
      #     * 0x64 = Fade In
      sfx_id     = wrd.read('uint:8')
      transition = wrd.read('uint:8')
      
      if sfx_id == 0xFF:
        cur_sfx = -1
      
      else:
        cur_sfx = sfx_id
    
    elif command == WRD_CHAR_TITLE:
      # 70 0F XX 00 YY
      #   * XX = Title status
      #     * 0x00 = Default title
      #     * 0x01 = Alternate title
      #   * YY = Char ID
      title_status = wrd.read("uint:8")
      wrd.read(8)
      char_id      = wrd.read("uint:8")
    
    elif command == WRD_REPORT_INFO:
      # 70 10 XX 00 YY
      #   * XX = Char ID
      #   * YY = # of pieces of info known
      char_id    = wrd.read("uint:8")
      wrd.read(8)
      info_known = wrd.read("uint:8")
      
    elif command == WRD_SPEAKER:
      # 70 21 XX <-- Change speaker tag
      #   * XX = Char ID
      char_id = wrd.read('uint:8')
      
      if char_id in common.CHAR_IDS:
        cur_speaker = char_id
        speaker_set = True
      elif char_id == 0x1C:
        cur_speaker = last_sprite
        speaker_set = True
    
    elif command == WRD_BGD:
      # 70 30 XX XX YY
      #   * XX XX = BGD ID
      #   * YY    = Show/hide
      #     * 01 = Show
      #     * 03 = Hide (?)
      
      bgd_id = wrd.read('uint:16')
      bgd_state = wrd.read('uint:8')
      
      # Clear everything first, since a new call takes
      # priority of display over an old call.
      cur_bgd   = -1
      cur_flash = -1
      cur_movie = -1
      
      if bgd_state == 1:
        cur_bgd = bgd_id
        
        cur_trialcam = None
        cur_sprite = SpriteId()
    
    elif command == WRD_CUTIN:
      # 70 06 XX XX 00 00 00 00 00 YY
      #   * XX XX = 0x0BB8 + Cutin ID (base 10: 3000 + Cutin ID)
      #     * if < 1000 (base 10), then it's a flash event.
      #     * I've seen numbers between 1000 and 3000, but I'm not sure what they're for.
      #   * YY = Show/hide
      #     * 01 = Show
      #     * 02 = Hide
      #     * 03 = Load/prepare flash (?)
      #     * FF = Hide flash (?)
      
      cutin_id = wrd.read('uint:16')
      wrd.read(40)
      cutin_state = wrd.read('uint:8')
      
      # An actual cutin.
      if cutin_id >= 3000:
        if cutin_state == 1:
          cur_cutin = cutin_id - 3000
        else:
          cur_cutin = -1
      
      # A flash event.
      elif cutin_id < 1000:
      
        # Clear other stuff first, since a new call takes
        # priority of display over an old call.
        cur_bgd   = -1
        cur_movie = -1
        
        # These flash IDs are special trial animations that kind of screw things up.
        invalid_flash = [500, 501, 502, 503]
        
        if (cutin_state in [1, 3, 4]) and (cutin_id not in invalid_flash):
          #cur_flash = cutin_id
          if cutin_id in flash_stack:
            flash_stack.remove(cutin_id)
          
          flash_stack.append(cutin_id)
        elif cutin_state == 0xFF and len(flash_stack) > 0:
          if cutin_id in flash_stack:
            flash_stack.remove(cutin_id)
          else:
            flash_stack.pop()
          #cur_flash = -1
        
        if len(flash_stack) == 0:
          cur_flash = -1
        else:
          cur_flash = flash_stack[-1]
          cur_trialcam = None
          cur_sprite = SpriteId()
    
    elif command == WRD_AMMO:
      # 70 0C XX YY
      #   * XX = Ammo ID
      #   * YY = Status
      #     * 00 = If ID == 0xFF & status == 0x00, clear all ammo from ElectroiD
      #     * 01 = Add to ElectroiD
      #     * 02 = Update info
      
      ammo_id    = wrd.read("uint:8")
      ammo_state = wrd.read("uint:8")
      
      if ammo_state == 1:
        cur_ammo = ammo_id
      else:
        cur_ammo = -1
    
    elif command == WRD_MOVIE:
      # 70 05 XX YY
      #   * XX = Movie ID
      #   * YY = Show/hide
      #     * 01 = Show
      #     * ?? = Hide
      
      movie_id = wrd.read('uint:8')
      movie_state = wrd.read('uint:8')
      
      # Clear everything first, since a new call takes
      # priority of display over an old call.
      cur_bgd   = -1
      cur_flash = -1
      cur_movie = -1
      
      if movie_state == 1:
        cur_movie = movie_id
    
    elif command == WRD_SETFLAG:
      # 70 26 XX YY XX
      #   * XX = Flag group
      #   * YY = Flag ID
      #   * ZZ = Flag State
      #     * 00 = Off
      #     * 01 = On
      
      flag_group = wrd.read('uint:8')
      flag_id    = wrd.read('uint:8')
      flag_state = wrd.read('uint:8')
      #print '0x%04X -> %d' % (flag_id, flag_state)
    
    elif command == WRD_CHECKFLAG:
      # 70 35 XX XX 00 YY 
      #   * If there are multiple flags (as many as needed)
      #   -> WW XX XX 00 YY 
      #
      #   * When all the flags have been listed.
      #   -> 70 3C 70 34 ZZ ZZ
      #
      #   * XX XX = Flag group/ID
      #   * YY = Flag State
      #     * 00 00 = Off
      #     * 00 01 = On
      #
      #   * WW = Operator
      #     * 06 = AND
      #     * 07 = OR  (?)
      #
      #   * ZZ ZZ = Label to jump to if check failed.
      
      flags = []
      flag_ops = []
      
      while True:
        flag_group = wrd.read('uint:8')
        flag_id    = wrd.read('uint:8')
        flag_state = wrd.read('uint:8')
        
        # Some weird edge cases where the flag marker is only three bytes?
        # Only cases I've seen:
        # 70 35 0C 00 01 70 3C 70 34 01 F6 -> !e03_021_103.scp.wrd
        # 70 35 14 00 09 70 3C 70 34 01 F4 -> !e05_000_141.scp.wrd
        # 70 35 0F 1B 01 70 3C 70 2A 01 F7 -> !e06_007_152.scp.wrd
        if flag_state == 0:
          flag_state = wrd.read('uint:8')
        flags.append((flag_group, flag_id, flag_state))
        
        if wrd.peek('uint:8') in [0x06, 0x07]:
          operator = wrd.read('uint:8')
          if operator == 0x06:
            flag_ops.append('&&')
          elif operator == 0x07:
            flag_ops.append('||')
        else:
          break
      
      end_cmd  = wrd.read(16)
      if not end_cmd == WRD_FLAGCHECK_END:
        print "Invalid flag check.", end_cmd
        flags = []
        continue
      
      jump_cmd = wrd.peek(16)
      if not jump_cmd == WRD_GOTOLABEL:
        print "No jump command after flag check.", jump_cmd
        #continue
      else:
        wrd.read(16)
        fail_label = wrd.read('uint:16')
      
      check_str = ["if"]
      for i, flag in enumerate(flags):
        if flag[2] == 0:
          check_str.append("not")
        check_str.append('0x%02X%02X' % (flag[0], flag[1]))
        
        if i < len(flag_ops):
          check_str.append(flag_ops[i])
      check_str = ' '.join(check_str)
      # print check_str
    
    elif command == WRD_IMGFILTER:
      # 70 04 01 XX 00 00
      #   * 00 = Unfiltered
      #   * 01 = Sepia
      #   * 05 = Inverted
      
      wrd.read(8)
      filter = wrd.read('uint:8')
      wrd.read(16)
      
      if filter == 0x00:
        img_filter = IMG_FILTERS.unfiltered
      elif filter == 0x01:
        img_filter = IMG_FILTERS.sepia
      elif filter == 0x05:
        img_filter = IMG_FILTERS.inverted
      else:
        img_filter = IMG_FILTERS.unfiltered
        #try:
          #print wrd_info[-1].file_id,
        #except: pass
        #print "Unknown filter! 0x%x" % filter
    
    elif command == WRD_GOTOFOLDER:
      # 70 1B XX YY ZZ
      #   * XX = Chapter
      #   * YY = Scene
      #   * ZZ = Room
      
      # Probably nothing we can really do with this right now.
      goto_chapter = wrd.read('uint:8')
      goto_scene   = wrd.read('uint:8')
      goto_room    = wrd.read('uint:8')
    
    elif command == WRD_SETLABEL:
      # 70 2A XX XX
      # * XX XX = Label ID
      label_id     = wrd.read('uint:16')
    
    elif command == WRD_GOTOLABEL:
      # 70 34 XX XX
      # * XX XX = Label ID
      label_id     = wrd.read('uint:16')
    
    elif command == WRD_WAIT:
      # 70 3A
      # No parameters. Just tells the script to wait for button press.
      pass
    
    elif command == WRD_WAIT_FRAME:
      # 70 3B
      # No parameters. Just tells the script to wait for a frame.
      pass
      
    elif command == WRD_TEXT:
      # 70 02 XX XX
      # * XX XX = Text file index
      file_index = wrd.read('uint:16')
      
      scene_info = SceneInfo()
      scene_info.file_id = file_index
      
      if not cur_mode == None:
        scene_info.mode = cur_mode
      
      scene_info.room = cur_room
      
      if not show_tag:
        scene_info.speaker = -1
      else:
        scene_info.speaker = cur_speaker
      
      scene_info.speaking   = is_speaking
      scene_info.sprite     = cur_sprite
      scene_info.voice      = cur_voice
      scene_info.bgm        = cur_bgm
      
      scene_info.box_color  = box_color
      scene_info.box_type   = box_type
      
      scene_info.ammo       = cur_ammo
      scene_info.bgd        = cur_bgd
      scene_info.cutin      = cur_cutin
      scene_info.flash      = cur_flash
      scene_info.movie      = cur_movie
      
      scene_info.img_filter = img_filter
      
      if not cur_object == -1:
        scene_info.special    = common.SCENE_SPECIAL.checkobj
        scene_info.extra_val  = cur_object
        cur_object            = -1
      
      if is_option_pt:
        scene_info.special = common.SCENE_SPECIAL.showopt
        scene_info.extra_val = option_val
      elif is_option:
        scene_info.speaker = -1
        scene_info.special = common.SCENE_SPECIAL.option
        scene_info.extra_val = option_val
      
      #scene_info.trialcam = cur_trialcam
      #scene_info.nonstop = is_floating
      
      ##############################
      ### RESET STUFF
      ##############################
      
      cur_ammo = -1
      
      scene_info.headshot = cur_portrait
      
      if is_option:
        is_option = False
        option_val = None
      
      #is_option_pt = False
      is_floating = False
      speaker_set = False
      
      cur_voice = VoiceId()
      
      wrd_info.append(scene_info)
    
    else:
      try:
        unparsed_cmds[command.hex] += 1
      except:
        unparsed_cmds[command.hex] = 1
  
  return wrd_info
  
if __name__ == "__main__":

  #input_file = ""
  #file_num = None

  #if len(sys.argv) > 1:
    #input_file = sys.argv[1].decode(sys.stdin.encoding)
    
  #else:
    #print "No file provided."
    #exit()
  
  #parse_wrd(input_file)
  
  import glob
  import pprint
  
  for file in glob.iglob("X:/Danganronpa/Danganronpa_BEST/umdimage/*/*.scp.wrd"):
    print file
    parse_wrd(file)
    print
    print "----------------------------------------"
    print
  
  pp = pprint.PrettyPrinter()
  pp.pprint(unparsed_cmds)

### EOF ###