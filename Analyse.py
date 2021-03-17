import numpy as np

class Analyse:
    """
    Contains all methods needed to analyse a given array containing timestamps and values.
    Needs to be initialized new for _every_ array.
    """

    def __init__(self, rawData):

        self.threshold = 200
        self.rawData = rawData
        self.cleanData = self.cleanUp()

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

