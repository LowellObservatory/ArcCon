
from ArcCamLib.ArcCam import ArcCam
import time

device = "/dev/Arc64PCI0"
config_file = "/home/dlytle/git/ArcCam/src/config/CCD57.xml"

device = ArcCam("CCD57", None, device, config_file)

device.setup()  # Open file descriptor

device.system.set_memory_map(1048576)  # Set up memory map on the fd
# 
# device.loadTimingDSP("../misc/tim.lod.0x04_0x8C_20V_straight") # load tim dsp
# 
# device.simple.set_amplifier("LEFT") # set amp
# 
# time.sleep(1)  # sleep one second
# 
# device.simple.read_memory(2, 'X', 0x000000) # check timing board status

device.simple.stop_idle()
time.sleep(1)
device.simple.start_idle() # start idle
#time.sleep(1)



# device.simple.power_on() # power on
# 
# time.sleep(1) # sleep one second

device.close() # Close file descriptor.