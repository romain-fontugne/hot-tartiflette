import ihrData
import welch
import mapitData
import plotter 
from matplotlib import pyplot as plt
from scipy import signal
import numpy as np
import logging
from datetime import datetime

# 
plotSpectrums = False
plotSignals = False
minDate = datetime(2017,1,1)
minSample = 30 

nperseg = 4*24
minRMS = 10 

# initialisation of logger
FORMAT = '%(asctime)s %(processName)s %(message)s'
logging.basicConfig(format=FORMAT, filename='hot-tartiflette.log', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')
logging.info("Started")

# Load data
mapit = mapitData.MapitData()
mapit.loadData()
ihr = ihrData.IhrData(fnames=["data/ihr_delay_alarms_20180403.csv"],  minDate=minDate, minSample=minSample)
ihr.loadData() 

# Frequency Analysis
wel = welch.Welch(nperseg=nperseg, minRMS=minRMS)
wel.analyze(ihr.signals)

fi = open("data/hotLinks.csv","w")
for link, (f, pspec) in wel.pspec.iteritems():
    freqMax = f[pspec.argmax()]
    print freqMax
    if freqMax < 1.0/23 and freqMax > 1.0/25:
        ampMax = np.sqrt(pspec.max())
        fi.write("%s, %s, %s, %s\n" % (link[0], link[1], freqMax, ampMax))
fi.close()

if __name__ == "__main__":
    logging.info("Plotting results...")
    # Plot Results
    plt = plotter.Plotter(ihr, wel, mapit)

    # plt.alarmsDistribution()
    plt.freqRMSscatterplot()
    if plotSpectrums:
        logging.info("Plotting spectrums...")
        plt.allSpectrums()
    if plotSignals:
        logging.info("Plotting signals...")
        plt.allSignals()

    # for link, (f, Pxx_spec) in wel.pspec.iteritems():
        # if f[Pxx_spec.argmax()]< 1.0/(24*21):
            # print link
            # plt.signal(link)
            # plt.spectrum(link)

    logging.info("Number of interdomain links: %s/%s" % ( len(plt.interdomainLinks), plt.nbLinks))
