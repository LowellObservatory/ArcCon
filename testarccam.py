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

from arclib.ARCInterface import ARCInterface
import time

device = "/dev/Arc64PCI0"
config_file = "config/CCD57.xml"

device = ARCInterface("CCD57", device, config_file)

device.setup()  # Open file descriptor

device.system.set_memory_map(1048576)  # Set up memory map on the fd

# device.loadTimingDSP("../misc/tim.lod.0x04_0x8C_20V_straight") # load tim dsp
#
# device.simple.set_amplifier("LEFT") # set amp
#
# time.sleep(1)  # sleep one second
#
# device.simple.read_memory(2, 'X', 0x000000) # check timing board status

device.simple.stop_idle()
time.sleep(1)
device.simple.start_idle()
time.sleep(1)

# device.simple.power_on() # power on
#
# time.sleep(1) # sleep one second

# Close file descriptor.
device.close()
