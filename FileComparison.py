### CC Maik Porrmann ###



import numpy as np
from matplotlib import pyplot as plt
from Analyse import Analyse
from Reference import createReference


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

    def getMeanTimeStep(self):
        timeArray1 = self.analyse1.cleanData[:,0]
        timeArray2 = self.analyse2.cleanData[:, 0]
        minLen = min(timeArray1.shape[0], timeArray2.shape[0])
        timesteps1 = (timeArray1[1:minLen]-timeArray1[:minLen-1])
        timesteps2 = (timeArray2[1:minLen]-timeArray2[:minLen-1])
        meanTimeStep = np.mean(np.abs(timesteps1))
        timestepDiffSum = meanTimeStep -np.mean(np.abs(timesteps2))
        assert timestepDiffSum < 0.05, f"Timesteps differ! Mean of Difference: {timestepDiffSum}"
        return meanTimeStep

    def getMergedArrays(self):
        # start time
        starttime1 = self.analyse1.cleanData[0, 0]
        starttime2 = self.analyse2.cleanData[0, 0]

        #time to peak
        timeToPeak1 = self.analyse1.peak[1]
        timeToPeak2 = self.analyse2.peak[1] 

        #time from peak
        timeFromPeak1 = self.analyse1.cleanData[-1, 0]-timeToPeak1
        timeFromPeak2 = self.analyse2.cleanData[-1, 0] - timeToPeak2

        # merged Times
        mergedTimeToPeak = min(timeToPeak1-starttime1, timeToPeak2-starttime2)
        mergedTimeFromPeak = min(timeFromPeak1,timeFromPeak2)
        # boolean indices 
        ind1 = np.logical_and(self.analyse1.cleanData[:, 0] >= timeToPeak1-mergedTimeToPeak,
                              self.analyse1.cleanData[:, 0] <= timeToPeak1 + mergedTimeFromPeak)
        ind2 = np.logical_and(self.analyse2.cleanData[:, 0] >= timeToPeak2-mergedTimeToPeak,
                              self.analyse2.cleanData[:, 0] <= timeToPeak2 + mergedTimeFromPeak)

        timestep = self.getMeanTimeStep()
        #In some situations one array has 1 more timestep in the desired interval than the other.
        if not np.sum(ind1)== np.sum(ind2):
            if np.sum(ind1) > np.sum(ind2):
                ind1[np.arange(0,ind1.shape[0])[ind1][-1]] = False
            else:
                ind2[np.arange(0, ind2.shape[0])[ind2][-1]] = False
        mergedArray = np.zeros((3, np.sum(ind1)))
        mergedArray[0,:] = np.arange(0,mergedArray.shape[1])*timestep
        mergedArray[2, :np.sum(ind2)] = self.analyse2.cleanData[ind2, 1]

        mergedArray[1, :np.sum(ind1)] = self.analyse1.cleanData[ind1, 1]
        return mergedArray
def main(loaddata, peakHight, plateauHight, plateauLength):
    ref = createReference(peakHight, plateauHight, plateauLength)
    testdata = np.loadtxt(loaddata)
    
    filecomp = FileComparison(ref,testdata)
    mergedArray = filecomp.getMergedArrays()
    
    
    
    plt.plot(mergedArray[0],mergedArray[1], 'b-', label = "Reference")
    plt.plot(mergedArray[0], mergedArray[2], 'r-', label="Datafile")
    plt.figtext(0.15, 0.55 ,f"Absolute Werte: \nPlateau: {filecomp.analyse2.plateau[2]}N \nSpannungsabfall: {filecomp.analyse2.dentDepth}N \nMaximalkraft: {filecomp.analyse2.peak[2]}N \nZeit: {filecomp.analyse2.time}ms", bbox={"facecolor":"orange", "alpha":0.5, "pad":5})
    plt.figtext(0.15, 0.35 ,f"Differenz zur Referenz: \nPlateau:{round(filecomp.difPlateau,2)}N \nMaximalkraft: {round(filecomp.difPeak,2)}N \nZeit: {round(filecomp.difTime,2)}ms", bbox={"facecolor":"orange", "alpha":0.5, "pad":5})
    plt.legend()
    plt.xlabel('Zeit[ms]')
    plt.ylabel('Kraft[N]')
    fig = plt.get_current_fig_manager()
    fig.window.wm_iconbitmap('assets/bone.ico')
    plt.gcf().canvas.set_window_title('Analyse') 

    
    plt.show()

if __name__ == "__main__":
    main('ausgabe/20210529_151717.tom0', 360, 80, 1600)

    
