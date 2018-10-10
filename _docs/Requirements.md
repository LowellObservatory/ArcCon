
## ArcCon Library Software Requirements Specification


### Introduction

#### Description   
The ArcCon library will make it possible to operate an ARC (Astronomical Research Camera, Inc) camera
controller of which many are in use at Lowell Observatory.  The desire to have a very narrowly focused
set of tools for the purpose of controlling ARC camera controllers is born out of the experience with the
current software implementation for commanding the ARC controllers, LOIS, which has grown to become much
more than a simple command interface for these controllers.  The purpose of ArcCam is to perform no other
tasks aside from commanding the controllers.

Scope
This document will describe the key requirements necessary to operate an ARC controller and will also offer
suggested capabilities that have not previously been implemented. We will not discuss implementation details
such as the language used for this new library. A table of low level “DSP” commands will be included in the
appendix to be used as a guideline of command requirements. 


Requirements 

The ArcCam library must be able to perform the following tasks:

I.	a) Load timing DSP
b) Load utility DSP
c) Load PCI DSP
      b) Report controller state during each of the above 3 steps. (Need to revisit the 'RCC' command
      since it did not work as expected when I tried using it.)

II.	a) Set binning up to 4x4. For binning values greater than 4x4 in addition to rectangular binning see
       the “Future  Enhancements” section below.
      b) Report binning status
III.	a) Set amplifier
      b) Report amplifier status
IV.	a) Set 1 or more subframes
      b) Report subframe status
V.	a) Set exposure time
      b) Report exposure time
VI.	a) Control camera shutter
      b) Report shutter status (Is shutter opened or closed? Is there hardware feedback to know this for sure?)

I think the camera shutter is controlled by the DSP code when a SEX command is sent so we may not have
to have a requirement for this.  But, talk to Ted about it.  Can we do independent shutter control? Also,
how to prevent shutter from opening in the case of biases? Also, note there are OSH, CSH (found in the table
in the appendix) command for open/close shutter. It is probably a command independent of the 'SEX' command.
We have not been able to try this since we have not had a working shutter hooked up.


VII.	a) Take image data
      b) Report exposure progress. 
      c) Report readout progress.

Ted said something, sometime, when we were working with the ARC57 camera that checking readout progress
could be problematic.  I forget what the problem was. I wonder if this point was confused with something
else since I was able to wait for the last pixel during readout. Grabbing the exposure progress should be
a simple matter of dividing the total number of pixels by 100, or something like that, to provide a readout
progress as a %. But do
we really want to do this at the ArcCam level because of the potential system resource overhead it will involve?
I believe LOUI currently does a best guess at exposure progress and that guess is close enough. I know the old LOIS
used to provide readout progress based on the total number of pixels. Maybe the end of each row was searched for
during readout?

VIII. a) Provide accurate exposure start times.
           (Exposure start times based on shutter voltage change?)


VIV. a) Store raw image data in a memory buffer to be made available to the software layer above ArcCam.
      b) Report status of image buffer during readout.


Future Enhancements

I.	Abort an exposure in progress 
      a) Straight forward abort
      b) Pause / Resume abort
      c) Abort and save

We need to understand this better than we do now and that requires sitting down with Ted to talk about it.
We should look at someone's code where this is working. Perhaps the C++ code from the ASU group? Or maybe
using 'Owl'? First see if it works in either of those.

II.	Coadd - For use with infrared instruments
The Coadd possibilities will also have to have parameters set, for example, how many images can we coadd
without causing problems with the size of the values stored in memory?  Can the values be saved with more
bytes per pixel to handle large coadd numbers?

III.	Fowler Sampling – For use with infrared instruments

IV. Rectangular binning 
























Appendix

```	DC	'IDL',IDL  		; Put CCD in IDLE mode    
; Remove for gen-iii since it is in timboot as per June 30 #9                      ??? Question for Ted
;	DC	'STP',STP  		; Exit IDLE mode
	DC	'SVR',SETVRDS		; set VRD2,3
	DC	'SBV',SETBIAS 		; Set DC bias supply voltages  
	DC	'RDC',RDCCD 		; Begin CCD readout    
	DC	'CLR',CLEAR  		; Fast clear the CCD   
	DC	'SGN',ST_GAIN  		; Set video processor gain     
	DC  'SMX',SET_MUX       ; Set clock driver MUX output           Is MUX broken?

	DC	'ABR',ABR_RDC		; Abort readout
	DC	'CRD',CONT_RD		; Continue reading out
	DC	'CSW',CLR_SWS		; Clear analog switches to lower power
	DC	'SOS',SEL_OS		; Select output source
	DC	'RCC',READ_CONTROLLER_CONFIGURATION 
	DC	'SSS',SET_SUBARRAY_SIZES
	DC	'SSP',SET_SUBARRAY_POSITIONS
	DC	'DON',START		; Nothing special
	DC	'OSH',OPEN_SHUTTER
	DC	'CSH',CLOSE_SHUTTER
	DC	'PON',PWR_ON		; Turn on all camera biases and clocks
	DC	'POF',PWR_OFF		; Turn +/- 15V power supplies off
	DC	'SET',SET_EXP_TIME 	; Set exposure time
	DC	'SEX',START_FT_EXPOSURE	; Goes to mode-dependent jump table
	DC	'AEX',ABORT_EXPOSURE
	DC	'STG',SET_TRIGGER	;  Set Trigger Mode on or off
	DC	'SIP',SET_IMAGE_PARAM
	DC	'SRC',SET_ROWS_COLUMNS ; Set NSR, NPR, and binning
	DC	'INF',GET_INFO		; info command for versioning and more


COM_TBL	DC      'TDL',TDL		; Test Data Link
	DC      'RDM',RDMEM		; Read from DSP or EEPROM memory
	DC      'WRM',WRMEM		; Write to DSP memory        
	DC	'LDA',LDAPPL		; Load application from EEPROM to DSP
	DC	'STP',STOP_IDLE_CLOCKING
	DC	'DON',START		; Nothing special
	DC      'ERR',START		; Nothing special```


