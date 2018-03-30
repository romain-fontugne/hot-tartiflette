from scipy import signal
import numpy as np

class Welch(object):
    def __init__(self, nperseg=256, fs=1.0/3600):

        self.nperseg = nperseg
        self.fs = fs
        self.pspec = {}

    
    def analyze(self, signals):
        for link, sig in signals.iteritems():
            # if len(sig>1024):
                # plt.figure()
                # plt.title(link)
                # plt.plot(sig["diffmedian"])

                if 0:
                    f, Pxx_den = signal.welch(sig["diffmedian"], fs, nperseg=self.nperseg)
                    # plt.figure()
                    # plt.semilogy(f, Pxx_den)
                    # # plt.ylim([0.5e-3, 1])
                    # plt.vlines([1.0/(3600*24*7), 1.0/(3600*24)], plt.ylim()[0], plt.ylim()[1], "r", "dashed")
                    # plt.xlabel('frequency [Hz]')
                    # plt.ylabel('PSD [V**2/Hz]')
                    # plt.show()

                if 1:
                    f, Pxx_spec = signal.welch(sig["diffmedian"], self.fs, nperseg=self.nperseg, scaling='spectrum')
                    self.pspec[link] = (f, Pxx_spec)

