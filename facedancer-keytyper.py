#!/usr/bin/env python3

"""Facedancer Keyboard Input

Pass a string on the command line to have it typed on the target computer.
"""
import sys

from serial import Serial, PARITY_NONE

from Facedancer import *
from MAXUSBApp import *
from USBKeyboard import *

def main():
  sp = Serial("/dev/ttyUSB0", 115200, parity=PARITY_NONE, timeout=2)
  fd = Facedancer(sp, verbose=1)
  u = MAXUSBApp(fd, verbose=1)

  d = USBKeyboardDevice(u, verbose=4)

  d.connect()

  try:
    d.run()
  # SIGINT raises KeyboardInterrupt
  except KeyboardInterrupt:
    d.disconnect()

def ascii_to_hid(inputstr):
  keymaps = []
  keymaps.append( # Keymap for no modkeys [0]
    {
      'a' : 0x04,
      'b' : 0x05,
      'c' : 0x06,
      'd' : 0x07,
      'e' : 0x08,
      'f' : 0x09,
      'g' : 0x0a,
      'h' : 0x0b,
      'i' : 0x0c,
      'j' : 0x0d,
      'k' : 0x0e,
      'l' : 0x0f,
      'm' : 0x10,
      'n' : 0x11,
      'o' : 0x12,
      'p' : 0x13,
      'q' : 0x14,
      'r' : 0x15,
      's' : 0x16,
      't' : 0x17,
      'u' : 0x18,
      'v' : 0x19,
      'w' : 0x1a,
      'x' : 0x1b,
      'y' : 0x1c,
      'z' : 0x1d,
      '1' : 0x1e,
      '2' : 0x1f,
      '3' : 0x20,
      '4' : 0x21,
      '5' : 0x22,
      '6' : 0x23,
      '7' : 0x24,
      '8' : 0x25,
      '9' : 0x26,
      '0' : 0x27,
      '\n': 0x28,
      '^[': 0x29,
      '^?': 0x2a,
      '\t': 0x2b,
      ' ' : 0x2c,
      '-' : 0x2d,
      '=' : 0x2e,
      '[' : 0x2f,
      ']' : 0x30,
      '\\': 0x31,
      'zq': 0x32, #FIXME should be an ellipses
      ';' : 0x33,
      '\'': 0x34,
      '`' : 0x35,
      ',' : 0x36,
      '.' : 0x37,
      '/' : 0x38
    })
  keymaps.append( # With LeftCtrl depressed
    {})
  keymaps.append( # With LeftShift depressed
    {
      'A' : 0x04,
      'B' : 0x05,
      'C' : 0x06,
      'D' : 0x07,
      'E' : 0x08,
      'F' : 0x09,
      'G' : 0x0a,
      'H' : 0x0b,
      'I' : 0x0c,
      'J' : 0x0d,
      'K' : 0x0e,
      'L' : 0x0f,
      'M' : 0x10,
      'N' : 0x11,
      'O' : 0x12,
      'P' : 0x13,
      'Q' : 0x14,
      'R' : 0x15,
      'S' : 0x16,
      'T' : 0x17,
      'U' : 0x18,
      'V' : 0x19,
      'W' : 0x1a,
      'X' : 0x1b,
      'Y' : 0x1c,
      'Z' : 0x1d,
      '!' : 0x1e,
      '@' : 0x1f,
      '#' : 0x20,
      '$' : 0x21,
      '%' : 0x22,
      '^' : 0x23,
      '&' : 0x24,
      '*' : 0x25,
      '(' : 0x26,
      ')' : 0x27,
      ' ' : 0x28,
      ' ' : 0x29,
      ' ' : 0x2a,
      ' ' : 0x2b,
      ' ' : 0x2c,
      '_' : 0x2d,
      '+' : 0x2e,
      '{' : 0x2f,
      '}' : 0x30,
      '|' : 0x31,
      'zq': 0x32, #FIXME should be an ellipses
      ':' : 0x33,
      '"' : 0x34,
      '~' : 0x35,
      '<' : 0x36,
      '>' : 0x37,
      '?' : 0x38
    })
  keymaps.append( # LeftCtrl & LeftShift
    {})
  keymaps.append( # LeftAlt
    {})


if __name__ == "__main__":
  main()
