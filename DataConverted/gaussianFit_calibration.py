import glob
import spinmob as s
import numpy as np
import matplotlib.pyplot as plt
from os import system as sys
paths = glob.glob("*.txt")
print(paths)
results = []

# loop over the paths
for path in paths:
        
    print("Converting " + path + " ...")
    
    Gaussianfitter = s.data.fitter('a*exp(-(x-x0)**2/w**2)+b', 'a=1, b=0, x0=1000, w=25', ymin=4)
    d = s.data.load(path)
    Gaussianfitter.set_data(xdata=d[0], ydata=d[1], eydata=np.sqrt(d[1]))
    print("CLICK THE PEAK!!")
    click_x, click_y = Gaussianfitter.ginput()[0]
    Gaussianfitter(a=click_y, x0=click_x, xmin=click_x-200, xmax=click_x+200, ymin=0.5)
    Gaussianfitter.fit()
    Gaussianfitter.ginput()
    fitVolts = np.int(path.split('.')[0].split('_')[2][:-1])
#    plt.savefit("wrongFit.png")
    
    results.append(np.array([Gaussianfitter.results[0][2], Gaussianfitter.results[1][2][2], fitVolts]))

#sys("mkdir ../calibrationResults")

np.save("../calibrationResults/mean_std", results)
#np.save("../calibrationResults/americiumAlone", results)