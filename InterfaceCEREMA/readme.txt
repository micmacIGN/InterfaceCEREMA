The CEREMA interface provides a user-friendly graphical user interface for 
MICMAC, the IGN's free photogrammetry tool.

The CEREMA interface provides a user-friendly graphical user interface to 
MICMAC, the IGN's free photogrammetry tool.

Version V 5.55 of 24 November 2020
- Addition of the MicMac Schnaps module
- Display of homologous points
- Help for entering GPS points 

Version V 5.54 of 21 August 2020
- correction of translations: the word "mistresses" is sometimes misinterpreted!
- Fraser' becomes the default option for Tapas

Version V 5.53 of 14 August 2020
- Removal of 'white stripes' in 3D clouds of GPS coordinates on construction sites  
- multiple detail improvements, see version history

Version V 5.52 of 8 July 2020
- Massively multilingual version: French, English, German, Italian, Spanish, Chinese, Arabic
- Adding the file size in the menu "open job site".

Contained version V 5.512 of 25 June 2020 :
- Addition of a Business Tools Menu : to compare 2 point clouds
- various improvements and corrections: see the history and the script
- the msi installer for Windows is too big for GitHub, ask for it at interface-micmac@cerema.fr.

Contained version V 5.50 of May 4, 2020 :
- Writing plys in MNT IGN and GRASS format
- Choice of an EPSG repository for UAV GPS data
- Choice between mesh and cloud for densified ply from Malt
- the non dense cloud becomes optional
- various improvements and corrections: see the history and the script

version V 5.49 15 January 2020 :
- GPS data from the UAV's onboard cameras are used to define the point cloud referential.
  4 new items in the expert menu to manage these GPS data.
- if a batch of photos defines several scenes: proposal to process the most numerous ones
- copying of homologous points from one job site to another
- various improvements: see history and source

version V 5.48 25 May 2019 :
- recovery of the calibration of the devices from another site.
- the sites proposed to copy the GCP points and the calibration are filtered.
- correction of a regression of V 5.47 (Tarama bug)

version V 5.47 21 May 2019 :
- various improvements of the programme s aromatics, see source.

version V 5.46 20 May 2019 :
- Addition of the item Tools/GCP points quality
- Added item Expert/Customise MicMac optional parameters

version V 5.45 13 May 2019 :
- Securing the import of a building site from a directory") + "\n "+\
- Securing the import of GCP points (Ground Control Point=GPS) from a building site or a file") + "\n "+\
- Add function 'rename a job site' (function deleted in V5.41)") + "\n "+\
- Securing the calibration of the devices by Tapas (ForCalib option) for sites with a lot of photos

version V 5.44 9 May 2019 :

 - addition of the "search" function in the texts displayed by text201 (trace, help); Ctrl F then F3
 - the cleaning in a building site no longer removes the possible building sites present underneath it
 - displays the result of system commands in a text window (menu expert/system command)
 - after a failure in Tapas the choice "option" proposes to keep the homologous points (= item 'throw micmac')
See complete list in the script
 
version V 5.44 :
	Possibility to launch several instances of the interface under windows
	Help 'some tips' divided into 3 items
	Some bug fixes and minor modifications: see the script
	
version 5.42 04 April 2019 :
	Correction of a regression this version 5.41 concerning the trace
	
version 5.41 04 April 2019 :
	Ergonomic improvement of the File/Household function and correction of a bug
	The menu item "File/Rename job" changes to "Save as..." with the corresponding error message.

version 5.40 01 April 2019 :
	modification ergonomics input of GPC points, next/previous picture in input window
	bug corrections
	added draping for c3dc's quickmac micmac and BigMac options
	modification of c3dc's default option: BigMac
	
version 5.34 following the advice of Xavier Rolland (26/03/19)
- global replacement of GPS by GCP = Ground Control Point
- When you return from entering GCP points: photo list window
- the display of the coordinates of the entered points becomes optional
- the zoom limit in the point input window is increased

March 25, 2019: addition of a tutorial to get to grips with MicMac through the CEREMA interface.

March 25th 2019 version: 5.33
- Possibility of restarting an unfinished building site while keeping the homologous points.
- Addition of an item to the expert menu: change the length of the prefix used to define several devices. 
- removal for old versions of 32-bit windows and linux installers.
  These installers (msi 32 bit for version 5.0; deb and rpm for version 3.14) remain available in the Github history. 

Version of 12 March 2019: 5.32
- the search for a new version on the web proposes the visualization of the file "readme.txt" (Tools/check presence...)
- under windows : warning if the length of a command line exceeds 8191 characters, risk of crashing 
- correction bug when defining several cameras, improvement of the processing speed 

March 8, 2019 version: 5.31
- Tapioca's default scales are calculated according to the photos: 60% of the maximum dimension of the photos
- Deleting the tool menu items\line photo quality and ALL photo quality,
  maintains the quality of the photos on the last treatment
- Addition of a stage uniqueness control after the first, fast passage of Tapioca MultiScale :
  avoids the need for an in-depth search for homologous points if failure is expected.
- Add 1 item to the tools menu: remove photos from the worksite
- optimisation of the "Expert/multiple devices" function
- the msi installer for Windows installs a start menu item, a desktop shortcut, and
  adds the installation directory to the path

Several new features in version 5.30 February 2019:
- in the 'Tools/Photo Quality' items, added 'isolated' photos, in disjunction of all the others.
  These photos make the orientation search 'crash'.
- Following the search for homologous points, verification of the uniqueness of the photographed scene.
  Several scenes with no common homologous points cause the search for orientation to fail.
  This function is added to the 'Tools/Photo quality' item.
- When the MAXLINELENGTH message is issued by Tapioca, it is displayed and explained in the synthetic trace.
- The error concerning the filedialog function in Mac-Os is taken into account when searching for programmes (exiftool...).
- Addition of an item in parameter setting : search for a new GitHub version.

in versions 5.2 :
- automatic launch of campari after GCP_bascul (menu MicMac/options/gps points)
- addition of mm3d log consultation (expert menu)
- update of dicocamera.xml for "all" cameras in the dataset (tools menu)
- adding a job site from a directory (file menu)
- addition of an item in the expert menu: opening of a console to launch "python" commands

Several new features in version 5.11 : 

- MicMac menu/options: the "calibration" tab is renamed: "scaling".
- MicMac/option/Tapas menu: the photos to calibrate the camera are, or not, independent of the photos used to build the cloud
- tools/camera name menu: display of photo dimensions and camera serial number (if present in the exif)
- Expert menu, new items :
  - entry of GPS points from a text file (space separator: name, x,y,z, dx,dy,dz)
  - possibility to divide the photos into several cameras 
  - list of the different cameras present in the batch of photos
  
For more details see the menu item "Help/History" or the source code.
First webcast: 23 November 2015.


An msi installer facilitates the installation under 64-bit Windows.
Under linux and mac/os: see the documentation
 
The IGN MicMac application must be installed :
https://micmac.ensg.eu/index.php/Install
See also :
https://github.com/micmacIGN or http://logiciels.ign.fr/?Micmac )

Translated with www.DeepL.com/Translator (free version)

