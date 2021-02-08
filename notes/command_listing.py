# Device Driver Commands
ASTROPCI_GET_HCTR = 0x1
ASTROPCI_GET_PROGRESS = 0x41524302
ASTROPCI_GET_DMA_ADDR = 0x3
ASTROPCI_GET_HSTR = 0x4
ASTROPCI_HCVR_DATA = 0x10
ASTROPCI_SET_HCTR = 0x11
ASTROPCI_SET_HCVR = 0x12
ASTROPCI_PCI_DOWNLOAD = 0x13
ASTROPCI_PCI_DOWNLOAD_WAIT = 0x14
ASTROPCI_COMMAND = 0x15

# Define Commands
TDL = 0x0054444C  # Test Data Link
TRM = 0x0054524D  # Test DRAM
RDM = 0x0052444D  # Read Memory
WRM = 0x0057524D  # Write Memory
WSI = 0x00575349  # Write Synthetic Image
SEX = 0x00534558  # Start Exposure
SET = 0x00534554  # Set Exposure Time
PEX = 0x00504558  # Pause Exposure
REX = 0x00524558  # Resume Exposure
RET = 0x00524554  # Read Elapsed Time
AEX = 0x00414558  # Abort Exposure
PON = 0x00504F4E  # Power On
POF = 0x00504F46  # Power Off
RDI = 0x00524449  # Read Image
SOS = 0x00534F53  # Select Output Source
MPP = 0x004D5050  # Multi-Pinned Phase Mode
DCA = 0x00444341  # Download Coadder
SNC = 0x00534E43  # Set Number of Coadds
VID = 0x00564944  # mnemonic that means video board
SBN = 0x0053424E  # Set Bias Number
SBV = 0x00534256  # Set Bias Voltage
SGN = 0x0053474E  # Set Gain
RST = 0x00525354  # Reset
SMX = 0x00534D58  # Select Multiplexer
CLK = 0x00434C4B  # mnemonic means clock driver board
SSS = 0x00535353  # Set Subarray Sizes
SSP = 0x00535350  # Set Subarray Positions
LGN = 0x004C474E  # Set Low Gain
HGN = 0x0048474E  # Set High Gain
SRM = 0x0053524D  # Set Readout Mode - CDS or single
CDS = 0x00434453  # Correlated Double Sampling
SFS = 0x00534653  # Send Fowlefr Sample
SPT = 0x00535054  # Set Pass Through Mode
LDA = 0x004C4441  # Load Application
RCC = 0x00524343  # Read Controller Configuration
CLR = 0x00434C52  # Clear Array
IDL = 0x0049444C  # Idle
STP = 0x00535450  # Stop Idle
CSH = 0x00435348  # Close Shutter
OSH = 0x004F5348  # Open Shutter
SUR = 0x00535552  # Set Up The Ramp Mode
SSB = 0x00535342  # Set subframe mode for IR
CSB = 0x00435342  # Clear subframe mode
GTK = 0x0047544B  # Get (PCI) tick
INF = 0x00494E46  # Get info

TBS = 0x544253  # Test Byte Swap
SBS = 0x534253  # Set Byte Swap
SBC = 0x534243  # Set Bit Comp
WDC = 0x574443  # WDC
ICA = 0x494341  # Init CoAdd
DCB = 0x444342  # Dump Coadder Buffer
SSM = 0x53534D  # Send Trigger Command
STG = 0x535447  # Start Trigger Run
TEX = 0x544558  # Start Trigger Exposure
SSV = 0x535356  # Start Series Run
SFD = 0x534644  # Start some kind of Exposure
SIP = 0x534950  # Set Image Parameters
SRC = 0x535243  # fSet Image Dimensions

#       Memory Location Id Constants
#               R       (Bit 20)  ROM
#               P       (Bit 21)  DSP program memory space
#               X       (Bit 22)  DSP X memory space
#               Y       (Bit 23)  DSP Y memory space

P = 0x100000
X = 0x200000
Y = 0x400000
R = 0x800000
