#!/usr/bin/env python3

import sys, signal, time, json, os
from ChirimbolitoDisplay import ChirimbolitoDisplay

class Chirimbolito(object):

  def sigintHandler(self, signal, frame):
    '''Print a message and cleanup the display before exit'''
    self.lcd.clear()
    self.lcd.message('Interrupted,\nshutting down.')
    time.sleep(2)
    self.lcd.clear()
    self.lcd.set_backlight(0)
    try:
      sys.exit(0)
    except SystemExit:
      os._exit(0)

  def __init__(self):
    # register the handler
    signal.signal(signal.SIGINT, self.sigintHandler)
    signal.signal(signal.SIGTERM, self.sigintHandler)

    self.loadConfig()
    self.display = ChirimbolitoDisplay(self.configuration)
    self.lcd = self.display.lcd
    self.lastTime = time.time()
    self.display.initInfo()
    self.main()

  def loadConfig(self):
    '''Try to read the config file'''
    filePath = os.path.join(os.path.expanduser('~'), '.config/chirimbolito.json')
    try:
      self.configuration = json.load(open(filePath))
    except IOError:
      print "Error: %s file not found" % filePath
      try:
        sys.exit(0)
      except SystemExit:
        os._exit(0)

  def main(self):
    while True:
      now = time.time()
      since = now - self.lastTime
      if since > self.configuration["rotation_delay"] or since < 0.0:
        self.display.modeUp()
        self.lastTime = now

def run():
  a = Chirimbolito()
