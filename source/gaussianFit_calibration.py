#!/usr/bin/env python3
import glob
import spinmob as s
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

#Retreive the read/write paths for files
#Usually read is '../database/'
#default_path = '../database/foilThickness/*/'
#combine_results = True
print(sys.argv)
if len(sys.argv) == 1:
    file_path = input("Where to read the file?: ")
    file_path = glob.glob("{}".format(file_path))
    if input("Combine results together? [y/n]: ") =='y':
        combine_results = True
elif len(sys.argv) == 2:
    file_path = sys.argv[1:]
    if input("Combine results together? [y/n]: ") =='y':
        combine_results = True
elif len(sys.argv) == 3:
    file_path = sys.argv[1]
    if sys.argv[2] == 1:
        combine_results = True

#file_path = default_path
#file_path = glob.glob("{}".format(file_path))

# loop over the paths
for master_path in file_path:
    
    #Brings us to new path
    os.chdir(master_path)
    paths = glob.glob("*.txt")
    
    results = []
    
    for path in paths:
        
        print("Converting " + path + " ...")
        
        Gaussianfitter = s.data.fitter('a*exp(-(x-x0)**2/w**2)+b', 'a=1, b=0, x0=1000, w=25', ymin=4)
        d = s.data.load(path)
        d[0]=s.fun.coarsen_array(d[0], level=2, method='mean')
        d[1]=s.fun.coarsen_array(d[1], level=2, method='mean')
        Gaussianfitter.set_data(xdata=d[0], ydata=d[1], eydata=np.sqrt(d[1]))
        print("CLICK THE PEAK!!")
        click_x, click_y = Gaussianfitter.ginput()[0]
        Gaussianfitter(a=click_y, x0=click_x, xmin=click_x-200, xmax=click_x+200, ymin=np.max(d[1])*0.15)
        Gaussianfitter.fit()
        print(Gaussianfitter.reduced_chi_squareds)
        Gaussianfitter.ginput()
    #    fitVolts = np.int(path.split('.')[0].split('_')[2][:-1])
    #    plt.savefit("wrongFit.png")
        results.append(np.array([Gaussianfitter.results[0][2], np.sqrt(Gaussianfitter.results[1][2][2])]))#, fitVolts]))
        # get the new path
        
    if combine_results == True:
        means = results[:][0]
        stds = results[:][1]
    #    results = np.zeroes(2)
    #    for i in range(len(means)):
        combined_means = np.mean(means)
        combined_stds = np.hypot(stds)
        #Writes over results
        results = np.array([combined_means, combined_stds])
            
    s = path.split('.')
#    s[-1] = 'txt'
#    s='.'.join(s)
    #Saves to new path
    np.save(('%s' %(s)), results, force_overwrite=True)
    os.remove("%s" %path)
    #sys("mkdir ../calibrationResults")
    
    #np.save("americium_alone", results)
    #np.save("../calibrationResults/americiumAlone", results)