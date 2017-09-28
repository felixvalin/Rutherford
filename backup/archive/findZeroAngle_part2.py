#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 14:23:03 2017

@author: felixvalin
"""

import spinmob as s
import matplotlib.pyplot as plt
import numpy as np
import os

os.chdir("../database/angle/")

d = np.load('zeroAngle_Mean_Error.npy')

zeroFitter = s.data.fitter('a*exp(-(x-x0)**2/w**2)+b', 'a=1, b=0, x0=0, w=3')#, ymin=4)
zeroFitter.set_data(xdata=d[:,2], ydata=d[:,0], eydata=d[:,1])
click_x, click_y = zeroFitter.ginput()[0]
print("CLICK THE PEAK!!")
zeroFitter(a=click_y, x0=click_x, xmin=click_x-200, xmax=click_x+200, ymin=0.5)
zeroFitter.fit()
zeroFitter.ginput()

trueAngle = zeroFitter.results[0][2]
trueAngle_err = zeroFitter.results[1][2][2]

np.save('trueAngle', [trueAngle, trueAngle_err])