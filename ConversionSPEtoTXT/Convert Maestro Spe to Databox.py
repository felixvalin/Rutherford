import glob
import spinmob
import sys 
from os import system as terminal


if len(sys.argv) == 0:
    default_path = "../DataConverted/"
else:
    default_path = sys.argv[1]

paths = glob.glob("*.Spe")

# loop over the paths
for path in paths:
    
    print("Converting " + path + " ...")
    
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
    d.save_file(path=('%s%s' %(default_path,s)), force_overwrite=True)
    terminal("rm %s" %path)
#raw_input('<enter>')
