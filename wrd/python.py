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

from collections import OrderedDict
import functools

from wrd.ops import *

################################################################################
### CONSTANTS
################################################################################
SECTION_SEP = "#" * 80
WRD_NAME    = "wrd"

CHAR_IDS = {
  "NAEGI":            0x00,
  "ISHIMARU":         0x01,
  "TOGAMI":           0x02,
  "OOWADA":           0x03,
  "KUWATA":           0x04,
  "YAMADA":           0x05,
  "HAGAKURE":         0x06,
  "MAIZONO":          0x07,
  "KIRIGIRI":         0x08,
  "ASAHINA":          0x09,
  "FUKAWA":           0x0A,
  "OOGAMI":           0x0B,
  "CELES":            0x0C,
  "ENOSHIMA":         0x0D,
  "FUJISAKI":         0x0E,
  "MONOKUMA":         0x0F,
  "ENOSHIMA_REAL":    0x10,
  "ALTER_EGO":        0x11,
  "GENOCIDER":        0x12,
  "HEADMASTER":       0x13,
  "NAEGI_MOTHER":     0x14,
  "NAEGI_FATHER":     0x15,
  "NAEGI_SISTER":     0x16,
  "ISHIMARU_OOWADA":  0x18,
  "DAIA_OOWADA":      0x19,
  "LAST_SPRITE":      0x1C,
  "NO_NAME":          0x1E,
  "NARRATION":        0x1F,
}

CHAR_IDS_R = {v:k for k, v in CHAR_IDS.iteritems()}

USE_CHAR_IDS = {
  WRD_VOICE:          ["char_id"],
  WRD_CHAR_TITLE:     ["id"],
  WRD_REPORT_INFO:    ["id"],
  WRD_TRIAL_CAM:      ["char_id"],
  WRD_SPRITE:         ["char_id"],
  WRD_SPEAKER:        ["id"],
}

################################################################################
### A meta-ish class that converts Pythonized wrd commands down to our internal
### wrd data format which can be used in all the other functions in this module.
################################################################################
class WrdPython:
  def __init__(self):
    self.commands = []
    
    # self.gen_functions()
  
  ##############################################################################
  ### Generates lambdas for functions that don't have special definitions.
  ##############################################################################
  def gen_functions(self):
    
    # Generate function aliases for anything that isn't already defined.
    for opcode in OP_FUNCTIONS:
      name = OP_FUNCTIONS[opcode]
      
      if name == None:
        continue
      
      vars(self)[name] = functools.partial(self.op, opcode)
  
  ##############################################################################
  ### A generic opcode converter using the format information in OP_PARAMS.
  ##############################################################################
  def op(self, op, *args, **kwargs):
    if op == WRD_HEADER:
      return
    
    if not op in OP_PARAMS:
      raise Exception("Unknown op: 0x%02X" % op)
      
    param_info = OP_PARAMS[op]
    fn_name = OP_FUNCTIONS[op]
    
    # Make our params match the format created by the parser.
    params = OrderedDict()
    
    # If we don't have a special function name, obviously we won't have
    # any keyword arguments. That doesn't make any sense.
    if fn_name == None:
      if len(args) > 0:
        params[None] = args
    
    # If we *do* have a function name, do a little magic so these functions
    # won't explode if argument names were omitted for whatever reason.
    else:
      # If it has a custom parsing function, just take the params as-is.
      if isinstance(param_info, basestring):
        params   = kwargs
        new_args = args
      
      else:
        new_args = []
        
        # Loop through the params by name so we have them in order.
        # Any unnamed arguments we have in a position with a name,
        # we assign that name, otherwise we put it into new_args.
        for i in range(len(param_info)):
          param_name = param_info[i][0]
          if param_name == None:
            new_args.append(args[i])
          
          else:
            try:
              params[param_name] = args[i] if i < len(args) else kwargs[param_name]
            except:
              raise TypeError("%s() missing keyword argument %s" % (fn_name, param_name))
      
      if len(args) > 0:
        params[None] = new_args
      
    self.commands.append((op, params))

