# Bitcoin Node Tools
Alpha Version

This repository's purpose is to store a few useful tools for users running
Bitcoin Nodes.

For now, there is only one application, LogReader, but the goal is to gradually create a few modules that make it easier to run and monitor a full bitcoin node. 

Please make sure to pip install the packages at requirements.txt.

LogReader - remote monitoring of debug.log file
--------------------------------------------------
Log Reader monitors the debug.log file and generates a webpage like the one below: 

![title](https://image.ibb.co/i9Jj4U/Screen_Shot_2018_10_07_at_4_30_55_PM.png)

Make sure to review config.ini file to setup the debug.log file location and
other settings.

If you want to make the log public (so you can access from anywhere),
see this link:
https://stackoverflow.com/questions/37661843/how-can-one-configure-flask-to-be-accessible-via-public-ip-interface

Feel free to update, modify and submit suggestions.
All code in this repository is open for copying
and modifying without limitations as long as you credit this
original repository. 
