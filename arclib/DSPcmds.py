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

import ARCGenIII as G3


class ARCDSPCmd(object):
    # Just make it required to set each param ahead of time
    def __init__(self, goodname, prefix, nargs,
                 cmdtype=None, cmdloc=None, board=None, retval=None):
        # These have to be specified for each command
        self.name = goodname
        self.call_prefix = prefix
        self.nargs = nargs

        # These are all optional
        self.cmdtype = cmdtype
        self.cmdloc = cmdloc
        self.board = board
        self.retval = retval


# Reminder: these are on the controller/instrument side!
#   board 0 means any board (1, 2, 3)
#   board 1 is the pci card
#   board 2 is the timing board
#   board 3 is utility board
ARC_command_list = dict()

ARC_command_list["stop_idle"] = ARCDSPCmd('stop_idle', 'simple', 0,
                                          cmdtype=G3.ASTROPCI_COMMAND,
                                          cmdloc=G3.STP,
                                          board=2, retval="DON")

ARC_command_list["start_idle"] = ARCDSPCmd('start_idle', 'simple', 0,
                                           cmdtype=G3.ASTROPCI_COMMAND,
                                           cmdloc=G3.IDL,
                                           board=2, retval="DON")

ARC_command_list["power_on"] = ARCDSPCmd('power_on', 'simple', 0,
                                         cmdtype=G3.ASTROPCI_COMMAND,
                                         cmdloc=G3.PON,
                                         board=2, retval="DON")

ARC_command_list["power_off"] = ARCDSPCmd('power_off', 'simple', 0,
                                          cmdtype=G3.ASTROPCI_COMMAND,
                                          cmdloc=G3.POF,
                                          board=2, retval="DON")

ARC_command_list["read_memory"] = ARCDSPCmd('read_memory', 'simple', 1,
                                            cmdtype=G3.ASTROPCI_COMMAND,
                                            cmdloc=G3.RDM,
                                            board=0, retval="UNDEFINED")

ARC_command_list["write_memory"] = ARCDSPCmd('write_memory', 'simple', 2,
                                             cmdtype=G3.ASTROPCI_COMMAND,
                                             cmdloc=G3.WRM,
                                             board=0, retval="UNDEFINED")

ARC_command_list["set_amplifier"] = ARCDSPCmd('set_amplifier', 'simple', 1,
                                              cmdtype=G3.ASTROPCI_COMMAND,
                                              cmdloc=G3.SOS,
                                              board=2, retval="DON")

ARC_command_list["set_row_col"] = ARCDSPCmd('set_row_col', 'simple', 2,
                                            cmdtype=G3.ASTROPCI_COMMAND,
                                            cmdloc=G3.SRC,
                                            board=2, retval="DON")

ARC_command_list["set_subframe_size"] = ARCDSPCmd('set_subframe_size',
                                                  'simple', 3,
                                                  cmdtype=G3.ASTROPCI_COMMAND,
                                                  cmdloc=G3.SSS,
                                                  board=2, retval="DON")

ARC_command_list["set_subframe_position"] = ARCDSPCmd('set_subframe_position',
                                                      'simple', 2,
                                                      cmdtype=G3.ASTROPCI_COMMAND,
                                                      cmdloc=G3.SSP,
                                                      board=2, retval="DON")

ARC_command_list["set_image_parameters"] = ARCDSPCmd('set_image_parameters',
                                                     'simple', 4,
                                                     cmdtype=G3.ASTROPCI_COMMAND,
                                                     cmdloc=G3.SIP,
                                                     board=2, retval="DON")

ARC_command_list["set_exposure_time"] = ARCDSPCmd('set_exposure_time',
                                                  'simple', 1,
                                                  cmdtype=G3.ASTROPCI_COMMAND,
                                                  cmdloc=G3.SET,
                                                  board=2, retval="DON")

ARC_command_list["start_exposure"] = ARCDSPCmd('start_exposure',
                                               'simple', 0,
                                               cmdtype=G3.ASTROPCI_COMMAND,
                                               cmdloc=G3.SEX,
                                               board=2, retval="DON")

ARC_command_list["clear_subframe"] = ARCDSPCmd('clear_subframe',
                                               'simple', 0,
                                               cmdtype=G3.ASTROPCI_COMMAND,
                                               cmdloc=G3.CSB,
                                               board=2, retval="DON")

ARC_command_list["camera_open"] = ARCDSPCmd('camera_open',
                                            'system', 0)

ARC_command_list["camera_close"] = ARCDSPCmd('camera_close',
                                             'system', 0)

ARC_command_list["set_memory_map"] = ARCDSPCmd('set_memory_map',
                                               'system', 1)

ARC_command_list["initialize"] = ARCDSPCmd('initialize',
                                           'system', 0)

ARC_command_list["load_timing_dsp"] = ARCDSPCmd('load_timing_dsp',
                                                'none', 1)

ARC_command_list["get_timing_status"] = ARCDSPCmd('get_timing_status',
                                                  'none', 0)

ARC_command_list["sleep"] = ARCDSPCmd('sleep', 'system', 1)

ARC_command_list["return_image"] = ARCDSPCmd('return_image', 'utilities', 3)
