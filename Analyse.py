import numpy as np
from matplotlib import pyplot as plt

class Analyse:
    """
    Contains all methods needed to analyse a given array containing timestamps and values.
    Needs to be initialized new for _every_ array.
    """

    def __init__(self, rawData):

        self.threshold = 200
        self.varLenght = 10
        #self.varThresh = 0.3
        self.rawData = rawData
        self.cleanData = self.cleanUp()
        self.peak = self.findPeak(self.cleanData)
        self.plateau = self.findPlateau(self.cleanData)


    def findPlateau(self, cleanData):

        peakInd = np.argmax(cleanData[:,1])
        varArr = np.zeros((peakInd, 2))
        varArr[:,0] = cleanData[:peakInd,0]

        for i in range(peakInd):
            varArr[i,1] = np.var(cleanData[i:i+self.varLenght,1])
        
        self.varArrayunreduziert = varArr

        minVar = np.min(varArr[:,1])
        varThresh = minVar * 1.2
      
        varArr = varArr[varArr[:,1] < varThresh]
        

        #If you want to merge similar points, you would do it here
        #One could also compare hights of the last two plateus to be sure you didn't find the dip at the end

        plateauTime = varArr[-1,0]
        plateauInd = self.findNewIndex(plateauTime)
        plateauValue = cleanData[plateauInd][1]

        return (plateauTime, plateauValue)
    
    def findPeak(self, cleanData):
        """
        Finds highest peak
        param: clean data
        return: Tuple (time, value)
        """
        peakInd = np.argmax(cleanData[:,1])
        peakTime = cleanData[peakInd, 0]
        peakValue = cleanData[peakInd, 1]

        return (peakTime, peakValue)

    def findOldIndex(self, timestamp):
        """
        param: time position i want to find
        return: index of timestamp on _original_ array
        """
        indexArr = np.where(self.rawData[:,0] == timestamp)[0]

        assert indexArr.size == 1, "timestamp not unique Analyse.findOldIndex()"

        return indexArr[0]
    
    def findNewIndex(self, timestamp):
        """
        param: time position i want to find
        return: index of timestamp on _cleand_ array
        """
        indexArr = np.where(self.cleanData[:,0] == timestamp)[0]

        assert indexArr.size == 1, "timestamp not unique Analyse.findNewIndex()"

        return indexArr[0]
    
    def cleanUp(self):
        """
        Cleans up data.
        1. Check for faulty data
        2. Invert values, if necessary. Lowest point at 0.
        3. Remove excess data
        return: Remaining interesting stuff after inverting and trimming.
        """
        if not self.checkTime(self.rawData):
            raise ValueError("data corrupted (Analyse.cleanUp())")

        cleanData = self.invertValues(self.rawData)
        cleanData = self.trim(cleanData)

        return cleanData

    def checkTime(self, rawData):
        """
        Validates data. Timestamps need to be regular to ensure reliable data.
        Reference value (ie 0.3) may need to be evaluated and adjusted, when more datasets are available.
        param: dataarray 
        return True If timestamps show low variance
               False If data contains holes or other irregularities
        """
        var = np.var(rawData[1:,0] - rawData[:-1,0])

        if var > 0.3:
            print("data corrupted (Analyse.checkTime())")
            return False
        
        return True
    
    def invertValues(self, rawData):
        """
        Inverts all values so that plateau and peak are the highest positiv values,
        if necessary. Also lowest point is now 0.
        """
        
        avr = np.mean(rawData[:,1])
        positivData = rawData

        if avr <= 0:
            positivData[:,1] = rawData[:,1] * -1
            
        
        positivData[:,1] = positivData[:,1] + np.min(positivData[:,1])

        return positivData


    def trim(self, positivData):
        """
        Cuts off all excess data (start and end)
        param: data where peak is positiv
        Return: Array only containing rise of plateau to end of peak.
        """

        return positivData[positivData[:,1] > self.threshold,:]
    
if '__main__' == __name__:
    rawData = np.loadtxt("./ref")
    analyse = Analyse(rawData)

    fig = plt.figure()
    ax1 = fig.add_subplot('121')
    ax2 = fig.add_subplot('122')
    ax1.plot(analyse.cleanData[:,0], analyse.cleanData[:,1])
    ax2.plot(analyse.varArrayunreduziert[:,0], analyse.varArrayunreduziert[:,1], "r")
    ax1.plot(*analyse.peak, "x")
    ax1.plot(*analyse.plateau, "+")
    plt.show()

    

