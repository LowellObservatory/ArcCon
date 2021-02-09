# -*- coding: utf-8 -*-
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
#  Created on 8 Feb 2021
#
#  @author: dlytle, rhamilton

from __future__ import division, print_function, absolute_import

import fcntl
from PIL import Image
import numpy as np


def ioctlCommand(file_descriptor, board_num, command, command_type, *args):
    num_args = len(args)

    # Combine everything so it can be passed
    cmd_int = [0] * 6
    cmd_int[0] = ((board_num << 8) | num_args + 2)
    cmd_int[1] = command
    cmd_int[2] = 0 if num_args == 0 else args[0]
    cmd_int[3] = 0 if num_args <= 1 else args[1]
    cmd_int[4] = 0 if num_args <= 2 else args[2]
    cmd_int[5] = 0 if num_args <= 3 else args[3]

    cmd = cmd_int[0].to_bytes(4, byteorder='little') \
        + cmd_int[1].to_bytes(4, byteorder='little') \
        + cmd_int[2].to_bytes(4, byteorder='little') \
        + cmd_int[3].to_bytes(4, byteorder='little') \
        + cmd_int[4].to_bytes(4, byteorder='little') \
        + cmd_int[5].to_bytes(4, byteorder='little')

    response = fcntl.ioctl(file_descriptor, command_type, cmd)

    return(response)


def print_text_response(rsp):
    cmd_sent = rsp[4:7].decode("utf-8")
    cmd_response = rsp[0:3].decode("utf-8")
    cmd_sent = cmd_sent[::-1]
    cmd_response = cmd_response[::-1]

    self.parent.writeToConsole('cmd: ' + str(cmd_sent) +
                               ' reply: ' + str(cmd_response), "arccam")


def print_hex_response(rsp):
    cmd_sent = rsp[4:7].decode("utf-8")
    cmd_response = rsp[0:3]
    cmd_sent = cmd_sent[::-1]
    cmd_response = cmd_response[::-1]

    self.parent.writeToConsole('cmd: ' + str(cmd_sent) +
                               " response: " + str(cmd_response), "arccam")


def return_image(mymap, x, y, offset):
    # mymap = self.parent.memorymap

    w = x
    h = y
    woffset, hoffset = 0, 0
    initoffset = 2 + offset
    data = np.zeros((h, w-woffset), dtype=np.float)
    inc = initoffset + w*2*hoffset
    #img2 = Image.new('I', (h,w-woffset), color='black')
    #pixels = img2.load()
    for j in range(0, h):
        myarray = mymap[inc:inc+(w-1)*2]
        byteswapped = bytearray(len(myarray))
        byteswapped[0::2] = myarray[1::2]
        byteswapped[1::2] = myarray[0::2]

        for i in range(0, w-1):
            #data[h-j-1, i] =  byteswapped[i*2]*4 #+ byteswapped[i*2+1]
            data[h-j-1, i] = byteswapped[i*2]*256 + byteswapped[i*2+1]
            #pixels[h-j-1, i] =  byteswapped[i*2]*3

        inc = inc+w*2

    a1d = np.reshape(data, w*h)
    # self.parent.parent.brokertalk.returnImage(a1d, x, y)
    img = Image.fromarray(data)
    #img.show()

    return img
