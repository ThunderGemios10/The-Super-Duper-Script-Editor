from sys import version_info
if version_info >= (2, 7, 0):
  from MeCabPy27.MeCab import *
  #print "2.7"
elif version_info >= (2, 6, 0):
  from MeCabPy26.MeCab import *
  #print "2.6"
else:
  print "Can't use this, sorry."