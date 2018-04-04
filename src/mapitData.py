
class MapitData(object):
    """Retrive and format MAP-IT data. """

    def __init__(self, fnames= "data/mapit_atlas_builtin_udm_2018-02-1to3.txt" ):
        """Initialize attributes. """

        self.fnames = fnames
        self.mapping = {}

    def readRawData(self):

        with open(self.fnames) as fp:
            for line in fp:
                # 1.1.1.57,False,1.1.1.58,0,3786,-Reserved AS-,@family-26059,True,False,False
                ip0, direction, ip1, asa, asb, _, _, _, _, _ = line.split(",")

                if direction == "False":
                    # if ip0 in self.mapping and asa != self.mapping[ip0]:
                        # print("contradictory mappings! %s: %s and %s" % (ip0, asa, self.mapping[ip0])
                    # if ip1 in self.mapping and asb != self.mapping[ip1]:
                        # print("contradictory mappings! %s: %s and %s" % (ip1, asb, self.mapping[ip0])
                    self.mapping[ip0] = (asa, asa)
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


    def isInterdomain(self, ip):
        if ip in self.mapping: 
            return self.mapping[ip]
        else:
            return None

