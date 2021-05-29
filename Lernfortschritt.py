#!/usr/bin/python3
from Analyse import Analyse as al
import numpy as np
import os
from matplotlib import pyplot as plt


def fortschritt(endung, peak):
  peak_list = []
  vorspannung_list =[]
  inzisur_list =[]
  time_list =[]
  
  for (x, y, filenames) in os.walk('ausgabe'):
    
    for file in sorted(filenames):
      name = file.split('.')
      if name[-1] != endung:
        continue 
        
      rawData = np.loadtxt('ausgabe/'+file)
      
      try:
        analyseData=al(rawData)
      except Exception as e:
        print('Fehler:'+str(e))
        pass
      peak_list.append([name[0], (analyseData.peak[2]-peak)])
      vorspannung_list.append([name[0], (analyseData.plateau[2]-(peak/4))])
      inzisur_list.append([name[0], analyseData.dentDepth])
      time_list.append([name[0], (analyseData.time-150)])
  return peak_list, vorspannung_list, inzisur_list, time_list
  


def plot():
  peak_list, vorspannung_list, inzisur_list, time_list = merge()
  fig = plt.figure(num='Lernfortschritt')
  p1=fig.add_subplot(221)
  p2=fig.add_subplot(222)
  p3=fig.add_subplot(223)
  p4=fig.add_subplot(224)

  p1.plot([item[1] for item in peak_list], label = "Peakverlauf")
  p1.set_title('Peak')   
  p1.set_ylabel('Kraft[N]') 

  p2.plot([item[1] for item in vorspannung_list], label ='Vorspannungsverlauf')
  p2.set_title('Vorspannung')
  p2.set_ylabel('Kraft[N]')

  p3.plot([item[1] for item in inzisur_list], label ='Inzisurverlauf')
  p3.set_title('Inzisurtiefe')
  p3.set_ylabel('Kraft[N]')

  p4.plot([item[1] for item in time_list], label='Zeitverlauf')
  p4.set_title('Impulsdauer')
  p4.set_ylabel('Zeit[ms]')
  fig.set_size_inches((9,6.5))
  
def merge():
  peak_list0=[]
  peak_list1=[]
  peak_list2=[]
  peak_list3=[]
  vorspannung_list0=[]
  vorspannung_list1=[]
  vorspannung_list2=[]
  vorspannung_list3=[]
  inzisur_list0=[]
  inzisur_list1=[]
  inzisur_list2=[]
  inzisur_list3=[]
  time_list0=[]
  time_list1=[]
  time_list2=[]
  time_list3=[]
  try:
    peak_list0, vorspannung_list0, inzisur_list0, time_list0 = fortschritt('tom0', 360)
  except:
      pass
  try:
    peak_list1, vorspannung_list1, inzisur_list1, time_list1 = fortschritt('tom1', 330)
  except:
    pass
  try:
    peak_list2, vorspannung_list2, inzisur_list2, time_list2 = fortschritt('tom2', 300)
  except:
    pass
  try:
    peak_list3, vorspannung_list3, inzisur_list3, time_list3 = fortschritt('tom3', 270)
  except:
    pass
  
  peak_fehler_list =sorted(peak_list0 + peak_list1 + peak_list2 + peak_list3)
  vorspannung_fehler_list = sorted(vorspannung_list0 + vorspannung_list1 + vorspannung_list2 + vorspannung_list3)
  inzisur_fehler_list = sorted(inzisur_list0 + inzisur_list1 + inzisur_list2 + inzisur_list3)
  time_fehler_list = sorted(time_list0 + time_list1 + time_list2 + time_list3)
  return peak_fehler_list, vorspannung_fehler_list, inzisur_fehler_list, time_fehler_list

def main():
  plot()
  plt.show()


if __name__ == '__main__':
  plot()
  plt.show()
  
  
  