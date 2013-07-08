# USBKeyboard.py
#
# Contains class definitions to implement a USB keyboard.

from USB import *
from USBDevice import *
from USBConfiguration import *
from USBInterface import *
from USBEndpoint import *
import keyboard_util

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

        empty_preamble = [ None ] * 10
        input_str = "vim wat.sh\ri#!/bin/bash\u000Decho hello\u001BZZchmod +x ./wat.sh\u000D./wat.sh\u000D"
        text = []
        for char in input_str:
          text.append(char)
          text.append(None)

        self.keys = [ keyboard_util.ascii_to_hid(x) for x in empty_preamble + text ]

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

