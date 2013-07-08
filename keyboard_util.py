#!/usr/bin/env python3

"""Facedancer Keyboard Input Utils"""

def ascii_to_hid(input_str=None):
  """ASCII to HID character

  Convert an ASCII character to an HID keypress.
    Specifically, takes the first character of an input string to a tuple of 
    (modifier, keycode) that represents a keypress to be passed to the target. 
    By default returns a (0, 0x00), which represents a <KEY UP>

  input_str -- a string, ideally of length 1, to be converted (default None)
  """
  if input_str is None:
    return (0x00, 0)

  keymap = {
      'a' : (0x04, 0), # Keypresses with no modifier (mod = 0)
      'b' : (0x05, 0),
      'c' : (0x06, 0),
      'd' : (0x07, 0),
      'e' : (0x08, 0),
      'f' : (0x09, 0),
      'g' : (0x0a, 0),
      'h' : (0x0b, 0),
      'i' : (0x0c, 0),
      'j' : (0x0d, 0),
      'k' : (0x0e, 0),
      'l' : (0x0f, 0),
      'm' : (0x10, 0),
      'n' : (0x11, 0),
      'o' : (0x12, 0),
      'p' : (0x13, 0),
      'q' : (0x14, 0),
      'r' : (0x15, 0),
      's' : (0x16, 0),
      't' : (0x17, 0),
      'u' : (0x18, 0),
      'v' : (0x19, 0),
      'w' : (0x1a, 0),
      'x' : (0x1b, 0),
      'y' : (0x1c, 0),
      'z' : (0x1d, 0),
      '1' : (0x1e, 0),
      '2' : (0x1f, 0),
      '3' : (0x20, 0),
      '4' : (0x21, 0),
      '5' : (0x22, 0),
      '6' : (0x23, 0),
      '7' : (0x24, 0),
      '8' : (0x25, 0),
      '9' : (0x26, 0),
      '0' : (0x27, 0),
      '\n': (0x28, 0),
      '^[': (0x29, 0),
      '^?': (0x2a, 0),
      '\t': (0x2b, 0),
      ' ' : (0x2c, 0),
      '-' : (0x2d, 0),
      '=' : (0x2e, 0),
      '[' : (0x2f, 0),
      ']' : (0x30, 0),
      '\\': (0x31, 0),
      'zq': (0x32, 0), #FIXME should be an ellipses
      ';' : (0x33, 0),
      '\'': (0x34, 0),
      '`' : (0x35, 0),
      ',' : (0x36, 0),
      '.' : (0x37, 0),
      '/' : (0x38, 0),
      '': (0x04, 1), # Keypresses with LeftCtrl (mod = 1)
      '': (0x05, 1),
      '': (0x06, 1),
      '': (0x07, 1),
      '': (0x08, 1),
      '': (0x09, 1),
      '': (0x0a, 1),
      '': (0x0b, 1),
      ' ' : (0x0c, 1),
      ' ' : (0x0d, 1),
      '': (0x0e, 1),
      '': (0x0f, 1),
      ' ' : (0x10, 1),
      '': (0x11, 1),
      '': (0x12, 1),
      '': (0x13, 1),
      '': (0x14, 1),
      '': (0x15, 1),
      '': (0x16, 1),
      '': (0x17, 1),
      '': (0x18, 1),
      '': (0x19, 1),
      '': (0x1a, 1),
      '': (0x1b, 1),
      '': (0x1c, 1),
      '': (0x1d, 1),
      'A' : (0x04, 2), # Keypresses with LeftShift (mod = 2)
      'B' : (0x05, 2),
      'C' : (0x06, 2),
      'D' : (0x07, 2),
      'E' : (0x08, 2),
      'F' : (0x09, 2),
      'G' : (0x0a, 2),
      'H' : (0x0b, 2),
      'I' : (0x0c, 2),
      'J' : (0x0d, 2),
      'K' : (0x0e, 2),
      'L' : (0x0f, 2),
      'M' : (0x10, 2),
      'N' : (0x11, 2),
      'O' : (0x12, 2),
      'P' : (0x13, 2),
      'Q' : (0x14, 2),
      'R' : (0x15, 2),
      'S' : (0x16, 2),
      'T' : (0x17, 2),
      'U' : (0x18, 2),
      'V' : (0x19, 2),
      'W' : (0x1a, 2),
      'X' : (0x1b, 2),
      'Y' : (0x1c, 2),
      'Z' : (0x1d, 2),
      '!' : (0x1e, 2),
      '@' : (0x1f, 2),
      '#' : (0x20, 2),
      '$' : (0x21, 2),
      '%' : (0x22, 2),
      '^' : (0x23, 2),
      '&' : (0x24, 2),
      '*' : (0x25, 2),
      '(' : (0x26, 2),
      ')' : (0x29, 2),
      ' ' : (0x28, 2),
      ' ' : (0x29, 2),
      ' ' : (0x2a, 2),
      ' ' : (0x2b, 2),
      ' ' : (0x2c, 2),
      '_' : (0x2d, 2),
      '+' : (0x2e, 2),
      '{' : (0x2f, 2),
      '}' : (0x30, 2),
      '|' : (0x31, 2),
      'zq': (0x32, 2), #FIXME should be an ellipses
      ':' : (0x33, 2),
      '"' : (0x34, 2),
      '~' : (0x35, 2),
      '<' : (0x36, 2),
      '>' : (0x37, 2),
      '?' : (0x38, 2)
      # Keypresses with LeftCtrl + LeftShift (mod = 3)
      # Keypresses with LeftAlt (mod = 4)
  }

  # Return the HID code for the first character in the input string
  return keymap(input_str[0])

def string_to_hid_list(input_str):
  """String to HID list

  Convert a string to a list of tuples representing an HID keypress.
    Each tuple contains a key in the form of (modifier, keycode) that will 
    represent a keypress to the target.
  """
  hid_list = []
  for character in input_str:
    hid_list.append(ascii_to_hid(character))

  # hid_list now contains the string in a form of HID tuples, (mod, key)
  return hid_list

