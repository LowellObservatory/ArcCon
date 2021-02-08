
''' ArcCommandStructure.py '''

__author__ = "Dyer Lytle"
__version__ = "1.0"
__lastupdate__ = "March 14, 2018"

''' Various Constants and Commands used by ArcCam '''


ARC_command_list = dict()

ARC_command_list["stop_idle"] = {
    "command_type":0x15,         # ASTROPCI_COMMAND
    "command": 0x00535450,       # STP
    "board_num": 2,              # Timing Board
    "num_args":0,
    "call_prefix": "simple",
    "expected_return":"DON"}

ARC_command_list["start_idle"] = {
    "command_type":0x15,          # ASTROPCI_COMMAND
    "command": 0x0049444C,        # IDL
    "board_num": 2,               # Timing Board
    "num_args":0,
    "call_prefix": "simple",
    "expected_return":"DON"}

ARC_command_list["power_on"] = {
    "command_type":0x15,          # ASTROPCI_COMMAND
    "command": 0x00504F4E,        # PON
    "board_num": 2,               # Timing Boardds
    "num_args":0,
    "call_prefix": "simple",
    "expected_return":"DON"}

ARC_command_list["power_off"] = {
    "command_type":0x15,          # ASTROPCI_COMMAND
    "command": 0x00504F46,        # POF
    "board_num": 2,               # Timing Board
    "num_args":0,
    "call_prefix": "simple",
    "expected_return":"DON"}

ARC_command_list["read_memory"] = {
    "command_type":0x15,          # ASTROPCI_COMMAND
    "command": 0x0052444D,        # RDM
    "board_num": 0,               # Any Board, 1,2,3
    "num_args":1,
    "call_prefix": "simple",
    "expected_return":"UNDEFINED"}

ARC_command_list["write_memory"] = {
    "command_type":0x15,          # ASTROPCI_COMMAND
    "command": 0x0057524D,        # WRM
    "board_num": 0,               # Any Board, 1,2,3
    "num_args":2,
    "call_prefix": "simple",
    "expected_return":"UNDEFINED"}

ARC_command_list["set_amplifier"] = {
    "command_type":0x15,          # ASTROPCI_COMMAND
    "command": 0x00534F53,        # SOS
    "board_num": 2,               # Timing
    "num_args":1,
    "call_prefix": "simple",
    "expected_return":"DON"}

ARC_command_list["set_row_col"] = {
    "command_type":0x15,          # ASTROPCI_COMMAND
    "command": 0x535243,          # SRC
    "board_num": 2,               # Timing
    "num_args":2,
    "call_prefix": "simple",
    "expected_return":"DON"}

ARC_command_list["set_subframe_size"] = {
    "command_type":0x15,          # ASTROPCI_COMMAND
    "command": 0x00535353,        # SSS
    "board_num": 2,               # Timing
    "num_args":3,
    "call_prefix": "simple",
    "expected_return":"DON"}

ARC_command_list["set_subframe_position"] = {
    "command_type":0x15,          # ASTROPCI_COMMAND
    "command": 0x00535350,        # SSP
    "board_num": 2,               # Timing
    "num_args":2,
    "call_prefix": "simple",
    "expected_return":"DON"}

ARC_command_list["set_image_parameters"] = {
    "command_type":0x15,          # ASTROPCI_COMMAND
    "command": 0x534950,          # SIP
    "board_num": 2,               # Timing
    "num_args":4,
    "call_prefix": "simple",
    "expected_return":"DON"}

ARC_command_list["set_exposure_time"] = {
    "command_type":0x15,          # ASTROPCI_COMMAND
    "command": 0x00534554,        # SET
    "board_num": 2,               # Timing
    "num_args":1,
    "call_prefix": "simple",
    "expected_return":"DON"}

ARC_command_list["start_exposure"] = {
    "command_type":0x15,          # ASTROPCI_COMMAND
    "command": 0x00534558,        # SEX
    "board_num": 2,               # Timing
    "num_args":0,
    "call_prefix": "simple",
    "expected_return":"DON"}

ARC_command_list["clear_subframe"] = {
    "command_type":0x15,          # ASTROPCI_COMMAND
    "command": 0x00435342,        # CSB
    "board_num": 2,               # Timing
    "num_args":0,
    "call_prefix": "simple",
    "expected_return":"DON"}

ARC_command_list["camera_open"] = {
    "num_args": 0,
    "call_prefix": "system"}

ARC_command_list["camera_close"] = {
    "num_args": 0,
    "call_prefix": "system"}

ARC_command_list["set_memory_map"] = {
    "num_args": 1,
    "call_prefix": "system"}

ARC_command_list["initialize"] = {
    "num_args": 0,
    "call_prefix": "none"}

ARC_command_list["load_timing_dsp"] = {
    "num_args": 1,
    "call_prefix": "none"}

ARC_command_list["get_timing_status"] = {
    "num_args": 0,
    "call_prefix": "none"}

ARC_command_list["sleep"] = {
    "num_args": 1,
    "call_prefix": "system"}

ARC_command_list["return_image"] = {
    "num_args": 3,
    "call_prefix": "utilities"}



