#!/usr/bin/env python3
import glob
import spinmob
import sys 
import os

#Retreive the read/write paths for files
#Usually read is '../database/'
if len(sys.argv) == 1:
    file_path = input("Where to read the file?: ")
elif len(sys.argv) == 2:
    file_path = sys.argv[1]

paths = glob.glob("{}*.Spe".format(file_path))

# loop over the paths
for path in paths:
    
    print("Converting " + path.split('/')[-1] + " ...")
    
    # read all the lines in the file
    lines = spinmob.fun.read_lines(path)
    
    # make a databox for saving
    d = spinmob.data.databox()    
    d['Channel'] = []
    d['Counts']  = []    
    
    # search for the data
    n = 0
    i = 0
    for i in range(len(lines)):
        
        # data starts with a space
        if lines[i][0] == ' ': 
            d.append_data_point([n, int(lines[i].strip())])
            n += 1
    
        # get info
        elif lines[i][0]=='$':

            # get the hkey and value
            hkey = lines[i][1:].strip()
            value= lines[i+1].strip()
            d.insert_header(hkey, value)
    
    # get the new path
    s = path.split('.')
    s[-1] = 'txt'
    s='.'.join(s)
    #Saves to new path
    d.save_file(path=('%s' %(s)), force_overwrite=True)
    os.remove("%s" %path)
#raw_input('<enter>')
