
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
As such the intended audience will be application developers interested in controlling CCDs using ARC controllers.

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
   Note: We will need to revisit the 'RCC' command since it did not work as expected in initial testing.

2. Binning
   - Set rectangular binning up to 4x4.
     Note: We can already do rectangular binning up to 4 columns x arbitrary rows.
   - Report binning status
   
3. Amplifiers
   - Set amplifier
   - Report amplifier status
   
4. Subframes
   - Set 1 or more subframes
   - Report subframe status
   
5. Exposure Time
   - Set exposure time
   - Report exposure time
   
6. Camera Shutter
   - Control camera shutter
   - Report shutter status (Is shutter opened or closed? Is there hardware feedback to know this for sure?)
	
```diff  
+     Ted: No there isn’t.  It’s even worse; different shutter controllers use different
+     logic levels for open and closed states.
   
+     We need to be able to specify whether a given image is an object frame with light on it, a dark frame
+     with such-and-such exposure time, or a bias frame with the smallest possible exposure time and no light.
+     At this level we the idea of a flat frame doesn’t make sense – it is just a normal frame where the shutter
+     opens and you expose to light.  The fact that it’s a flat is a detail that needs to be dealt with at a
+     higher software level.
  
-     Dyer: I think the camera shutter is controlled by the DSP code when a SEX command is sent so we may not have
-     to have a requirement for this.  But, talk to Ted about it. Can we do independent shutter control?

-     Len: Also, how to prevent shutter from opening in the case of biases?

+     Ted: This is done by setting the SHUT bit in the STATUS word in the DSP code.  I bet this is
+     done with RDMEM/WRMEM commands at the application level prior to issuing the SEX command.  Is this in pcicamtest?

-     Len: Also, note there are OSH, CSH (found in the table
-     in the appendix) command for open/close shutter. It is probably a command independent of the 'SEX' command.
-     We have not been able to try this since we have not had a working shutter hooked up.

+     Ted: You’re both right, there are separate open and close shutter commands and SEX operates the
+     shutter automatically too.  

+     Specify data acquisition mode.  Support single frames, basic occultation, and strip scanning.  There will be
+     sub-requirements to define the exposure time or interval for basic occultation (per frame) and strip scans (per row)
+     and the number of frames or rows in these time-resolved readout modes.  Strip scanning is useful sometimes for
+     engineering purposes and basic occultation is essential for the GWAVES guiders.  Referring to the appendix the
+     command for setting the mode and its parameters is SIP.
```

7. Exposures
   - Take image data
   - Report exposure progress. 
   - Report readout progress.

```diff
-    Dyer: Ted said something, sometime, when we were working with the ARC57 camera that checking readout progress
-    could be problematic.  I forget what the problem was.

-    Len: I wonder if this point was confused with something
-    else since I was able to wait for the last pixel during readout. Grabbing the exposure progress should be
-    a simple matter of dividing the total number of pixels by 100, or something like that, to provide a readout
-    progress as a %. But do we really want to do this at the ArcLib level because of the potential system resource
-    overhead it will involve? I believe LOUI currently does a best guess at exposure progress and that guess is
-    close enough. I know the old LOIS used to provide readout progress based on the total number of pixels. Maybe
-    the end of each row was searched for during readout?

+    Ted:  I don’t know how LOIS did the progress report but it doesn’t take much in the way of system
+    resources and I don’t remember it being problematic.  I’m sure we can come up with a reasonable approach for
+    this.  For now, just leave it as item c) in your requirements list.
```

8. Provide accurate exposure start times.  (Len: Exposure start times based on shutter voltage change?)

```diff
+  Ted: I don’t see how to do this.  If we REALLY care about exact times we should hardware trigger, but I think we
+  can do a lot better without going to that extreme.
```

9. Image buffering
   - Store raw image data in a memory buffer to be made available to the software layer above ArcCam.
   - Report status of image buffer during readout.
   
```diff
+    Ted: I think we need to explicitly include a section on engineering functions.  Referring to the
+    table in the appendix, these would be SMX, RDM, WRM, and SYN (the synthetic image deal I mentioned in my
+    email of 8/10/18.  Direct access to RDM and WRM is important for debugging but they are also needed for
+    certain functions that will show up in the requirements (e.g. setting the necessary flag to get a bias or
+    dark frame).

+    I think we’re going to need explicit control of clearing the CCD prior to the exposure in order to have
+    accurate exposure start times without hardware triggering.  (See CLR in the table in the appendix.)  Right
+    now SEX includes a CCD clear before opening the shutter.  I think there is nanny code in LOIS that causes
+    additional delay that impacts the start times in the LMI headers.
```

### Future Enhancements

1. Abort an exposure in progress 
   - Straight forward abort
   - Pause / Resume abort
   - Abort and save

```diff
-    Dyer: We need to understand this better than we do now and that requires sitting down with Ted to talk about it.

-    Len: We should look at someone's code where this is working. Perhaps the C++ code from the ASU group? Or
-    maybe using 'Owl'? First see if it works in either of those.

+    Ted: I need to understand all the facets of this.  Many things need to be aborted and configurations
+    restored to make this work correctly.
```

2. Coadd - For use with infrared instruments

```diff
-  Dyer: The Coadd possibilities will also have to have parameters set, for example, how many images can we coadd
-  without causing problems with the size of the values stored in memory?  Can the values be saved with more
-  bytes per pixel to handle large coadd numbers?

+  Ted: There are different ways to deal with this too.  The complicated but fast (maybe) way to do it is to
+  co-add in the PCI card.  The easier but slower (maybe) way is to co-add in the computer after reading out
+  the images.  The really easy way is to take lots of images and co-add them during the data analysis phase.
```

3. Fowler Sampling – For use with infrared instruments

```diff
+  Ted: Doing this in PCI card memory or computer memory are both approaches to consider.
```

























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


