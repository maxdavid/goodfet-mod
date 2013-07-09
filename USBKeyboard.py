# USBKeyboard.py
#
# Contains class definitions to implement a USB keyboard.

from USB import *
from USBDevice import *
from USBConfiguration import *
from USBInterface import *
from USBEndpoint import *

class USBKeyboardInterface(USBInterface):
    name = "USB keyboard interface"

    hid_descriptor = b'\x09\x21\x10\x01\x00\x01\x22\x2b\x00'
    report_descriptor = b'\x05\x01\x09\x06\xA1\x01\x05\x07\x19\xE0\x29\xE7\x15\x00\x25\x01\x75\x01\x95\x08\x81\x02\x95\x01\x75\x08\x81\x01\x19\x00\x29\x65\x15\x00\x25\x65\x75\x08\x95\x01\x81\x00\xC0'

    def __init__(self, verbose=3):
        descriptors = { 
                USB.desc_type_hid    : self.hid_descriptor,
                USB.desc_type_report : self.report_descriptor
        }

        endpoint = USBEndpoint(
                3,          # endpoint number
                USBEndpoint.direction_in,
                USBEndpoint.transfer_type_interrupt,
                USBEndpoint.sync_type_none,
                USBEndpoint.usage_type_data,
                16384,      # max packet size
                10,         # polling interval, see USB 2.0 spec Table 9-13
                self.handle_buffer_available    # handler function
        )

        # TODO: un-hardcode string index (last arg before "verbose")
        USBInterface.__init__(
                self,
                0,          # interface number
                0,          # alternate setting
                3,          # interface class
                0,          # subclass
                0,          # protocol
                0,          # string index
                verbose,
                [ endpoint ],
                descriptors
        )

        empty_preamble = [ None ] * 10  #FIXME Why is this here? seems to work fine without it
        input_str = "vim wat.sh\ri#!/bin/bash\u000Decho hello\u001BZZchmod +x ./wat.sh\u000D./wat.sh\u000D"
        text = []
        for char in input_str:
            text.append(char)
            text.append(None)

        self.keys = [ self.ascii_to_hid(x) for x in empty_preamble + text ]

    def ascii_to_hid(self, input_str=None):
        """ASCII to HID character

        Convert an ASCII character to an HID keypress.
            Specifically, takes the first character of an input string to a tuple of 
            (modifier, keycode) that represents a keypress to be passed to the target. 
            No arguments returns a (0x00, 0), representing a <KEY UP>
        """

        if input_str is None:
            return (0x00, 0)

        self.keymap = {
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
            '\n': (0x28, 0), # can also be '\r'
            '': (0x29, 0), # \u001B
            '': (0x2a, 0), # \u007F
            '\t': (0x2b, 0),
            ' ' : (0x2c, 0),
            '-' : (0x2d, 0),
            '=' : (0x2e, 0),
            '[' : (0x2f, 0),
            ']' : (0x30, 0),
            '\\': (0x31, 0),
            ''  : (0x32, 0), #FIXME should be an ellipses
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
            '\u000D': (0x10, 1), # can be written as '\r' or '\n'
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
            ''  : (0x32, 2), #FIXME should be an ellipses
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
        return self.keymap[input_str[0]]

    def handle_buffer_available(self):
        if not self.keys:
            return

        keycode = self.keys.pop(0) # Grab a tuple of form (key, mod)
        self.type_letter(keycode[0], keycode[1])

    def type_letter(self, letter, modifier=0):
        data = bytes([ modifier, 0, letter ])

        if self.verbose > 2:
          print(self.name, 'sending keypress 0x{:02}, mod {}'.format(int(letter), modifier))

        self.configuration.device.maxusb_app.send_on_endpoint(3, data)


class USBKeyboardDevice(USBDevice):
    name = "USB keyboard device"

    def __init__(self, maxusb_app, verbose=0):
        config = USBConfiguration(
                1,                                          # index
                "Emulated Keyboard",    # string desc
                [ USBKeyboardInterface() ]                  # interfaces
        )

        USBDevice.__init__(
                self,
                maxusb_app,
                0,                      # device class
                0,                      # device subclass
                0,                      # protocol release number
                64,                     # max packet size for endpoint 0
                0x610b,                 # vendor id
                0x4653,                 # product id
                0x3412,                 # device revision
                "Maxim",                # manufacturer string
                "MAX3420E Enum Code",   # product string
                "S/N3420E",             # serial number string
                [ config ],
                verbose=verbose
        )

