#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 14:23:03 2017

@author: felixvalin
"""

import spinmob as s
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os

#For font size!
font = {'family' : 'normal',
        'size'   : 13}

matplotlib.rc('font', **font)

os.chdir("../database/angle/")

d = np.load('zeroAngle_Mean_Error.npy')

zeroFitter = s.data.fitter('a*exp(-(x-x0)**2/w**2)+b', 'a=1, b=0, x0=0, w=3')#, ymin=4)
zeroFitter.set_data(xdata=d[:,2], ydata=d[:,0], eydata=d[:,1])
zeroFitter.set(plot_guess=False)
zeroFitter.set(xlabel="Angle [Degrees]")
zeroFitter.set(ylabel="Count Rate [Counts/Sec]")
click_x, click_y = zeroFitter.ginput()[0]
print("CLICK THE PEAK!!")
zeroFitter(a=click_y, x0=click_x, xmin=click_x-200, xmax=click_x+200, ymin=0.5)
zeroFitter.fit()
plt.savefig("../../assets/true_Zero.svg")
zeroFitter.ginput()

trueAngle = zeroFitter.results[0][2]
trueAngle_err = zeroFitter.results[1][2][2]
rcs = zeroFitter.reduced_chi_squareds()[0]
results = np.array([trueAngle, trueAngle_err, rcs])

np.save('trueAngle', results)