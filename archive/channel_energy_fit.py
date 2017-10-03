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

dy = channels[1] - channels[0]
dx = energy[1] - energy[0]
edy = np.sqrt(zero_energy[1]**2 + americium[1]**2)
slope = dy/dx
slope_err = edy/dx

intercept = americium[0] - slope*americium_energy
intercept_err = np.sqrt(americium[1]**2 + (slope_err*americium_energy)**2)

params = np.array([[slope, slope_err],[intercept, intercept_err]])
#print(params)

np.save("energy_vs_channel_params", params)