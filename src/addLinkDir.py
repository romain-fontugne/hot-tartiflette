import sys
import cPickle as pickle
import logging
import json
import bz2
from collections import defaultdict
from subprocess import Popen, PIPE

trfnames = ["bzcat","data/traceroute-v4-udm-2018-02-03.txt.bz2", "data/traceroute-v4-builtin-2018-02-03.txt.bz2"]
ihrname = "data/diffRTT_ref_20180410.pickle"

p1 = Popen(trfnames, stdout=PIPE, bufsize=-1)

logging.warn("Loading IHR reference")
ref = pickle.load(open(ihrname))

# for fname in trfnames:
logging.warn("Reading files" )

# with bz2.BZ2File(fname,"rU") as fi:
    # l = fi.readline()
    # while l:

for line in p1.stdout: 
    traceroute = json.loads(line)
    result = traceroute["result"]
    prevIps = None
    for hop in result:
        ips = set()
        # get all IPs that responded at this hop
        if "result" not in hop:
            continue

        for hopRes in hop["result"]:
            if "from" in hopRes:
                ips.add(hopRes["from"])
        
        # enumerate all possible links
        if prevIps is not None:
            for ip0 in prevIps:
                for ip1 in ips:
                    linkRef = None
                    if (ip1, ip0) in ref:
                        linkRef = ref[(ip1, ip0)]
                    elif (ip0, ip1) in ref:
                        linkRef = ref[(ip0, ip1)]

                    if linkRef is not None:
                        if "dir" not in linkRef:
                            linkRef["dir"] = {"far": defaultdict(int), "near":defaultdict(int)}

                        linkRef["dir"]["far"][ip1]+=1
                        linkRef["dir"]["near"][ip1]+=1

        prevIps = ips


logging.warn("Writing new reference file")
pname = ihrname.rpartition(".")[2]+"_dir.pickle"
pickle.dump(ref, open(pname, "w"))
