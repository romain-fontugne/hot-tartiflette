import cPickle as pickle
import bz2

trfnames ["../data/traceroute-v4-udm-2018-02-03.txt.bz2", "data/traceroute-v4-builtin-2018-02-03.txt.bz2"]


for fname in trfnames:
    with bz2.BZ2File(fname) as fi:
        :

