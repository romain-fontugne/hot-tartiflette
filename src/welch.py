from scipy import signal
import numpy as np
import logging

class Welch(object):
    def __init__(self, nperseg=256, fs=1.0, minRMS=5):

        self.nperseg = nperseg
        self.fs = fs
        self.pspec = {}
        self.minRMS = minRMS

    
    def analyze(self, signals):
        logging.debug("Frequency analysis...")
        for link, sig in signals.iteritems():

            # f, Pxx_spec = signal.welch(sig, self.fs, 
                    # nperseg=self.nperseg,  scaling="spectrum", detrend="linear")
            f, Pxx_spec = signal.periodogram(sig, self.fs, scaling="spectrum", detrend="linear")

            # midHigh = np.argwhere(f>1.0/(7*24))
            # f = f[midHigh]
            # Pxx_spec = Pxx_spec[midHigh]
            
            if np.sqrt(Pxx_spec.max())>self.minRMS:
                self.pspec[link] = (f, Pxx_spec)
 
