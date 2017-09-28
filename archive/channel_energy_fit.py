#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 14:19:15 2017

@author: felixvalin
"""

import spinmob as s
import numpy as np
import os

os.chdir("../database/")

zero_energy = np.load("channelToVolt_params.npy")[0]
#zero_energy = fitResults[1]

americium = np.load("americium_alone.npy")[0]
americium_energy = 5.486

channels = np.array([zero_energy[0],americium[0]])
energy = np.array([0,americium_energy])

Gaussianfitter = s.data.fitter('a*x+b', 'a=1, b=0')
Gaussianfitter.set_data(xdata=energy, ydata=channels, eydata=[np.sqrt(zero_energy[1]), np.sqrt(americium[1])])
Gaussianfitter.set(xlabel='Energy [MeV]')
Gaussianfitter.set(ylabel='Channel')
Gaussianfitter.fit()

slope = Gaussianfitter.results[0][0]
slope_err = np.sqrt(Gaussianfitter.results[1][0][0])
intercept = Gaussianfitter.results[0][1]
intercept_err = np.sqrt(Gaussianfitter.results[1][1][1])

params = np.array([[slope, slope_err],[intercept, intercept_err]])

np.save("energy_vs_channel_params", params)