#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 14:01:53 2017

@author: felixvalin
"""



import spinmob as s
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import glob
import os
import convertChannelToEnergy as conv

#For font size!
font = {'family' : 'normal',
        'size'   : 15}

matplotlib.rc('font', **font)

os.chdir("../database/angle/")

paths = glob.glob("*.txt")

results = []

# loop over the paths
for path in paths:
        
    print("Processing " + path + " ...")    
#    s.tweaks.ubertidy()
    Gaussianfitter = s.data.fitter('a*exp(-(x-x0)**2/w**2)+b', 'a=1, b=0, x0=4.2, w=1')#, ymin=4)
    d = s.data.load(path)
    d[0] = [conv.calibrate_channel(data) for data in range(len(d[0]))]
    Gaussianfitter.set_data(xdata=d[0], ydata=d[1], eydata=np.sqrt(d[1]))
    Gaussianfitter.set(plot_guess=False)
    Gaussianfitter.set(xlabel="Energy [MeV]")
    Gaussianfitter.set(ylabel="Counts")
    print("CLICK THE PEAK!!")
    click_x, click_y = Gaussianfitter.ginput()[0]
    Gaussianfitter(a=click_y, x0=click_x, xmin=click_x-1, xmax=click_x+1, ymin=0.5)
    Gaussianfitter.fit()
    s.tweaks.ubertidy()
#    Gaussianfitter.ginput()
    time = d.headers['MEAS_TIM:'].split(' ')
    time = np.float(time[0])#+'.'+time[1])
#    mean = Gaussianfitter.results[0][2]/time
    mean = Gaussianfitter.results[0][0]/time
    error = mean * np.sqrt(Gaussianfitter.results[1][0][0])/Gaussianfitter.results[0][0]#Error propagation formula
    energy = Gaussianfitter.results[0][2]
    energy_err = np.sqrt(Gaussianfitter.results[1][2][2])
    angle = np.float(path.split('_')[1][:-4])
    rcs = Gaussianfitter.reduced_chi_squareds()[0]
    #    plt.savefit("wrongFit.png")
    
    results.append(np.array([mean, error, energy,  energy_err, angle, rcs]))
    
    plt.savefig("../../assets/{}.svg".format(path.split('.')[0]))

#sys("mkdir ../calibrationResults")

np.save("zeroAngle_Mean_Error", results)
#os.rm("*.txt")
#np.save("../calibrationResults/americiumAlone", results)