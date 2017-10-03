#!/usr/bin/env python3
import glob
import spinmob as s
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
#import sys
import convertChannelToEnergy as conv

'''
What's left: put combined_results by default inside the for loop
Will make it easier and faster. Make sure all data sets are okay
and not too lossy... 

Will not work! maybe angle 15 not complete before doing the combination
'''
#For font size!
font = {'family' : 'normal',
        'size'   : 15}

matplotlib.rc('font', **font)

def hypot(values):
    sum = 0
    for x in values:
        sum += x**2
    return np.sqrt(sum)

original_dir = os.getcwd()

default_path = '../database/scattering/'
file_path = input("Relative path to database? (default is {}): ".format(default_path))
if file_path is '':
    file_path = default_path

#combine_results = input("Combine results for each angles? (default is y) [y/n]: ")
#if combine_results == 'y' or combine_results == '':
#    combine_results = True
#else:
#    combine_results = False
    
file_paths = glob.glob("{}*.txt".format(file_path))

angles = []

#Find all angles
for path in file_paths:
    angle = np.int(path.split('_')[1])
    angles.append(angle)

max_angle = np.max(angles)

#Each indices of this array will represent the angles
results = [[] for _ in range(max_angle+1)]
    
for path in file_paths:
    
    print("\n----------------------------------------\n")
    
    print("Computing " + path.split('/')[-1] + " ...")
    
    angle = np.int(path.split('_')[1])
    
#    Gaussianfitter = s.data.fitter('a*exp(-(x-x0)**2/w**2)+b', 'a=1, b=0, x0=1000, w=25')#, ymin=4)
    Gaussianfitter = s.data.fitter('a*exp(-(x-x0)**2/w**2)+b', 'a=5, b=0, x0=4.3, w=0.1')#, ymin=4)
    d = s.data.load(path)
    time = np.float(d.headers['MEAS_TIM:'].split(' ')[0])
    d[0] = [conv.calibrate_channel(data) for data in range(len(d[0]))]
    d[0]=s.fun.coarsen_array(d[0], level=2, method='mean')
    d[1]=s.fun.coarsen_array(d[1], level=2, method='mean')
    Gaussianfitter.set_data(xdata=d[0], ydata=d[1], eydata=np.sqrt(d[1]))
#    Gaussianfitter.set(xlabel="Channels")
    Gaussianfitter.set(xlabel="Energy [MeV]")
    Gaussianfitter.set(ylabel="Counts")
    print("Click the peak!")
    click_x, click_y = Gaussianfitter.ginput()[0]
    Gaussianfitter(a=click_y, x0=click_x, xmin=click_x-0.5, xmax=click_x+0.5, ymin=np.max(d[1])*0.05)
    Gaussianfitter.fit()
#    Gaussianfitter.ginput()
    try:
        results[angle].append(Gaussianfitter.results[0][0]/time)
        results[angle].append(Gaussianfitter.results[1][0][0]/time)#There is no uncertainty on time
        results[angle].append(Gaussianfitter.results[0][2])
        results[angle].append(np.sqrt(Gaussianfitter.results[1][2][2]))
    except TypeError:
        print("\nWatch out! This particular dataset has not been accounted for (peak too small): {}".format(path.split('/')[-1]))
        pass
    plt.savefig("../assets/{}.svg".format(path.split('/')[-1].split('.')[0]))
    np.save("{}allResults".format(file_path), results)

#print(results)

results = np.load("{}allResults.npy".format(file_path))

#if combine_results == True:
#Combines results for every angles 
for angle in range(len(results)):
    if len(results[angle]) != 0:
        count_rates = results[angle][0::2]
        count_rates_err = results[angle][1::2]
        means = results[angle][2::2]
        stds = results[angle][3::2]
    #    results = np.zeroes(2)
    #    for i in range(len(means)):
        combined_cout_rate= np.mean(count_rates)
        combined_count_rate_err = hypot(count_rates_err)
        combined_means = np.mean(means)
        combined_stds = hypot(stds)
        #Writes over results
#            results[angle] = np.array([combined_means, combined_stds])
#        mean_std = conv.calibrate(combined_means, combined_stds)
        this_result = np.array([combined_cout_rate, combined_count_rate_err, combined_means, combined_stds])
        np.save('{}angle_{}'.format(file_path, angle), this_result)
        
        print("\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
        print("Saved data (in [count/sec] and [eV]) to: angle_{}.npy".format(angle))
        print("\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            
#npy_file = path.split('.')[0][:-6]
##    s[-1] = 'txt'
##    s='.'.join(s)
##Saves to new path
#np.save(('%s' %(npy_file)), results)
#print("\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
#print("Saved data (in [eV]) to: {}.npy".format(npy_file))
#print("\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
##    os.remove("%s" %path)
#os.chdir(original_dir)
##sys("mkdir ../calibrationResults")
#
##np.save("americium_alone", results)
##    np.save("../calibrationResults/americiumAlone", results)