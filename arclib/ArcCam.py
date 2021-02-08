# -*- coding: utf-8 -*-
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
#  Created on 8 Feb 2021
#
#  @author: dlytle, rhamilton

from .SimpleOps import SimpleOps
from .SystemOps import SystemOps
from .Utilities import Utilities

import xml.etree.ElementTree as ET


class ArcCam(object):
    '''
    Root of ArcCam Library, includes complex operations.
    This object is used to communicate with an Leach/ARC camera
    controller.
    '''
    camera_file_descriptor = 0
    file_descriptor_open = False
    memory_map_open = False
    camera_exposure_time = 0

    def __init__(self, name, parent, device, config_file):
        '''
        Constructor
        '''
        self.device = device
        self.config_file = config_file
        self.parent = parent
        self.name = name
        self.file_descriptor_open = False
        self.printname = "'" + name + "'"
        message = ("'" + name + "' " + "created with parameters " +
                   str(device) + " and " + str(config_file))

        self.writeToConsole(message, "normal")

        self.simple = SimpleOps(self, device)
        self.system = SystemOps(self, device)
        self.utilities = Utilities(self, device)

        self.memorymap = None

        self.config_tree = ET.parse(self.config_file)
        root = self.config_tree.getroot()    # "camera-configuration"

    def __str__(self):
        return 'ArcCam: %s' % (self.name)

    def writeToConsole(self, message, messageType):
        if (self.parent is not None):
            self.parent.utilities.writeToConsole(message, messageType)
        else:
            print(message)

    def setup(self):
        self.system.camera_open()

    def close(self):
        self.system.camera_close()

    def load_timing_dsp(self, dsp_file):
        # Read through the timing DSP binhex file line by line until we find
        # the _END. When we find a data block, send to processDSPData
        # for ingest.
        fp = open(dsp_file)
        line = fp.readline()
        while line != '':
            if ("_END" in line):
                break
            if("_DATA" in line):
                items = line.split()  # The _DATA line contains memory type and
                #                       starting address for this data block.
                line = self.processDSPData(fp, items[1], items[2])
            line = fp.readline()

    def processDSPData(self, fp, memType, memAddress):
        x = 0
        # Convert start address to int.
        addr = int(memAddress, base=16)

        # Keep track of where we are in file.
        last_pos = fp.tell()
        line = fp.readline()
        while line != '':
            if ("_" in line):
                # if we find "_" back up one line and return
                fp.seek(last_pos)
                return()
            else:
                # Otherwise, split line up by spaces
                items = line.split()
                for item in items:
                    # Calculate the address to use
                    haddr = eval(hex(addr + x))
                    # Convert the data to int.
                    iitem = int(item, base=16)
                    # Actually write to memory (memwrt)
                    self.simple.write_memory(2, memType, haddr, iitem)

                    x += 1
            # Keep track of where we are in file and read next line
            last_pos = fp.tell()
            line = fp.readline()

    def status(self):
        rsp = self.simple.status()
        return(rsp)
