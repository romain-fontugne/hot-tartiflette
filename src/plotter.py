import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


def ecdf(a, ax=None, **kwargs):
    sorted=np.sort( a )
    yvals=np.arange(1,len(sorted)+1)/float(len(sorted))
    if ax is None:
        plt.plot( sorted, yvals, **kwargs )
    else:
        ax.plot( sorted, yvals, **kwargs )

def vecdf(a, ax=None, **kwargs):
    sorted=np.sort( a )
    yvals=np.arange(1,len(sorted)+1)/float(len(sorted))
    if ax is None:
        plt.plot( yvals,sorted,  **kwargs )
    else:
        ax.plot( yvals,sorted,  **kwargs )



class Plotter(object):
    def __init__(self, ihr, welch, mapit=None):

        self.ihr = ihr
        self.welch = welch
        self.mapit = mapit
        self.interdomainLinks = {}
        self.nbLinks = 0
    

    def allSignals(self):
        for link in self.welch.pspec.iterkeys():
            self.signal(link)


    def signal(self, link):
        x = self.ihr.signals[link]
        plt.figure(figsize=(8,4))
        plt.title(link)
        plt.plot(x)
        plt.savefig("fig/signals/%s.pdf" % link)
        plt.close()
    

    def allSpectrums(self):
        for link  in self.welch.pspec.iterkeys():
            self.spectrum(link)


    def spectrum(self, link):
        f, Pxx_spec = self.welch.pspec[link]

        plt.figure()
        plt.plot(f, np.sqrt(Pxx_spec))
        # plt.vlines([1.0/(3600*24)], plt.ylim()[0], plt.ylim()[1], "r", "dashed")
        # plt.vlines([1.0/(3600*24*7)], plt.ylim()[0], plt.ylim()[1], "b", "dashed")
        plt.xlabel('Frequency')
        plt.ylabel('RMS')
        plt.tight_layout()
        # Assume freqRMSscatterplot is executed before this
        if link in self.interdomainLinks:
            plt.savefig("fig/spectrums/interdomain/%s_maxfreq%s_avgamp%s.pdf" 
                    % (link, f[Pxx_spec.argmax()], np.sqrt(Pxx_spec.max())))
        else:
            plt.savefig("fig/spectrums/intradomain/%s_maxfreq%s_avgamp%s.pdf" 
                    % (link, f[Pxx_spec.argmax()], np.sqrt(Pxx_spec.max())))
        plt.close()


    # TODO optimize this function
    def alarmsDistribution(self, threshold=None):
        nbAlarms = []
        for link in np.unique(self.ihr.data["link"]):
            # A link appears twice in the same time bin
            nbAlarms.append(len(np.unique((self.ihr.data[ self.ihr.data["link"] == link ]).index)))

        plt.figure()
        ecdf(nbAlarms)
        if threshold is not None:
            plt.vlines(threshold,0,1,"k","dashed")
        plt.xscale("log")
        plt.xlabel("Number of alarms per link")
        plt.ylabel("CDF")
        plt.tight_layout()
        plt.savefig("fig/nbAlarms.pdf")
        plt.close()


    # TODO optimize this function?
    def alarmsDurationDistribution(self, threshold=None):
        duration = []
        for link, linkData in self.ihr.data.groupby("link"):
            # linkData = self.ihr.linkData(link)
            if len(linkData):
                duration.append((linkData.index[-1]-linkData.index[0]).total_seconds()/3600)

        plt.figure()
        ecdf(duration)
        if threshold is not None:
            plt.vlines(threshold,0,1,"0.5","dashed")
        plt.xscale("log")
        plt.xlabel("Reports duration per link")
        plt.ylabel("CDF")
        plt.tight_layout()
        plt.savefig("fig/alarmsDuration.pdf")
        plt.close()


    def freqRMSscatterplot(self):
        maxValues = {"x":[], "y":[]}
        maxValuesInter = {"x":[], "y":[]}
        self.nbLinks = 0 
        for link, (f, Pxx_spec) in self.welch.pspec.iteritems():
            # Plot spectrums
            link = link.rpartition("_")[0]
            peer = False
            if self.mapit.isInterdomain(link) is not None:
                peer = True

            if peer:
                self.interdomainLinks[link] = True
                maxValuesInter["x"].append( f[Pxx_spec.argmax()] )
                maxValuesInter["y"].append(np.sqrt(Pxx_spec.max())) 
            else:
                maxValues["x"].append( f[Pxx_spec.argmax()] )
                maxValues["y"].append(np.sqrt(Pxx_spec.max())) 

            self.nbLinks += 1

        # Scatter plot of maximum peak values
        plt.figure(figsize=(5,5))
        axScatter = plt.subplot(111)
        axScatter.plot(maxValuesInter["x"], maxValuesInter["y"], "*")
        axScatter.plot(maxValues["x"], maxValues["y"], ".")
        # axScatter.set_aspect(1.)

        axScatter.set_yscale("log")
        axScatter.set_xscale("log")
        axScatter.set_xlabel("Frequency")
        axScatter.set_ylabel("RMS")

        # create new axes on the right and on the top of the current axes.
        divider = make_axes_locatable(axScatter)
        axHistx = divider.append_axes("top", size=1.2, pad=0.1, sharex=axScatter)
        axHisty = divider.append_axes("right", size=1.2, pad=0.1, sharey=axScatter)

        ecdf(maxValuesInter["x"], ax=axHistx)
        ecdf(maxValues["x"], ax=axHistx)
        vecdf(maxValuesInter["y"], ax=axHisty)
        vecdf(maxValues["y"], ax=axHisty)

        # no labels
        plt.setp(axHistx.get_xticklabels(), visible=False)
        plt.setp(axHisty.get_yticklabels(), visible=False)
        axHistx.set_ylabel("CDF")
        axHisty.set_xlabel("CDF")

        # axScatter.set_xticks([1.0/(24*30), 1.0/(24*7*2), 1.0/(24*7), 1.0/(24*3), 1.0/(24), 1.0/(6)])
        # axScatter.set_xticklabels([r"$\frac{1}{30 days}$", r"$\frac{1}{14 days}$", r"$\frac{1}{7 days}$", r"$\frac{1}{3 days}$", r"$\frac{1}{1 day}$", r"$\frac{1}{6 hours}$"])
        axScatter.set_xticks([1.0/(24*30), 1.0/(24*7), 1.0/(24), 1.0/(4)])
        axScatter.set_xticklabels([ r"$\frac{1}{1 month}$", r"$\frac{1}{1 week}$", r"$\frac{1}{1 day}$", r"$\frac{1}{4 hours}$"])
        axScatter.set_yticks([10, 50, 100, 200])
        axScatter.set_yticklabels(["10ms", "50ms", "100ms", "200ms"])
        axHistx.set_yticks([0.0, 0.5, 1.0])
        axHisty.set_xticks([0.0, 0.5, 1.0])
        plt.tight_layout()
        plt.savefig("fig/maxPeaks.pdf")
        plt.close()