################################################################################
### Generates the header, including a list of all the function definitions,
### all the constants needed 
################################################################################
def gen_header():
  header = [SECTION_SEP, "### FUNCTION DEFINITIONS", "### "]
  fns    = [SECTION_SEP, "", "%s = WrdPython()" % WRD_NAME, ""]
  
  for op in sorted(OP_FUNCTIONS.keys()):
    name = OP_FUNCTIONS[op]
    if name == None:
      continue
    
    fns.append("%s.%s = functools.partial(%s.op, 0x%02X)" % (WRD_NAME, name, WRD_NAME, op))
    
    param_info = OP_PARAMS[op]
    if isinstance(param_info, basestring):
      if op == WRD_WAIT_FRAME:
        fn_def = "frames = uint"
      elif op == WRD_CHECKFLAG_A:
        fn_def = "flags = list(tuple(group = uint:8, id = uint:8, state = uint:16)), flag_ops = list(uint:8), fail_label = uint:16"
      elif op == WRD_CHECKFLAG_B:
        fn_def = "flags = list(tuple(uint:8, uint:8, uint:8, uint:8, uint:8)), flag_ops = list(uint:8), fail_label = uint:16"
      else:
        continue
    else:
      fn_def = ', '.join(["%s = %s" % param for param in OP_PARAMS[op]])
    
    line = "### Opcode 0x%02X: %s(%s)" % (op, name, fn_def)
    header.append(line)
  
  header.extend(fns)
  
  header.extend(["", SECTION_SEP, "### CONSTANTS", SECTION_SEP, ""])
  for val in sorted(CHAR_IDS_R.keys()):
    header.append("%s = 0x%02X" % (CHAR_IDS_R[val], val))
  
  header.extend(["", SECTION_SEP, "### CODE", SECTION_SEP, ""])
  
  return '\n'.join(header)

################################################################################
### Converts a list of commands to Python.
################################################################################
def to_python(commands):
  out_lines = [gen_header()]
  
  for op, params in commands:
  
    # Some commands we'd like to put a linespace/comments before.
    if op in [WRD_CHECK_CHAR, WRD_CHECK_OBJ]:
      if not out_lines[-1] == "":
        out_lines.append("")
      out_lines.append(SECTION_SEP)
      out_lines.append("")
    
    elif op in [WRD_CHOICE, WRD_SET_LABEL] and not out_lines[-1] == "":
      out_lines.append("")
    
    line = "%s." % WRD_NAME
    
    fn_name = OP_FUNCTIONS[op]
    param_list = []
    
    if fn_name == None:
      fn_name = "op"
      param_list.append("0x%02X" % op)
    
    line += "%s(" % fn_name
    
    # Put our unnamed parameters first, because Python syntax rules.
    if None in params:
      param_list.extend(["0x%02X" % param for param in params[None]])
    
    # Then put our named parameters afterwards.
    for param_name in params:
      
      # Which obviously means skipping the unnamed ones.
      if param_name == None:
        continue
      
      if op in USE_CHAR_IDS and param_name in USE_CHAR_IDS[op] and params[param_name] in CHAR_IDS_R:
        param_val = CHAR_IDS_R[params[param_name]]
      else:
        param_val = params[param_name]
      
      param_list.append("%s = %s" % (param_name, param_val))
    
    # Function all done.
    line += ", ".join(param_list) + ")"
    out_lines.append(line)
    
    # Some commands we'd like to put a linespace after.
    if op in [WRD_WAIT_INPUT, WRD_GOTO_LABEL]:
      out_lines.append("")
  
  return '\n'.join(out_lines)

################################################################################
### Runs a converted Python script and returns the list of commands.
################################################################################
def from_python(script):
  local_dict = {}
  exec script in {'__builtins__': {}, 'WrdPython': WrdPython, 'True': True, 'False': False, 'functools': functools}, local_dict
  return local_dict[WRD_NAME].commands

### EOF ###