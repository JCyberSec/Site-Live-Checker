#!/usr/bin/env python
# # -*- coding: utf-8 -*-
# __author__ = "Jake Sloane"
# __copyright__ = "Copyright 2018, CGI ATI"
# __credits__ = ["Jake Sloane"]
# __license__ = "GPL"
# __version__ = "0.3.1"


#Check if xdotool is installed
#  [+] command -v xdotool
# If no data is returned:
#  [+] sudo apt install xdotool

import urllib2
import sys
import os
import subprocess
from time import gmtime, strftime
# Make the output look beautiful
class bcolors: 
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    OKBLUE = '\033[94m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
# Assign the input file to a var
listObj = sys.argv[1]
# Used to check atleast one site is live at the end
change = 0
# initialise previous time var
preTime = 0001
with open(listObj, 'r') as f:
    for line in f:
        i = line.strip('\n')
        check = i[:4] # Checks to see if the domain is appended with http/https or not
        if check != 'http':
            i = "http://" + i
        timeNow = int(strftime("%H%M"))
        try: # Print the time stamp
            if (timeNow - preTime) >= 1: # Do roughly one a minuet  
                print (bcolors.OKBLUE + " [-]   " + strftime("%d/%b/%y %X", gmtime()) + bcolors.ENDC)
                preTime = timeNow
        except:
            pass     
        try: # Try to connect to the site
            response = urllib2.urlopen(i)
            code = response.getcode()
            webpage = urllib2.urlopen(i).read()
            title = str(webpage).split('<title>')[1].split('</title>')[0]
            print (bcolors.OKGREEN + "  [+]    " + str(code) + " - " + str(title) + " - " + i + bcolors.ENDC)
            subprocess.check_output(["xdg-open " + i], shell=True) # Open the site
            subprocess.check_output(["xdotool key alt+Tab"], shell=True) # Show the terminal
            change = 1 # Update change as site is live so need to run at end
        except urllib2.HTTPError: # Always have HTTP above URL or it will always catch
            print (bcolors.FAIL + " [+]    Failed to connect to " + i + bcolors.ENDC)
        except urllib2.URLError:
            print (bcolors.FAIL + " [+]    Failed to connect to " + i + bcolors.ENDC)
        except IndexError: # This is a indexing bug with the title tag
            print (bcolors.WARNING + "  [+]    IndexError on " + i + bcolors.ENDC)
            subprocess.check_output(["xdg-open " + i], shell=True)
            subprocess.check_output(["xdotool key alt+Tab"], shell=True)
            change = 1 # Update change as site is live so need to run at end
if change == 1: # Open the web browser at the end
    subprocess.check_output(["xdotool key alt+Tab"], shell=True)