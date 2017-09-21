import glob
import spinmob as s
import numpy as np
import matplotlib.pyplot as plt
import os
os.chdir("../assets/data/foilThickness")
paths = glob.glob("*/")

results = []

# loop over the paths
for path in paths:

    print("Inspecting " + path[:-1] + " ...")
    os.chdir(path)

    subpaths = glob.glob("*.txt")

    for subpath in subpaths:

        print("Converting " + path + "/" + subpath + " ...")

        Gaussianfitter = s.data.fitter('a*exp(-(x-x0)**2/w**2)+b', 'a=1, b=0, x0=1000, w=25', ymin=4)
        d = s.data.load(subpath)
        Gaussianfitter.set_data(xdata=d[0], ydata=d[1], eydata=np.sqrt(d[1]))
        print("CLICK THE PEAK!!")
        click_x, click_y = Gaussianfitter.ginput()[0]
        Gaussianfitter(a=click_y, x0=click_x, xmin=click_x-200, xmax=click_x+200, ymin=0.5)
        Gaussianfitter.fit()
        Gaussianfitter.ginput()
        peakChannel = Gaussianfitter.results[0][2]
        peakError = Gaussianfitter.results[1][2][2]

        s = path.split(".")
        run = s[-3:]

        results.append(np.array([peakChannel, peakError, run]))

        os.rename("{0}".format(path), "~/git-repos/Rutherford/NoNeed/")#Not sure this works yet!

#sys("mkdir ../calibrationResults")
    os.mkdir("../../foilThickness/{0}".format(path))#Might not work yet


    np.save("../../foilThickness/{0}/results".format(path), results)
#np.save("../calibrationResults/americiumAlone", results)
