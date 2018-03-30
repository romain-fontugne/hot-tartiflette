import ihrData
import welch
import mapitData
from matplotlib import pyplot as plt
from scipy import signal
import numpy as np
import logging

# if __name__ == "__main__":
def ecdf(a, ax=None, **kwargs):
    sorted=np.sort( a )
    yvals=np.arange(len(sorted))/float(len(sorted))
    if ax is None:
        plt.plot( sorted, yvals, **kwargs )
    else:
        ax.plot( sorted, yvals, **kwargs )


def plotSignal(link):
    x = ihr.signals[link]["diffmedian"]
    plt.figure()
    plt.title(link)
    plt.plot(x)
    plt.show()


plotSpectrums = True
minAppearance = 20
nperseg = 512

# Raw data
mapit = mapitData.mapitData()
mapit.loadData()
ihr = ihrData.ihrData(fnames=["data/7922.csv", "data/1239.csv", "data/5511.csv", "data/7018.csv"], minAppearance=minAppearance)
ihr.loadData() 

nbAppearance = []
for link in np.unique(ihr.data["link"]):
    nbAppearance.append(len(ihr.data[ ihr.data["link"] == link ]))

plt.figure()
ecdf(nbAppearance)
plt.vlines(minAppearance,0,1,"k","dashed")
plt.xscale("log")
plt.tight_layout()
plt.savefig("fig/nbAppearance.pdf")



# Frequency Analysis
wel = welch.Welch(nperseg=nperseg)

print "Total number of links: %s" % len(np.unique(ihr.data["link"]))
print "Analyzed links: %s" % len(ihr.signals)

wel.analyze(ihr.signals)

maxValues = {"x":[], "y":[]}
nbLinks = 0 
nbInterdomainLinks = 0
for link, (f, Pxx_spec) in wel.pspec.iteritems():
    # Plot spectrums
    if np.sqrt(Pxx_spec.max())>10:
        maxValues["x"].append( f[Pxx_spec.argmax()] )
        maxValues["y"].append(np.sqrt(Pxx_spec.max())) 

        peer = False
        for ip in link[1:-1].split(","):
            if mapit.isInterdomain(ip) is not None:
                peer = True

        if peer:
            nbInterdomainLinks += 1

        nbLinks += 1

        if plotSpectrums:
            plt.figure()
            # plt.semilogy(f, np.sqrt(Pxx_spec))
            plt.plot(f, np.sqrt(Pxx_spec))
            plt.vlines([1.0/(3600*24)], plt.ylim()[0], plt.ylim()[1], "r", "dashed")
            plt.vlines([1.0/(3600*24*7)], plt.ylim()[0], plt.ylim()[1], "b", "dashed")
            plt.xlabel('frequency [Hz]')
            plt.ylabel('Power spectrum')
            plt.tight_layout()
            plt.savefig("fig/spectrums/%s.pdf" % link)
            plt.close()
                

print("Number of interdomain links: %s/%s" % ( nbInterdomainLinks, nbLinks))
# Scatter plot of maximum peak values
plt.figure()
plt.plot(maxValues["x"], maxValues["y"], ".")
plt.vlines([1.0/(3600*24)], 10, 20, "r")
plt.vlines([1.0/(3600*24*7)], 10, 20, "b")
plt.vlines([1.0/(3600*24*14)], 10, 20, "g")
plt.yscale("log")
plt.grid(True)
# plt.xlim([0, 0.00002])
plt.xlabel("Frequency (Hz)")
plt.ylabel("Estimated RMS")
plt.tight_layout()
plt.savefig("fig/maxPeaks.pdf")
plt.close()

plt.figure()
ecdf(maxValues["x"])
plt.tight_layout()
plt.savefig("fig/maxFreq.pdf")

# plotSignal("(154.54.5.106,50.248.118.237)")
