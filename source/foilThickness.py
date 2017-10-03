#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 16:40:23 2017

@author: felix
"""

#import convertChannelToEnergy as conv
import numpy as np
#import os
import spinmob as s
import matplotlib.pyplot as plt
import matplotlib

font = {'family' : 'normal',
        'size' : 13}

matplotlib.rc('font', **font)


e0 = np.array([0.5,0.75,1.0,1.20,1.30,1.50,2.0,2.5,3.0,3.4,3.6,4.0,4.4,4.6,5.0,5.5,6,7])
copper = np.array([1.06,1.38,1.69,1.95,2.08,2.36,3.11,3.93,4.82,5.58,5.98,6.81,7.68,8.13,9.06,10.3,11.6,14.3])
aluminum = np.array([0.65,0.82,0.99,1.15,1.23,1.39,1.85,2.37,2.94,3.44,3.7,4.25,4.84,5.15,5.79,6.63,7.53,9.48])
gold = np.array([1.9,2.5,3.12,3.64,3.91,4.47,5.97,7.59,9.34,10.8,11.6,13.2,14.8,15.7,17.4,19.7,22.1,27.1])

#plt.figure()

copperF = s.data.fitter(f='a*x**2+b*x+c', p='a=1.0,b=1.0,c=0')
copperF.set_data(xdata=e0, ydata=copper, eydata=0.01)
copperF.set(xlabel="$E_0$")
copperF.set(ylabel="Ranges for Copper [mg/cm$^2$]")
copperF.fit()
plt.savefig("../assets/copperThickness.svg")
copperP = np.array([[copperF.results[0][0], np.sqrt(copperF.results[1][0][0])]])
copperP = np.append(copperP,[[copperF.results[0][1], np.sqrt(copperF.results[1][1][1])]], axis=0)
copperP = np.append(copperP,[[copperF.results[0][2], np.sqrt(copperF.results[1][2][2])]], axis=0)
np.save("../database/foilThickness/copperP", copperP)

aluminumF = s.data.fitter(f='a*x**2+b*x+c', p='a=1.0,b=1.0,c=0')
aluminumF.set_data(xdata=e0, ydata=aluminum, eydata=0.01)
aluminumF.set(xlabel="$E_0$")
aluminumF.set(ylabel="Ranges for Aluminum [mg/cm$^2$]")
aluminumF.fit()
plt.savefig("../assets/aluminumThickness.svg")
aluminumP = np.array([[aluminumF.results[0][0], np.sqrt(aluminumF.results[1][0][0])]])
aluminumP = np.append(aluminumP,[[aluminumF.results[0][1], np.sqrt(aluminumF.results[1][1][1])]], axis=0)
aluminumP = np.append(aluminumP,[[aluminumF.results[0][2], np.sqrt(aluminumF.results[1][2][2])]], axis=0)
np.save("../database/foilThickness/aluminumP", aluminumP)

goldF = s.data.fitter(f='a*x**2+b*x+c', p='a=1.0,b=1.0,c=0')
goldF.set_data(xdata=e0, ydata=gold, eydata=0.01)
goldF.set(xlabel="$E_0$")
goldF.set(ylabel="Ranges for Gold [mg/cm$^2$]")
goldF.fit()
plt.savefig("../assets/goldThickness.svg")
goldP = np.array([[goldF.results[0][0], np.sqrt(goldF.results[1][0][0])]])
goldP = np.append(goldP,[[goldF.results[0][1], np.sqrt(goldF.results[1][1][1])]], axis=0)
goldP = np.append(goldP,[[goldF.results[0][2], np.sqrt(goldF.results[1][2][2])]], axis=0)
np.save("../database/foilThickness/goldP", goldP)
