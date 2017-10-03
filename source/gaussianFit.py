#!/usr/bin/env python3
import glob
import spinmob as s
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
#import sys
import convertChannelToEnergy as conv

#Font size!
font = {'family' : 'normal',
        'size'   : 15}

matplotlib.rc('font', **font)

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
        
        Gaussianfitter = s.data.fitter('a*exp(-(x-x0)**2/w**2)+b', 'a=200, b=0, x0=3.5, w=0.1', ymin=4)
        d = s.data.load(path)
        d[0] = [conv.calibrate_channel(data) for data in range(len(d[0]))]
        d[0]=s.fun.coarsen_array(d[0], level=2, method='mean')
        d[1]=s.fun.coarsen_array(d[1], level=2, method='mean')
        Gaussianfitter.set_data(xdata=d[0], ydata=d[1], eydata=np.sqrt(d[1]))
        Gaussianfitter.set(xlabel="Energy [MeV]")
        Gaussianfitter.set(ylabel="Counts")
        print("Click the peak!")
        click_x, click_y = Gaussianfitter.ginput()[0]
        Gaussianfitter(a=click_y, x0=click_x, xmin=click_x-1, xmax=click_x+1, ymin=np.max(d[1])*0.15)
        Gaussianfitter.fit()
        try:
            results.append(Gaussianfitter.results[0][2])
            results.append(np.sqrt(Gaussianfitter.results[1][2][2]))
        except TypeError:
            print("This dataset has not been accounted for due to a NoneType error...")
            pass
        plt.savefig("../../../assets/{}.svg".format(path.split('.')[0]))
    
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
