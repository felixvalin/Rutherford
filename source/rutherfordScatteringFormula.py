#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 11:03:15 2017

@author: felixvalin
"""

import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import spinmob as s
from scipy import constants as const

#For font size!
font = {'family' : 'normal',
        'size'   : 15}

matplotlib.rc('font', **font)

datapath = "../database/scattering/"
foilpath = "../database/foilThickness/b6/"

thickness, err_thickness = np.load(foilpath+"b6.npy")

angle0 = np.load(datapath+"angle_0.npy")
angle10 = np.load(datapath+"angle_10.npy")
angle11 = np.load(datapath+"angle_11.npy")
angle15 = np.load(datapath+"angle_15.npy")
angle20 = np.load(datapath+"angle_20.npy")
angle30 = np.load(datapath+"angle_30.npy")

#err_angle = 0.25
err_angle = np.deg2rad(0.25)
angles = np.array([10,11,15,20,30])
angles = np.deg2rad(angles)

scatters = np.array([angle10, angle11, angle15, angle20, angle30])

def a_s():
    count_rate_zero = angle0[0]
    err_count_rate_zero = angle0[1]
    R_5 = 120.7
    A_c5 = 30
    a_s = (4*np.pi*R_5**2)/A_c5
    err_a_s = a_s*err_count_rate_zero/count_rate_zero
    return a_s, err_a_s

def I_0(a_s, err_a_s):
    A_c3 = 16
    R_3 = 50.8
    I_0 = (a_s*A_c3)/(4*np.pi*R_3**2)
    err_I_0 = I_0*err_a_s/a_s
    return I_0, err_I_0

def N_0(thickness, err_thickness):
    N_A = const.Avogadro
    M = 196.96655 #gold molar mass in g/mol
    n_0 = thickness*N_A/M
    err_n_0 = n_0*err_thickness/thickness
    return n_0, err_n_0

def cross_section(count_rate_angle, err_count_rate_angle, I_0, err_I_0, n_0, err_n_0):
    delta_omega = 0.09169
    cross_section = 10**27*count_rate_angle/(I_0*n_0*delta_omega)
    err_cross_section = cross_section*np.sqrt((err_count_rate_angle/count_rate_angle)**2+(err_I_0/I_0)**2+(err_n_0/n_0)**2)
    return cross_section, err_cross_section

def rutherford_formula(cross_section, err_cross_section, angle, err_angle, energy, err_energy):
    Z1 = 96
    Z2 = 79
    y = np.log(cross_section)
#    ey = np.log(err_cross_section)
    ey = err_cross_section/cross_section #error propagation
    
    x = np.log(1/(np.sin(angle/2))**4) + np.log(1.296*((Z1*Z2/energy)**2))
    exA = np.sqrt((2*np.tan(angle/2)*err_angle)**2) #Error propagation formula
    exB = np.sqrt((-2*err_energy/energy)**2) #Error propagation formula
    ex = np.sqrt(exA**2 + exB**2)
    
    return x, ex, y, ey

def rutherford_goodness():
    As, err_As = a_s()
    i_0, err_i_0 = I_0(As, err_As)
    n_0, err_n_0 = N_0(thickness, err_thickness)
    
    plotting_value = []
    for i, angle in enumerate(scatters):
        energy = angle[2]
        err_energy = angle[3]
        crosssection, err_crosssection = cross_section(angle[0], angle[1], i_0, err_i_0, n_0, err_n_0)
        plotting_value.append(rutherford_formula(crosssection, err_crosssection, angles[i], err_angle, energy, err_energy))
        
    return plotting_value

plotting_value = rutherford_goodness()

print([row[0] for row in plotting_value])
print([row[1] for row in plotting_value])
print([row[3] for row in plotting_value])

rutherford_fitter = s.data.fitter('m*x+b', 'm=1, b=0')
#rutherford_fitter = s.data.fitter('m*x', 'm=1')
rutherford_fitter.set_data(xdata=[row[0] for row in plotting_value], ydata=[row[2] for row in plotting_value], eydata=[row[3] for row in plotting_value])
#rutherford_fitter.set_data(xdata=[row[2] for row in plotting_value], ydata=[row[0] for row in plotting_value], eydata=[row[1] for row in plotting_value])
rutherford_fitter.set(xlabel="$\log [1/\sin^4 (\Theta/2)] + \log[1.296(Z_1Z_2/E)^2])$")
rutherford_fitter.set(ylabel="$\log [d\sigma/d\Omega]$")
rutherford_fitter.fit(xmax=25)
plt.savefig("../assets/rutherford_fit.svg")


    
