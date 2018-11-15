
## ArcLib Software Requirements Specification


### Introduction

#### Purpose   
ArcLib will present an Application Programming Interface (API) to allow parent applications to operate
Astronomical Research Cameras, Inc (ARC) camera controllers.

#### Product Scope
This document will describe the key requirements necessary to operate an ARC controller and will also offer
suggested capabilities that have not previously been implemented. A table of low level Digital Signal
Processor (DSP) commands will be included in the appendix to be used as a guideline for command requirements.

#### Intended Audience  
ArcLib will be used by system applications, in particular the Lowell Observatory Camera Utility System (LOCUS).
As such, the intended audience will be application developers interested in controlling CCDs using ARC controllers.

#### History  
The desire to have a very narrowly focused set of tools for this purpose is born out of the experience with the
current software implementation for commanding the ARC controllers, LOIS, which has grown to become much
more than a simple command interface for these controllers.  The purpose of ArcLib is to perform no other
tasks aside from commanding the controllers.

#### References  
[The Astronomical Research Cameras Website](http://www.astro-cam.com/index.php)

### Requirements 

ArcLib must be able to perform the following tasks:

1. Upload DSP files to the controller.  These consist of:
   - DSP for the timing board
   - DSP for the utility board
   - DSP for the PCI board

   ArcLib will report controller state during each of the above 3 steps.  
```diff 
+	Note: We will need to revisit the 'RCC' command since it did not work as expected in initial testing.
-	This might be related to modifications we made in the HIPO DSP.
```
2. Binning
   - Set rectangular binning up to 4x4.  Binning cannot be done with IR arrays.
   - Report binning status
   
3. Amplifiers
   - Set amplifier (e.g. left amplifier, left and right amplifier, top and bottom amplifier, etc.)
   - Report amplifier status
   
4. Subframes
   - Select either full frame readout or 1 to 4 subframes subject to these restrictions:
     - subframes cannot overlap in the row direction 
     - subframes are supported only for single amplifier readouts
   - Report subframe status
   
5. Exposure Time
   - Set exposure time with millisecond resolution.  Minimum is 1 ms.
   - Report exposure time
   
6. Camera Shutter
   - Control camera shutter automatically when taking data
   - Control camera shutter with independent open and close commands
   - Report shutter status (Is shutter opened or closed?)
   - Define whether the shutter should stay closed for an exposure (e.g. bias or dark).

7. Exposure mode
   - Define what mode will be used for the exposure.  
   - Single Frames are supported for all detector types
     - For IR arrays support CDS images and also both reset and post-integration read images.
   - Strip scanning is supported for all CCD types
   - Basic Occultation is supported only for frame transfer CCDs.
   - For time-resolved data provide a way to define the number of integrations and integration time.

8. Exposures
   - Take image data
   - Report exposure progress. 
   - Report readout progress.

9. Provide accurate exposure start times.

```diff
+  We can either flush before sending the SEX command or account for the time needed for the flush.
+  This can be done already with the CLR command.  If we do this the flush should be removed from the SEX commands.
+  Much of the problem with LMI is nanny code that we should manage carefully in LOCUS.
```

10. Image buffering
   - Store raw image data in a memory buffer to be made available to the software layer above ArcCam.
   - Report status of image buffer during readout.
   
11. Resets for infrared instruments
   - Global reset: Reset the entire array at once.  Only available with some arrays.
   - Pixel reset:  Reset pixel-at-a-time.

### Engineering Functions

1. Select clocks to direct to the two analog multiplexers on the clock driver board.

2. Support the synthetic image command, if present in the DSP code.

3. Support the low-level read and write memory commands directly.

### Future Enhancements

1. Abort an exposure in progress 
   - Support aborting only during integration, not during readout
     - Depend on error checking at the application level to prevent crazy readout sizes
   - Abort exposure, read out, and save data
   - Abort exposure, skip readout, and don't save data.

2. Change the exposure time on the fly (i.e. update exposure time during exposure)
   - If exposure time requested is less than exposure already made, abort, read out, and save data.

3. Pause an exposure and then resume it

```diff
+    Discuss with Tom.  Pause/resume is fraught.  What about multiple pause/resumes?  What airmass goes
+    in the header?  What's the exposure start time?  Won't abort-and-save together with a subsequent 
+    exposure accomplish the same thing?
```

4. Fowler Sampling – For use with infrared instruments.  (NDR = non-destructive read)
   - Basic operation is to reset/NDR, integrate, NDR, ..., integrate, NDR, idle (continuous reset)
   - Define the number of samples to make up the ramp
   - Define the interval between samples
   - Massaging of the Fowler sampled images occurs at the level above ArcLib

```diff
+  Ted: Doing this in the computer shouldn't involve any compromise since the array read rate is
+  slower than the fiber data transfer rate and the computer is fast.  The problem of what to do
+  with the Fowler samples is deferred to a different requirements document.
+  This solution presupposes that we aren't working longer than K band.
```

Appendix
```diff
+    Ted: The NIHTS command table is shorter than this one.  It includes:
+    SBV, SMX, RCC, DON, PON, POF, SET, SEX, and AEX, as well as the last set at COM_TBL.
+    In addition it has RET (Read_exposure_time), SNR (set_num_reads), and SBN (set_bias_number)
+    I don't think the NIHTS LOIS uses any of these three.  IR detectors don't have shutters and
+    can't be binned so commands related to them are meaningless.  NIHTS also doesn't support
+    subframes so all of the functions related to them are missing.
+    The LMI and DeVeny tables are basically the same as this table.
```

```	DC	'IDL',IDL  		; Put CCD in IDLE mode    
	DC	'STP',STP  		; Exit IDLE mode
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


