import sys
import os
import cPickle as pickle
from collections import defaultdict
from scipy import stats
import logging
import glob
import pandas as pd

sys.path.append("../ip2asn/")
import ip2asn

agg = "asn"
# agg = "country"
ihrfname = "data/diffRTT_ref_20180410.pickle"
hotfname = "data/hotLinks.csv"

ia = ip2asn.ip2asn("../ip2asn/db/rib.20180201.pickle")

def asnres(ip):
    #TODO add mapit mapping  
    asn = ia.ip2asn(ip)
    return asn

def loadDelegationFiles(dir="data/irr_delegation"):
    asn2cc = {}
    for fname in glob.glob(dir+"/*_asn"):
        fi = open(fname)
        cc = fname.rpartition("/")[2].partition("_")[0].upper()
        for line in fi.readlines():
            asn2cc[int(line[2:-1])] = cc

    return asn2cc
            
asn2cc = loadDelegationFiles()
def countryres(ip):
    asn = asnres(ip)
    if asn in asn2cc:
        return asn2cc[asn]
    else:
        return "UNK"

if agg == "asn":
    resfct = asnres
else:
    resfct = countryres

if __name__ == "__main__":
    # IHR data
    if not os.path.exists("data/ihr_%s_count.pickle" % agg):
        ihrCount = defaultdict(int)
        logging.warn("Loading IHR reference")
        ref = pickle.load(open(ihrfname))
        for link in ref.iterkeys():
            ihrCount[resfct(link[0])]+=1
            ihrCount[resfct(link[1])]+=1
    
        pickle.dump(ihrCount, open("data/ihr_%s_count.pickle" % agg, "w"))
    else:
        ihrCount = pickle.load( open("data/ihr_%s_count.pickle" % agg, "r"))


    # Hot links data
    if not os.path.exists("data/hotlinks_%s_count.pickle" % agg):
        fi = open("data/hotLinks.csv")
        hotlinksCount = defaultdict(int)

        for line in fi.readlines():
            ip0, ip1, _, _, _ = line.split(",")
            hotlinksCount[resfct(ip0.strip())]+=1
            hotlinksCount[resfct(ip1.strip())]+=1

        pickle.dump(hotlinksCount, open("data/hotlinks_%s_count.pickle" % agg, "w"))
    else:
        hotlinksCount = pickle.load( open("data/hotlinks_%s_count.pickle" % agg, "r"))


    dfihr = pd.DataFrame(data=ihrCount.values(), index=ihrCount.keys(), columns=["count"])
    dfhot = pd.DataFrame(data=hotlinksCount.values(), index=hotlinksCount.keys(), columns=["count"])

    dfall = dfihr.merge(dfhot, how="outer", left_index=True, right_index=True, suffixes=["_ihr", "_hot"])
    dfall = dfall.fillna(0)

    print stats.spearmanr(dfall)
    pickle.dump(dfall, open("data/%s_all_count.pickle" % agg, "w"))
