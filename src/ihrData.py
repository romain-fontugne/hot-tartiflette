from numpy import concatenate
from datetime import datetime
import numpy as np
import pandas as pd

class ihrData(object):
    """Retrive and format Internet Health Report data. """

    def __init__(self, fnames, minAppearance=7, minDate = datetime(2017,1,1)):
        """Initialize attributes. """

        self.data = None
        self.signals = {}
        self.features = None
        self.fnames = fnames 
        self.scaler = None
        self.minAppearance = minAppearance 
        self.linkAppearance = []
        self.minDate = minDate


    def readRawData(self):
        """Grab raw data from ihr and put it in a pandas data frame."""

        dataset = []
        for fi in self.fnames:
            dataset.append(pd.read_csv( fi, header=None, 
                names=["timebin", "ip0", "ip1", "diffmedian", "deviation", "nbprobes"]))
        
        df = pd.concat(dataset)
        df.index = pd.DatetimeIndex(df.timebin)
        del df["timebin"]

        self.data = df


    def cleanData(self):
        """Filter out links to be ignored in the analysis."""

        self.data["link"] = self.data["ip0"]+","+self.data["ip1"]
        del self.data["ip0"]
        del self.data["ip1"]

        # Remove links that rarely appeared	
        for link in np.unique(self.data["link"]):
            datalink = self.data[(self.data["link"] == link) & (self.data.index >= self.minDate)]
            self.linkAppearance.append(len(datalink))
            if len(datalink) > self.minAppearance:
                self.signals[link] = datalink.resample("H").sum() 


    def loadData(self):
        """Load raw data and prepare it for analysis.

        return data, label"""

        self.readRawData()
        self.cleanData()

