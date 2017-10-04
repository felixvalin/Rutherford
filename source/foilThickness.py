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
    a, ea = materialP[0]
    b, eb = materialP[1]
    c, ec = materialP[2]
    nf, enf = nofoil
    f, ef = foil
    
    #Computes range for foil
    Af = a*f**2
    Bf = b*f
    Ef = Af+Bf+c
    #error on foil Range
    eAf = np.sqrt((f**2*ea)**2 + (2*f*a*ef)**2)
    eBf = np.sqrt((f*eb)**2 + (b*ef)**2)
    eEf = np.sqrt(eAf**2+eBf**2+ec**2)
    
    #Computes range for no foil
    Anf = a*nf**2
    Bnf = b*nf
    Enf = Anf+Bnf+c
    #error on no foil range
    eAnf = np.sqrt((nf**2*ea)**2 + (2*nf*a*enf)**2)
    eBnf = np.sqrt((nf*eb)**2 + (b*enf)**2)
    eEnf = np.sqrt(eAnf**2+eBnf**2+ec**2) 
    
    return (Enf - Ef), np.sqrt(eEnf**2+eEf**2)

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


np.save("../database/foilThickness/thicknesses", thicknesses)