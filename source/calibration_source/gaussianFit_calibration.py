import glob
import spinmob as s
import numpy as np
import matplotlib.pyplot as plt
import os

os.chdir("../../database/")

paths = glob.glob("Americium_peak_alone.txt")

results = []

# loop over the paths
for path in paths:
        
    print("Converting " + path + " ...")
    
    Gaussianfitter = s.data.fitter('a*exp(-(x-x0)**2/w**2)+b', 'a=1, b=0, x0=1000, w=25', ymin=4)
    d = s.data.load(path)
    d[0]=s.fun.coarsen_array(d[0], level=2, method='mean')
    d[1]=s.fun.coarsen_array(d[1], level=2, method='mean')
    Gaussianfitter.set_data(xdata=d[0], ydata=d[1], eydata=np.sqrt(d[1]))
    print("CLICK THE PEAK!!")
    click_x, click_y = Gaussianfitter.ginput()[0]
    Gaussianfitter(a=click_y, x0=click_x, xmin=click_x-200, xmax=click_x+200, ymin=1)
    Gaussianfitter.fit()
    print(Gaussianfitter.reduced_chi_squareds)
    Gaussianfitter.ginput()
#    fitVolts = np.int(path.split('.')[0].split('_')[2][:-1])
#    plt.savefit("wrongFit.png")
    
    results.append(np.array([Gaussianfitter.results[0][2], Gaussianfitter.results[1][2][2]]))#, fitVolts]))

#sys("mkdir ../calibrationResults")

np.save("americium_alone", results)
#np.save("../calibrationResults/americiumAlone", results)