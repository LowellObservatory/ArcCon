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
from binascii import unhexlify

import numpy as np
from PIL import Image


# NOTE: A lot of these are a bit silly in Python, because they're just
#   literal translations of each other in a lot of cases.  But it makes
#   things more readable and some aren't, so I'm defining them still.

# Generic States
UNDEFINED = -1
ERROR = -1
NO_ERROR = 0

# PCI Vector Commands
READ_PCI_IMAGE_ADDR = 0x8075
PCI_PC_RESET = 0x8077
BOOT_EEPROM = 0x807B
READ_HEADER = 0x81
TIM_RESET = 0x87
WRITE_NUM_IMAGE_BYTES = 0x8F
INITIALIZE_IMAGE_ADDRESS = 0x91
WRITE_COMMAND = 0xB1

# Readout modes
__L = 0x005F5F4C
__R = 0x005F5F52
_LR = 0x005F4C52
ALL = 0x00414C4C

# Gain and speed constants
ONE = 1
TWO = 2
FIVE = 5
TEN = 10
SLOW = 0
FAST = 1

# Readout modes
SPLIT_PARALLEL = 1
SPLIT_SERIAL = 2
QUAD_CCD = 3
QUAD_IR = 4

# Define shutter positions
_OPEN_SHUTTER_SBIT_ = (1 << 11)
_CLOSE_SHUTTER_SBIT_ = ~(1 << 11)

# Replies
TOUT = 0x544F5554
ROUT = 0x524F5554
DON = 0x00444F4E
ARC_ERR = 0x00455252
ARC_SYR = 0x00535952
RST = 0x00525354

# Readout Constants
READOUT = 5
READ_TIMEOUT = 200

# Board Ids
PCI_ID = 1
TIM_ID = 2
UTIL_ID = 3

# Memory Location Id Constants
#	R	(Bit 23)  ROM
#	P	(Bit 20)  DSP program memory space
#	X	(Bit 21)  DSP X memory space
#	Y	(Bit 22)  DSP Y memory space
P = 0x100000
X = 0x200000
Y = 0x400000
R = 0x800000

# Masks to set the Host Control Register HCTR.
#
#       Only three bits of this register are used. Two are control bits to set
#  the mode of the PCI board (bits 8 and 9)  and  the  other (bit 3) is a flag
#  indicating the progress of image data transfer to the user's application.
#
#       Bit 3   = 1     Image buffer busy transferring to user space.
#               = 0     Image buffer not  transferring to user space.
#
#       Bit 8= 0 & Bit 9= 1   PCI board set to slave mode for PCI file download
#       Bit 8= 0 & Bit 9= 0   PCI board set to normal processing.
#
#       Note that the HTF_MASK, sets the HTF bits 8 and 9 to transfer mode.
#
HTF_MASK = 0x200
HTF_CLEAR_MASK = 0xFFFFFCFF
BIT3_CLEAR_MASK = 0xFFFFFFF7
BIT3_SET_MASK = 0x00000008
HTF_BITS = 0x00000038

# Macros for fill and wrap counter in continuous mode. The operand is the
#   32 bit output of the ASTROPCI_GET_PROGRESS ioctl.
#   which is partitioned thus:  wrap D31-26, FILL D25-0
PCIDSP_WRAP_BITS = 6
PCIDSP_WRAPCNT = 64
"""
pcidsp_fill( progress_pixels)   ( (progress_pixels) & \
                                        (( 1 << (32 - PCIDSP_WRAP_BITS)) -1))
pcidsp_wrap( progress_pixels)   (\
       ((progress_pixels) >> (32 - PCIDSP_WRAP_BITS)) &\
       (( 1 << PCIDSP_WRAP_BITS) - 1))
"""


"""
/**
*****************************************************************************
*	Check the reply returned from the PCI DSP against the specified
*	expected reply value.
*
*	reply		Actual reply from PCI.
*	expected_reply	The value of the expected reply.
*****************************************************************************
*/
int check_expected_reply(int reply, int expected_reply)
{
        char reply_str[20], expreply_str[20], cmd_str[20];

        strncpy( reply_str, dsp_interp(reply), sizeof(reply_str)-1);
        reply_str[ sizeof(reply_str) - 1] = '\0';
        strncpy( expreply_str, dsp_interp(expected_reply),
                 sizeof(expreply_str)-1);
        expreply_str[ sizeof(expreply_str) - 1] = '\0';
        strncpy( cmd_str, dsp_interp(((unsigned int)cmd_data[1])),
                 sizeof(cmd_str)-1);
        cmd_str[ sizeof(cmd_str) - 1] = '\0';

	if (reply != expected_reply) {
	  lois_log1("Error: Expected Reply:%s Actual Reply:%s Command(%s)",
		    expreply_str, reply_str, cmd_str);
		error = reply;
		return ERROR;
	}
	else
		return NO_ERROR;
}
"""


def dsp_interp(dspword):
    try:
        interp = unhexlify(dspword)
    except Exception as err:
        # TODO: Catch the right exception here
        print(str(err))
        # give up and just return the hex
        interp = dspword
        print("0x%x" % interp)

    return interp


def check_standard_reply(reply):
    """
    Check the reply returned from the PCI DSP against the standard set
    of replies: ERR, SYR, RST, TOUT. If the reply does not match one of
    the standard ones, the reply is just returned.

    reply		Actual reply from PCI.
    """
    if reply in [ARC_ERR, ARC_SYR, RST]:
        return reply
    elif reply == TOUT:
        error = reply
        print("Error: Standard Reply %s", dsp_interp(reply))
        return ERROR
    else:
        return reply


def hcvr(file_descriptor, command, data, reply):
    """
    Send a command to the PCI DSP via the vector register. The reply
    returned from the PCI DSP is checked against the specified expected
    reply value.

    board_id	The board to receive the command.
                Can be one of: PCI_ID, TIM_ID, or UTIL_ID.
    command		The vector command to be sent to the PCI DSP.
    data		The data associated with the vector command.
    expected_reply	The value of the expected reply.
    """
    reply = NO_ERROR, retval

    # If there's data, send it
    if (data != UNDEFINED):
        retval = ioctl(file_descriptor, ASTROPCI_HCVR_DATA, data)
        if (retval != 0):
            return retval

    # Send the command
    retval = ASTROPCI_SET_HCVR
    retval = ioctl(file_descriptor, ASTROPCI_SET_HCVR, command)

    if (retval != 0):
        print("HCVR IOCTL call return errno=%d\n", errno)
        return retval

    reply = command

    # If a reply is expected, check it
    if (expected_reply != UNDEFINED):
        return (check_expected_reply(reply, expected_reply))
    else:
        return (check_standard_reply(reply))



def ioctlCommand(file_descriptor, board_num, command, command_type, *args):
    num_args = len(args)

    # Combine everything so it can be passed.  Should make this faster
    #   (but less readable) and just keep this as a comment/reminder
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


def responseDecode(rsp, fmt='txt'):
    if fmt.lower() == 'txt:':
        cmd_sent = rsp[4:7].decode("utf-8")
        cmd_response = rsp[0:3].decode("utf-8")
    elif fmt.lower() == 'hex':
        cmd_sent = rsp[4:7]
        cmd_response = rsp[0:3]

    cmd_sent = cmd_sent[::-1]
    cmd_response = cmd_response[::-1]

    return "cmd: " + str(cmd_sent) + " reply: " + str(cmd_response), "arccam"


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
