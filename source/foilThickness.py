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
        'size' : 15}

matplotlib.rc('font', **font)

copperP = np.load("../database/foilThickness/copperP.npy")
aluminumP = np.load("../database/foilThickness/aluminumP.npy")
goldP = np.load("../database/foilThickness/goldP.npy")
nofoil = np.load("../database/foilThickness/noFoil/NoFoil.npy")
b1 = np.load("../database/foilThickness/b1/b1.npy") #Gold
b3 = np.load("../database/foilThickness/b3/b3.npy") #Gold
b6 = np.load("../database/foilThickness/b6/b6.npy") #Gold
f1 = np.load("../database/foilThickness/f1/f1.npy") #Aluminum
f5 = np.load("../database/foilThickness/f5/f5.npy") #Copper

def thickness(nofoil, foil, materialP):
    #Retreives material, foils params
    a, b, c = materialP[:-1][0::2]
    ea, eb, ec = materialP[:-1][1::2]

    nf, enf = nofoil
    f, ef = foil
    
    #test 
    E0 = nf-f
    eE0 = np.sqrt(nf**2+f**2)
    
    #Computes range for foil
    Af = a*E0**2
    Bf = b*E0
    Ef = Af+Bf+c
    #error on foil Range
    eAf = np.sqrt((E0**2*ea)**2 + (2*E0*a*eE0)**2)
    eBf = np.sqrt((E0*eb)**2 + (b*eE0)**2)
    eEf = np.sqrt(eAf**2+eBf**2+ec**2)

    return Ef, eEf

b1_thickness = thickness(nofoil, b1, goldP)
b3_thickness = thickness(nofoil, b3, goldP)
b6_thickness = thickness(nofoil, b6, goldP)
f1_thickness = thickness(nofoil, f1, aluminumP)
f5_thickness = thickness(nofoil, f5, copperP)

thicknesses = np.array([[b1_thickness, "b1"]])
thicknesses = np.append(thicknesses, [[b3_thickness, "b3"]], axis=0)
thicknesses = np.append(thicknesses, [[b6_thickness, "b6"]], axis=0)
thicknesses = np.append(thicknesses, [[f1_thickness, "f1"]], axis=0)
thicknesses = np.append(thicknesses, [[f5_thickness, "f5"]], axis=0)

print(thicknesses)

np.save("../database/foilThickness/thicknesses", thicknesses)