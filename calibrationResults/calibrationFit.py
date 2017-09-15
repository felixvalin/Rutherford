#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 10:04:15 2017

@author: felixvalin
"""

import spinmob as s
import numpy as np

results = np.load("mean_std.npy")

results = np.sort(results, 0)

calibrationFitter = s.data.fitter(f='a*(x-x0)', p='a=0.026, x0=28')#, x0=50')
calibrationFitter.set_data(xdata=results[:,0][1:], ydata=results[:,2][1:], eydata=0.1)#eydata=results[:,1])
calibrationFitter.set(xlabel='Channel')
calibrationFitter.set(ylabel='Voltage [V]')
calibrationFitter.fit()

#a_fit = np.array([calibrationFitter.results[0][0], calibrationFitter.results[1][0][0]])
#b_fit = np.array([calibrationFitter.results[0][1], calibrationFitter.results[1][1][1]])
#
#print(-b_fit[0]/a_fit[0])

calibResults = np.array([[calibrationFitter.results[0][0], calibrationFitter.results[1][0][0]],[calibrationFitter.results[0][1], calibrationFitter.results[1][1][1]]])

np.save("calibResults", calibrationFitter.results)

#results = []
#
## loop over the paths
#for path in paths:
#    
#    print("Converting " + path + " ...")
#    
#    Gaussianfitter = s.data.fitter('a*exp(-(x-x0)**2/w**2)+b', 'a=1, b=0, x0=1000, w=25')
#    d = s.data.load(path)
#    Gaussianfitter.set_data(xdata=d[0], ydata=d[1], eydata=np.sqrt(d[1]))
#    print("CLICK THE PEAK!!")
#    click_x, click_y = Gaussianfitter.ginput()[0]
#    Gaussianfitter(a=click_y, x0=click_x, xmin=click_x-200, xmax=click_x+200, ymin=0.5)
#    Gaussianfitter.fit()
#    fitVolts = np.int(path.split('.')[0].split('_')[2][:-1])
#    
#    results.append(np.array([Gaussianfitter.results[0][2], Gaussianfitter.results[0][3], fitVolts]))
#
#sys("mkdir ../calibrationResults")
#

