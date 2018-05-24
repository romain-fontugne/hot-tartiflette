import cPickle as pickle

class MapitData(object):
    """Retrive and format MAP-IT data. """

    def __init__(self, fnames= "data/mapit_atlas_builtin_udm_2018-02-1to3.txt",
            ihrRef="data/diffRTT_ref_20180410_dir.pickle"):
        """Initialize attributes. """

        self.fnames = fnames
        self.mapping = {}
        self.ref = pickle.load(open(ihrRef))

    def readRawData(self):

        with open(self.fnames) as fp:
            for line in fp:
                # 1.1.1.57,False,1.1.1.58,0,3786,-Reserved AS-,@family-26059,True,False,False
                # Read MAP-IT output. Here is an example:
                # 50.242.151.69,False,50.242.151.70,7922,2914,CCCS-ARIN,NTTAM-1-ARIN,False,False,False
                # 50.242.151.70,True,50.242.151.69,7922,2914,CCCS-ARIN,NTTAM-1-ARIN,True,False,False

                # The boolean at the second column (called direction) tells us which AS is 
                # managing the reported IP (that's the first column).
                # So if the direction is set to False, then the IP maps to the first ASN (column 
                # 4). If it is set to True then it corresponds to the second ASN (column 5).
                # In the example, 50.242.151.69 is for comcast and 50.242.151.70 is for ntt.
                ip0, direction, ip1, asa, asb, _, _, _, _, _ = line.split(",")

                if direction == "False":
                    # if ip0 in self.mapping and asa != self.mapping[ip0]:
                        # print("contradictory mappings! %s: %s and %s" % (ip0, asa, self.mapping[ip0])
                    # if ip1 in self.mapping and asb != self.mapping[ip1]:
                        # print("contradictory mappings! %s: %s and %s" % (ip1, asb, self.mapping[ip0])
                    self.mapping[ip0] = (asa, asb)
                    self.mapping[ip1] = (asb, asa)

                else: 
                    # if ip1 in self.mapping and asa != self.mapping[ip1]:
                        # print("contradictory mappings! %s: %s and %s" % (ip1, asa, self.mapping[ip0])
                    # if ip1 in self.mapping and asb != self.mapping[ip0]:
                        # print("contradictory mappings! %s: %s and %s" % (ip0, asb, self.mapping[ip0])
                    self.mapping[ip1] = (asa, asb)
                    self.mapping[ip0] = (asb, asa)


    def loadData(self):
        self.readRawData()


    def isInterdomain(self, link):
        # check the link direction in the IHR reference
        if link in self.ref:
            ip = max(self.ref[link]["dir"]["far"], key=self.ref[link]["dir"]["far"].get) 

            if ip in self.mapping: 
                return self.mapping[ip]
            else:
                return None

        # not in the reference we can still check if one of the IP is found by
        # map-it
        else:
            for ip0 in link[1:-1].split(","):
                ip = ip0.strip()
                if ip in self.mapping:
                    return self.mapping[ip]

            return None


