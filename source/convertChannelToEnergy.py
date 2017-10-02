# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import spinmob as s
import numpy as np
import matplotlib.pyplot as plt

channelToEnergy_params = np.load("../database/energy_vs_channel_params.npy")

a1, ea1 = channelToEnergy_params[0]
b1, eb1 = channelToEnergy_params[1]


#(a1*CHANNEL+b1-b2)/a2 to get MeV from Channel

def calibrate(channel, channel_err):
    
    result1 = channel-b1
    err1 = np.sqrt(channel_err**2+eb1**2)
    
    energy = result1/a1
    energy_err = energy*np.sqrt((err1/result1)**2+(ea1/a1)**2)   
    
    return energy, energy_err

def calibrate_channel(channel):
    
    result1 = channel-b1
    energy = result1/a1
    
    return energy