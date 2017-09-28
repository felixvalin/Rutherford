import glob
import spinmob as s
import numpy as np
from os import system as sys
import os

os.cd("../database/")

paths = glob.glob("*.txt")

results = []

# loop over the paths
for path in paths:
    
    print("Converting " + path + " ...")
    
    Gaussianfitter = s.data.fitter('a*exp(-(x-x0)**2/w**2)+b', 'a=1, b=0, x0=1000, w=25')
    d = s.data.load(path)
    Gaussianfitter.set_data(xdata=d[0], ydata=d[1], eydata=np.sqrt(d[1]))
    print("CLICK THE PEAK!!")
    click_x, click_y = Gaussianfitter.ginput()[0]
    Gaussianfitter(a=click_y, x0=click_x, xmin=click_x-200, xmax=click_x+200, ymin=0.5)
    Gaussianfitter.fit()
    fitVolts = np.int(path.split('.')[0].split('_')[2][:-1])
    
    results.append(np.array([Gaussianfitter.results[0][2], Gaussianfitter.results[0][3], fitVolts]))

np.save("../../database/mean_std", results)
    #    # read all the lines in the file
#    lines = spinmob.fun.read_lines(path)
#    
#    # make a databox for saving
#    d = s.data.databox()    
#    d['Channel'] = []
#    d['Counts']  = []    
#
#    # search for the data
#    n = 0
#    i = 0
#    for i in range(len(lines)):
#        
#        # data starts with a space
#        if lines[i][0] == ' ': 
#            d.append_data_point([n, int(lines[i].strip())])
#            n += 1
#    
#        # get info
#        elif lines[i][0]=='$':
#
#            # get the hkey and value
#            hkey = lines[i][1:].strip()
#            value= lines[i+1].strip()
#            d.insert_header(hkey, value)
#    
#    # get the new path
#    s = path.split('.')
#    s[-1] = 'txt'
#    s='.'.join(s)
#    d.save_file(path=('../DataConverted/%s' %s), force_overwrite=True)
##raw_input('<enter>')
