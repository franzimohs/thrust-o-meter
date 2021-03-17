import numpy as np
from matplotlib import pyplot as plt

class Analyse:
    """
    Contains all methods needed to analyse a given array containing timestamps and values.
    Needs to be initialized new for _every_ array.
    """

    def __init__(self, rawData):

        self.peakIsNegativ = True                         #Falls ihr die Daten irgendwann umdreht, sodass der Peak nicht nach unten ausschlägt: Setzt das hier auf False
        self.sliceCount = 0                               #Hier wird mitgezählt wie oft ich den Datensatz zugeschnitten habe, damit ich in keiner Reckrsivendlosschleife ende
        self.threshold = 200                              #So hoch müssen die Werte mindestsns sein, damit sie relevant sind (kann natürlich bei Bedarf angepasst werden)
        self.varLenght = 20                               #Auf diese Länge wird jeweils die Varianz berechnet. Mein Tipp: Falls das Plateau für eine Mindestdauer gehalten werden muss, würde ich hier ca die Hälfte dieser Zeit eintragen.
        #self.varThresh = 0.3                             #Die tolerierte Varianz berechne ich inzwischen relativ zum Datensatz, aber hier könnte man einen festen Wert einsetzen, wenn man will.
        self.rawData = rawData                            #Das ist das Array, das in den Konstruktor übergeben werden muss. Ich hab das an den bestehenden Datensätzen orientiert.
        self.rawDataBackUp = rawData                      #Das brauche ich für den fall, dass ich die rawData zuschneiden muss, aber danach den orginalIndex wiederfinden will.
        self.cleanData = self.cleanUp()                   #Die Daten werden validiert, gespiegelt, nach oben geschoben und getrimmt.
        self.peak = self.findPeak(self.cleanData)         #Der Peak wird berechnet und als Tupel von Timestamp und Wert angegeben. Der Kraftwert wird allerdings als meine geeichte Version zurückgegeben. Paar Zeilen weiter unten sind die Werte korrigiert.
        self.plateau = self.findPlateau(self.cleanData)   #Der Anfangspunkt des Plateaus wird ebenfalls als Tupel angegeben (timestamp, force). Für den Kraftwert gilt das gleich wie für den Peak.

        #Hier nochmal die Koordinaten des Peaks und des Plateaus mit ihren orginal Forcewerten:
        #Zurückgegebn werden Tripel jeweils mit dem folgenden Aufbau: (Index, Timestamp, Force)
        oldIndexPeak = self.findOldIndex(self.peak[0])
        self.peakCorrect = (oldIndexPeak, self.rawDataBackUp[oldIndexPeak, 0], self.rawDataBackUp[oldIndexPeak, 1])

        oldIndexPlateau = self.findNewIndex(self.plateau[0])
        self.plateauCorrect = (oldIndexPlateau, self.rawDataBackUp[oldIndexPlateau, 0], self.rawDataBackUp[oldIndexPlateau, 1])

        print(f"geschobener Peak: {self.peak}")
        print(f"zurückgeschobener Peak: {self.peakCorrect}")

        print(f"geschobenes Plateau: {self.plateau}")
        print(f"zurückgeschobenes Plateau: {self.plateauCorrect}")

    def findPlateau(self, cleanData):
        """
        Finds last plateau befor peak.
        param: clean Data
        return: Coordinates of plateau (timestamp, value)
        """

        peakInd = np.argmax(cleanData[:,1])
        varArr = np.zeros((peakInd, 2))
        varArr[:,0] = cleanData[:peakInd,0]

        for i in range(peakInd):
            varArr[i,1] = np.var(cleanData[i:i+self.varLenght,1])
        
        self.varArrayunreduziert = varArr

        minVar = np.min(varArr[:,1])
        varThresh = minVar * 2.5
      
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
        indexArr = np.where(self.rawDataBackUp[:,0] == timestamp)[0]

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
        if not self.checkTime():
            raise ValueError("data corrupted (Analyse.cleanUp())")

        cleanData = self.invertValues(self.rawData)
        cleanData = self.trim(cleanData)

        return cleanData

    def checkTime(self):
        """
        Validates data. Timestamps need to be regular to ensure reliable data.
        Reference value (ie 0.3) may need to be evaluated and adjusted, when more datasets are available.
        param: dataarray 
        return True If timestamps show low variance
               False If data contains holes or other irregularities
        """
        var = np.var(self.rawData[1:,0] - self.rawData[:-1,0])

        if var > 0.3:
            print("data corrupted. I will try again with ends cut off (Analyse.checkTime())")
            if self.sliceCount >= 5:
                self.sliceCount = 0
                return False
            
            self.rawData = self.rawData[10:-10,:]
            self.sliceCount += 1
            return self.checkTime()
        
        return True
    
    def invertValues(self, rawData):
        """
        Inverts all values so that plateau and peak are the highest positiv values,
        if necessary. Also lowest point is now 0.
        """
        
        positivData = rawData

        if self.peakIsNegativ:
            positivData[:,1] = rawData[:,1] * -1
            
        
        positivData[:,1] = positivData[:,1] - np.min(positivData[:,1])

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
    ax1 = fig.add_subplot(121)
    ax1.set_title("Werte, Peak, Plateau")
    ax2 = fig.add_subplot(122)
    ax2.set_title("Varianzverlauf")
    ax1.plot(analyse.cleanData[:,0], analyse.cleanData[:,1])
    ax2.plot(analyse.varArrayunreduziert[:,0], analyse.varArrayunreduziert[:,1], "r")
    ax1.plot(*analyse.peak, "x")
    ax1.plot([analyse.plateau[0], analyse.plateau[0]+analyse.varLenght], [analyse.plateau[1]]*2, "r-")
    plt.show()

    

