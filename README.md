# Toolbox v3.09
The third generation of the Toolbox.

Please notice! v3.06 is not backward-compatible with previous versions due to code structure changes. 

To get a detailed documentation of this software, please open the software and go to Menubar->Module->Document.

FTIR fitting tool v3 and FTIR Commander are included to serve as demo. 

System requirement:

Mac OS/ Windows / Linux (Not tested)

python 3.4 +

The following packages need to be installed before running the program:

matplotlib, numpy, PyQt5 and mysqlclient. Install using pip is recommended.

Now dark theme is available. Pip install qdarkstyle in order to use it. 

How to run it:

Download the whole package to local, and then run "Toolbox_v3.py".

For any questions, please contact pman3@uic.edu.

Update log:

v. 3.0: Initial version number. Qt(PyQt5) is used to design the UI. 

v. 3.01: Bug fixes; Added splash screen.  

v. 3.02: Fixed an issue where the tabs in MDI area won't close properly. 

v. 3.03: Added "Quit" and other window adjustment function to menu bar; 

Added Dark theme. pip install qdarkstyle module is required to use dark theme. 

v. 3.04: Statusbar coorperates better with changing modules using tabs; 

Now the size of log frame is adjustable. It can either hide or adjust to a certain height within very good amount of range.

v. 3.05: While we are waiting for Ryan's update, here are the small changes: 

The color of Matplolib area has changed to match the dark theme. The main reason for that is the black background would hide some lines. 

Added an icon in the system tray.  Right now it only has "Exit" function. 

Added Edit menu,  but no function is created. 

Slight change made to the module menu. 
             
v. 3.06: Ryan's update is here. Create a new module is easy than ever. The structure of Toolbox_v3.py has changed to be more flexible. 

Several new tools are added. Now all tools are stored inside individual folders instead of the main folder. 

The configuration.ini file now belongs to each module. Toolbox itself has a separate configuration.ini file. ﻿

Documentation is updated to include the documents from all tools.

v. 3.07: 

A few changes to optimize the file path handling. Now the program is ready to be packaged into an executable app using pyinstaller (tested on Mac OS and Windows 7);

Fixed bugs where some n/k csv file has invlid characters; 

Fixed bugs where some csv readers do not work as exprected; 

Improved error messages when import failed. 

Added different icon format for Mac Os/Windows.

v. 3.08: 

Added addlog() and addlog_with_button() into the main toolbox.py file as standard functions.
 
See example in the document file. 

v. 3.09: 

Some minor improvements. 

Fixed an issue where arrow keys cannot be used to navigate the documents. 

Now one can quit fullscreen mode with Esc key. 

Added three new modules: MBE Assistant, Microscope Assistant and ImageM. Now modules other than FTIR fitting tool is moved to github submudules. 

Added pure dark theme. It can be activated by setting colortheme parameter to 2. It may cause some visual problems in modules with Matplotlib build-in toolbar.
             
