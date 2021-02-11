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

# NOTE: This file actually contains the memory locations and contants
#   that are used here; this is more of a skeleton in case we go back and
#   can support ARC Gen II stuff and there are differences.
import ARCGenIII as G3


class DSPCmd(object):
    # Just make it required to set each param ahead of time
    def __init__(self, goodname, prefix, nargs,
                 cmdtype=None, cmdloc=None, board=0, retval=None):
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
ARCCmds = dict()

ARCCmds["stop_idle"] = DSPCmd('stop_idle', 'simple', 0,
                              cmdtype=G3.ASTROPCI_COMMAND,
                              cmdloc=G3.STP,
                              board=2, retval="DON")

ARCCmds["start_idle"] = DSPCmd('start_idle', 'simple', 0,
                               cmdtype=G3.ASTROPCI_COMMAND,
                               cmdloc=G3.IDL,
                               board=2, retval="DON")

ARCCmds["power_on"] = DSPCmd('power_on', 'simple', 0,
                             cmdtype=G3.ASTROPCI_COMMAND,
                             cmdloc=G3.PON,
                             board=2, retval="DON")

ARCCmds["power_off"] = DSPCmd('power_off', 'simple', 0,
                              cmdtype=G3.ASTROPCI_COMMAND,
                              cmdloc=G3.POF,
                              board=2, retval="DON")

ARCCmds["read_memory"] = DSPCmd('read_memory', 'simple', 1,
                                cmdtype=G3.ASTROPCI_COMMAND,
                                cmdloc=G3.RDM,
                                board=0, retval="UNDEFINED")

ARCCmds["write_memory"] = DSPCmd('write_memory', 'simple', 2,
                                 cmdtype=G3.ASTROPCI_COMMAND,
                                 cmdloc=G3.WRM,
                                 board=0, retval="UNDEFINED")

ARCCmds["set_amplifier"] = DSPCmd('set_amplifier', 'simple', 1,
                                  cmdtype=G3.ASTROPCI_COMMAND,
                                  cmdloc=G3.SOS,
                                  board=2, retval="DON")

ARCCmds["set_row_col"] = DSPCmd('set_row_col', 'simple', 2,
                                cmdtype=G3.ASTROPCI_COMMAND,
                                cmdloc=G3.SRC,
                                board=2, retval="DON")

ARCCmds["set_subframe_size"] = DSPCmd('set_subframe_size',
                                      'simple', 3,
                                      cmdtype=G3.ASTROPCI_COMMAND,
                                      cmdloc=G3.SSS,
                                      board=2, retval="DON")

ARCCmds["set_subframe_position"] = DSPCmd('set_subframe_position',
                                          'simple', 2,
                                          cmdtype=G3.ASTROPCI_COMMAND,
                                          cmdloc=G3.SSP,
                                          board=2, retval="DON")

ARCCmds["set_image_parameters"] = DSPCmd('set_image_parameters',
                                         'simple', 4,
                                         cmdtype=G3.ASTROPCI_COMMAND,
                                         cmdloc=G3.SIP,
                                         board=2, retval="DON")

ARCCmds["set_exposure_time"] = DSPCmd('set_exposure_time',
                                      'simple', 1,
                                      cmdtype=G3.ASTROPCI_COMMAND,
                                      cmdloc=G3.SET,
                                      board=2, retval="DON")

ARCCmds["start_exposure"] = DSPCmd('start_exposure',
                                   'simple', 0,
                                   cmdtype=G3.ASTROPCI_COMMAND,
                                   cmdloc=G3.SEX,
                                   board=2, retval="DON")

ARCCmds["clear_subframe"] = DSPCmd('clear_subframe',
                                   'simple', 0,
                                   cmdtype=G3.ASTROPCI_COMMAND,
                                   cmdloc=G3.CSB,
                                   board=2, retval="DON")

ARCCmds["camera_open"] = DSPCmd('camera_open', 'system', 0)
ARCCmds["camera_close"] = DSPCmd('camera_close', 'system', 0)
ARCCmds["set_memory_map"] = DSPCmd('set_memory_map', 'system', 1)
ARCCmds["initialize"] = DSPCmd('initialize', 'system', 0)
ARCCmds["load_timing_dsp"] = DSPCmd('load_timing_dsp', 'none', 1)
ARCCmds["get_timing_status"] = DSPCmd('get_timing_status', 'none', 0)
ARCCmds["sleep"] = DSPCmd('sleep', 'system', 1)
ARCCmds["return_image"] = DSPCmd('return_image', 'utilities', 3)
