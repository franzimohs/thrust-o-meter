import numpy as np
from matplotlib import pyplot as plt
from Analyse import Analyse

class FileComparison:
    """
    Compares to given files for similarities and differences.
    """

    def __init__(self, rawData1, rawData2):
        """
        Initiate with both data arrays.
        First is reference.
        Second is test subjects input.
        """

        self.analyse1 = Analyse(rawData1)
        self.analyse2 = Analyse(rawData2)

        self.difPeak = self.comparePeaks()
        self.difPlateau = self.comparePlateaus()
        self.difTime = self.compareTime()
    
    def comparePeaks(self):

        peak1 = self.analyse1.peakCorrect[2]
        peak2 = self.analyse2.peakCorrect[2]

        return peak2 - peak1

    def comparePlateaus(self):

        plateau1 = self.analyse1.plateauCorrect[2]
        plateau2 = self.analyse2.plateauCorrect[2]

        return plateau2 - plateau1
    
    def compareTime(self):

        time1 = self.analyse1.time
        time2 = self.analyse2.time

        return time2 - time1