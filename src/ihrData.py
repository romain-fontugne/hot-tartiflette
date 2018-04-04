from numpy import concatenate
import logging
from datetime import datetime
import numpy as np
import pandas as pd

class IhrData(object):
    """Retrive and format Internet Health Report data. """

    def __init__(self, fnames, minDuration=90*24, minSample=12, minDate=datetime(2017,1,1)):
        """Initialize attributes. """

        self.data = None
        self.signals = {}
        self.features = None
        self.fnames = fnames 
        self.scaler = None
        self.minDuration = minDuration 
        self.linkAppearance = []
        self.minSample = minSample
        self.minDate = minDate
        self.maxDate = None


    def readRawData(self):
        """Grab raw data from ihr and put it in a pandas data frame."""

        logging.debug("Read raw IHR data...")
        dataset = []
        for fi in self.fnames:
            # dataset.append(pd.read_csv( fi, header=None, 
                # names=["timebin", "ip0", "ip1", "diffmedian", "deviation", "nbprobes"]))
            dataset.append(pd.read_csv(fi, 
                usecols=["timebin", "link", "diffmedian", "nbprobes"],
                dtype={"link":str, "diffmedian":float,  "nbprobes":int}))
        
        df = pd.concat(dataset)
        df.index = pd.DatetimeIndex(df.timebin)
        self.maxDate = df.index[-1]
        del df["timebin"]

        self.data = df

    # def linkData(self, link):
        # return self.data[self.data["link"] == link]

    def cleanData(self):
        """Filter out links to be ignored in the analysis."""

        logging.debug("Clean IHR data...")

        self.data = self.data[self.data.index >= self.minDate]
        self.data = self.data[(self.data["diffmedian"]<1000) & (self.data["diffmedian"]>-1000)]
        # self.data["bin"] = [str(d.year)+str(d.month) for d in self.data.index]
        self.data["bin"] = self.data["link"]+"_"+self.data.index.year.astype(str)+self.data.index.month.astype(str)
        # self.data = self.data[self.data["nbprobes"]>9]

        # Group data monthly and filter out months with insufficient number of samples
        logging.debug("Group data per bin...")
        grouped = self.data.groupby("bin")
        logging.debug("Clean IHR data... (bin)")
        for bin, bindata in grouped:
            if len(np.unique(bindata.index))>self.minSample:
                signal = bindata.resample("H").mean().fillna(0)
                self.signals[bin] = signal["diffmedian"]


    def loadData(self):
        """Load raw data and prepare it for analysis.

        return data, label"""

        self.readRawData()
        self.cleanData()

