#!/usr/bin/env python3
import glob
import spinmob as s
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import convertChannelToEnergy as conv

#Retreive the read/write paths for files
#Usually read is '../database/'
#default_path = '../database/foilThickness/*/'
#combine_results = True
#print(sys.argv)
#if len(sys.argv) == 1:
#    file_path = input("Where to read the file?: ")
#    file_path = glob.glob("{}".format(file_path))
#    if input("Combine results together? [y/n]: ") =='y':
#        combine_results = True
#elif len(sys.argv) == 2:
#    file_path = sys.argv[1:]
#    if input("Combine results together? [y/n]: ") =='y':
#        combine_results = True
#elif len(sys.argv) == 3:
#    file_path = sys.argv[1]
#    if sys.argv[2] == 1:
#        combine_results = True

def hypot(values):
    sum = 0
    for x in values:
        sum += x**2
    return np.sqrt(sum)

original_dir = os.getcwd()

default_path = '../database/foilThickness/*/'
file_path = input("Relative path to database? (default is {}): ".format(default_path))
if file_path is '':
    file_path = default_path

combine_results = input("Combine results for each foils? (default is y) [y/n]: ")
if combine_results == 'y' or combine_results == '':
    combine_results = True
else:
    combine_results = False
    
file_path = glob.glob("{}".format(file_path))

# loop over the paths
for master_path in file_path:
    
    #Brings us to new path
    os.chdir(master_path)
    paths = glob.glob("*.txt")
    
    results = []
    
    for path in paths:
        
        print("\n----------------------------------------\n")
        
        print("Converting " + path + " ...")
        
        Gaussianfitter = s.data.fitter('a*exp(-(x-x0)**2/w**2)+b', 'a=1, b=0, x0=1000, w=25', ymin=4)
        d = s.data.load(path)
        d[0]=s.fun.coarsen_array(d[0], level=2, method='mean')
        d[1]=s.fun.coarsen_array(d[1], level=2, method='mean')
        Gaussianfitter.set_data(xdata=d[0], ydata=d[1], eydata=np.sqrt(d[1]))
        print("Click the peak!")
        click_x, click_y = Gaussianfitter.ginput()[0]
        Gaussianfitter(a=click_y, x0=click_x, xmin=click_x-200, xmax=click_x+200, ymin=np.max(d[1])*0.15)
        Gaussianfitter.fit()
        ###For testing purposes
#        Gaussianfitter.ginput()
    #    fitVolts = np.int(path.split('.')[0].split('_')[2][:-1])
    #    plt.savefit("wrongFit.png")
        results.append(Gaussianfitter.results[0][2])
        results.append(np.sqrt(Gaussianfitter.results[1][2][2]))#, fitVolts]))
        # get the new path
        #####For testing
#        break
        
    if combine_results == True:
        means = results[0::2]
        stds = results[1::2]
    #    results = np.zeroes(2)
    #    for i in range(len(means)):
        combined_means = np.mean(means)
        combined_stds = hypot(stds)
        #Writes over results
        results = np.array([combined_means, combined_stds])
        results = conv.calibrate(results[0], results[1])
            
    npy_file = path.split('.')[0][:-6]
#    s[-1] = 'txt'
#    s='.'.join(s)
    #Saves to new path
    np.save(('%s' %(npy_file)), results)
    print("\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
    print("Saved data (in [eV]) to: {}.npy".format(npy_file))
    print("\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
#    os.remove("%s" %path)
    os.chdir(original_dir)
    #sys("mkdir ../calibrationResults")
    
    #np.save("americium_alone", results)
#    np.save("../calibrationResults/americiumAlone", results)