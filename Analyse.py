import numpy as np
from matplotlib import pyplot as plt

class Analyse:
    """
    Contains all methods needed to analyse a given array containing timestamps and values.
    Needs to be initialized new for _every_ array.
    Tip: Don't use the methods from outside. All relevant points are calculated in __init__
    Only ask for already calculated results (ie analyse.peak, analyse.dent etc.)
    """

    def __init__(self, rawData):

        self.peakIsNegativ = True                         #Falls ihr die Daten irgendwann umdreht, sodass der Peak nicht nach unten ausschlägt: Setzt das hier auf False
        self.sliceCount = 0                               #Hier wird mitgezählt wie oft ich den Datensatz zugeschnitten habe, damit ich in keiner Reckrsivendlosschleife ende
        self.threshold = 200                              #So hoch müssen die Werte mindestsns sein, damit sie relevant sind (kann natürlich bei Bedarf angepasst werden)
        self.varLenght = 20                               #Auf diese Länge wird jeweils die Varianz berechnet. Mein Tipp: Falls das Plateau für eine Mindestdauer gehalten werden muss, würde ich hier ca die Hälfte dieser Zeit eintragen.
        #self.varThresh = 0.3                             #Die tolerierte Varianz berechne ich inzwischen relativ zum Datensatz, aber hier könnte man einen festen Wert einsetzen, wenn man will.
        self.rawData = rawData                            #Das ist das Array, das in den Konstruktor übergeben werden muss. Ich hab das an den bestehenden Datensätzen orientiert.
        self.rawDataBackUp = rawData.copy()               #Das brauche ich für den fall, dass ich die rawData zuschneiden muss, aber danach den orginalIndex wiederfinden will.
        self.cleanData = self.cleanUp()                   #Die Daten werden validiert, gespiegelt, nach oben geschoben und getrimmt.
        self.peak = self.findPeak(self.cleanData)         #Der Peak wird berechnet und als Tupel von Index, Timestamp und Wert angegeben. Der Kraftwert wird allerdings als meine geeichte Version zurückgegeben. Paar Zeilen weiter unten sind die Werte korrigiert.
        self.plateau = self.findPlateau(self.cleanData)   #Der Anfangspunkt des Plateaus wird ebenfalls als Tupel angegeben (index, timestamp, force). Für den Kraftwert gilt das gleich wie für den Peak.
        self.dent = self.findDent(self.cleanData)         #Das hier ist die Delle zwischen Plateau und Peak
        self.slope = self.calculateSlope()                #Das hier ist die Steigung zwischen Delle und Peak
        self.dentDepth = self.calculateDentDepth()

        #Hier nochmal die Koordinaten von Peaks, Plateaus und Dent mit ihren orginal Index- und Forcewerten:
        #Zurückgegebn werden Tripel jeweils mit dem folgenden Aufbau: (Index, Timestamp, Force)
        oldIndexPeak = self.findOldIndex(self.peak[1])
        self.peakCorrect = (oldIndexPeak, self.rawDataBackUp[oldIndexPeak, 0], self.rawDataBackUp[oldIndexPeak, 1])

        oldIndexPlateau = self.findOldIndex(self.plateau[1])
        self.plateauCorrect = (oldIndexPlateau, self.rawDataBackUp[oldIndexPlateau, 0], self.rawDataBackUp[oldIndexPlateau, 1])

        oldIndexDent = self.findOldIndex(self.dent[1])
        self.dentCorrect = (oldIndexDent, self.rawDataBackUp[oldIndexDent, 0], self.rawDataBackUp[oldIndexDent, 1])

        print(f"Arbeits-Plateau: {self.plateau}")
        print(f"Arbeits-Dent: {self.dent}")
        print(f"Arbeits-Peak: {self.peak}")

        print(f"Orginal-Plateau: {self.plateauCorrect}")
        print(f"Orginal-Peak: {self.peakCorrect}")


    def calculateDentDepth(self):
        """
        return: Difference between plateau hight and dent hight.
        """
        return self.plateau[2] - self.dent[2]

    def calculateSlope(self):
        """
        Calculates Slope between dent and Peak
        return: slope
        """

        deltaX = self.peak[1] - self.dent[1]
        delteY = self.peak[2] - self.dent[2]
        slope = delteY / deltaX

        return slope
    
    def findDent(self, cleanData):
        """
        Finds lowest point between plateau and peak -> Dent
        return: (index, timestamp, force value)
        """

        dentInd = np.argmin(cleanData[self.plateau[0]:self.peak[0],1])
        dentInd = dentInd + self.plateau[0]
        dentTime = cleanData[dentInd,0]
        dentValue = cleanData[dentInd,1]

        return (dentInd, dentTime, dentValue)
    
    def findPlateau(self, cleanData):
        """
        Finds last plateau befor peak.
        param: clean Data
        return: Coordinates of plateau (index, timestamp, force value)
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

        return (plateauInd, plateauTime, plateauValue)
    
    def findPeak(self, cleanData):
        """
        Finds highest peak
        param: clean data
        return: Tuple (index, time, value)
        """
        peakInd = np.argmax(cleanData[:,1])
        peakTime = cleanData[peakInd, 0]
        peakValue = cleanData[peakInd, 1]

        return (peakInd, peakTime, peakValue)

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
    ax1 = fig.add_subplot(131)
    ax1.set_title("Arbeitsdaten")
    ax2 = fig.add_subplot(133)
    ax2.set_title("Varianzverlauf")
    ax3 = fig.add_subplot(132)
    ax3.set_title("Orginaldaten")

    ax1.plot(analyse.cleanData[:,0], analyse.cleanData[:,1])
    ax1.plot(analyse.peak[1], analyse.peak[2], "rx")
    ax1.plot(analyse.dent[1], analyse.dent[2], "rx")
    ax1.plot([analyse.plateau[1], analyse.plateau[1]+analyse.varLenght], [analyse.plateau[2]]*2, "r-")
    ax1.plot([analyse.dent[1]]*2, [analyse.dent[2], analyse.plateau[2]], "r-")

    textX1 = analyse.cleanData[0,0]
    textY1 = analyse.plateau[2] + ((analyse.peak[2] - analyse.plateau[2]) /2)
    ax1.text(textX1, textY1, f"Plateau: {analyse.plateau[2]} \nDelle: {analyse.dent[2]} \nSpannungsabfall: {analyse.dentDepth} \nSpitze: {analyse.peak[2]} \nSteigung: {analyse.slope}")

    ax2.plot(analyse.varArrayunreduziert[:,0], analyse.varArrayunreduziert[:,1], "r")

    ax3.plot(analyse.rawDataBackUp[:,0], analyse.rawDataBackUp[:,1])
    ax3.plot(analyse.peakCorrect[1], analyse.peakCorrect[2], "rx")
    ax3.plot(analyse.dentCorrect[1], analyse.dentCorrect[2], "rx")
    ax3.plot([analyse.plateauCorrect[1], analyse.plateauCorrect[1]+analyse.varLenght], [analyse.plateauCorrect[2]]*2, "r-")
    ax3.plot([analyse.dentCorrect[1]]*2, [analyse.dentCorrect[2], analyse.plateauCorrect[2]], "r-")

    textX2 = np.min(analyse.rawDataBackUp[:,0])
    textY2 = analyse.plateauCorrect[2] + ((analyse.peakCorrect[2] - analyse.plateauCorrect[2]) /2)
    ax3.text(textX2, textY2, f"Plateau: {analyse.plateauCorrect[2]} \nDelle: {analyse.dentCorrect[2]} \nSpannungsabfall: {analyse.dentDepth} \nSpitze: {analyse.peakCorrect[2]} \nSteigung: {analyse.slope}")

    plt.show()

    

