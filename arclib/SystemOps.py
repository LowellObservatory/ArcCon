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

import os
import mmap
import sys
import time


class SystemOps(object):
    '''
    The routines in this file are part of ArcCamLib and are operating system
    commands as opposed to controller commands.
    '''

    def __init__(self, parent, params):
        '''
        Constructor
        '''
        self.parent = parent

    def camera_open(self):
        # Open the device, return a file descriptor.
        self.parent.writeToConsole(self.parent.name +
                                   " is doing a 'camera_open' command.",
                                   "arccam")
        try:
            self.parent.camera_file_descriptor = os.open(self.parent.device,
                                                         os.O_RDWR, 0)
        except OSError as e:
            if '[Error 16]' in str(e):
                self.parent.writeToConsole('Device already in use', "error")
            return(-1)
        except Exception as err:
            self.parent.writeToConsole("Unexpected Error: " +
                                       str(sys.exc_info()[0]), "error")
            return(-1)
        else:
            self.parent.file_descriptor_open = True
            self.parent.writeToConsole("open successful", "arccam")
            #self.parent.simple.reset_controller()
            return()

    def camera_close(self):
        # Close the device.
        self.parent.writeToConsole(self.parent.name +
                                   " is doing a 'camera_close' command.",
                                   "arccam")
        try:
            #self.parent.memorymap.close()
            os.close(self.parent.camera_file_descriptor)
            if (self.parent.memory_map_open):
                self.parent.memorymap.close()
                self.parent.memory_map_open = False
        except Exception as err:
            self.parent.writeToConsole("Unexpected Error: " +
                                       str(sys.exc_info()[0]), "error")
            return(-1)
        else:
            self.parent.file_descriptor_open = False
            self.parent.writeToConsole("close successful", "arccam")
            return(0)

    def set_memory_map(self, mmap_size):
        # Map memory to file descriptor, return map pointer.
        self.parent.writeToConsole(self.parent.name +
                                   " is doing a 'set_memory_map' command.",
                                   "arccam")
        if (self.parent.file_descriptor_open):
            try:
                mymap = mmap.mmap(self.parent.camera_file_descriptor,
                                  mmap_size, mmap.MAP_SHARED,
                                  mmap.PROT_READ | mmap.PROT_WRITE)
            except Exception as err:
                self.parent.writeToConsole("Unexpected Error: " +
                                           str(sys.exc_info()[0]), "error")
                return(-1)
            else:
                self.parent.writeToConsole("set_memory_map successful",
                                           "arccam")
                self.parent.memorymap = mymap
                self.parent.memory_map_open = True
                return(mymap)

        else:
            self.parent.writeToConsole(
                "Error in set_memory_map, file descriptor not open", "error")

    def sleep(self, sleeptime):
        time.sleep(sleeptime)
