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
# minDuration = 90*24
minSample = 12 

nperseg = 30*24
minRMS = 10 

# initialisation of logger
FORMAT = '%(asctime)s %(processName)s %(message)s'
logging.basicConfig(format=FORMAT, filename='hot-tartiflette.log', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')
logging.info("Started")

# Load data
mapit = mapitData.MapitData()
mapit.loadData()
# ihr = ihrData.IhrData(fnames=["data/7922.csv", "data/1239.csv", "data/5511.csv", "data/7018.csv"], minDuration=minDuration, minSample=minSample)
ihr = ihrData.IhrData(fnames=["data/ihr_delay_alarms_20180403.csv"],  minDate=minDate, minSample=minSample)
ihr.loadData() 

# Frequency Analysis
wel = welch.Welch(nperseg=nperseg, minRMS=minRMS)
wel.analyze(ihr.signals)


if __name__ == "__main__":
    logging.info("Plotting results...")
    # Plot Results
    plt = plotter.Plotter(ihr, wel, mapit)
    for link, (f, Pxx_spec) in wel.pspec.iteritems():
        if f[Pxx_spec.argmax()]< 1.0/(3600*24*90):
            print link
            plt.signal(link)
            plt.spectrum(link)

    # plt.alarmsDistribution()
    plt.freqRMSscatterplot()
    if plotSpectrums:
        logging.info("Plotting spectrums...")
        plt.allSpectrums()
    if plotSignals:
        logging.info("Plotting signals...")
        plt.allSignals()

    logging.info("Number of interdomain links: %s/%s" % ( len(plt.interdomainLinks), plt.nbLinks))
