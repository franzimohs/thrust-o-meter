####CC Franziska Mohs####


from Analyse import Analyse as al
import numpy as np
import os
from matplotlib import pyplot as plt

def entspeichern():
  with open('Ausgabepfad', 'r') as speicher:
    dirname = str(speicher.readline())
  return dirname
    


def fortschritt(endung, peak, verhältnis):
  peak_list = []
  vorspannung_list =[]
  inzisur_list =[]
  time_list =[]
  dirname = entspeichern()
  
  for (x, y, filenames) in os.walk(dirname): 

    for file in sorted(filenames):
      name = file.split('.')
      if name[-1] != endung:
        continue 
        
      rawData = np.loadtxt(os.path.join(dirname,file))
      
      try:
        analyseData=al(rawData)
      except Exception as e:
        print('Fehler:'+str(e))
        pass
      peak_list.append([name[0], (analyseData.peak[2]-peak)])
      vorspannung_list.append([name[0], (analyseData.plateau[2]-(peak/verhältnis))])
      inzisur_list.append([name[0], analyseData.dentDepth])
      time_list.append([name[0], (analyseData.time-150)])
  return peak_list, vorspannung_list, inzisur_list, time_list
  


def plot():
  peak_list, vorspannung_list, inzisur_list, time_list = merge()
  fig = plt.figure(num='Lernfortschritt')
  fig_manager = plt.get_current_fig_manager()
  fig_manager.window.wm_iconbitmap('assets/bone.ico')
  
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
    peak_list0, vorspannung_list0, inzisur_list0, time_list0 = fortschritt('tom00', 550, 2.5)
  except:
      pass
  try:
    peak_list1, vorspannung_list1, inzisur_list1, time_list1 = fortschritt('tom10', 450, 2.5)
  except:
    pass
  try:
    peak_list2, vorspannung_list2, inzisur_list2, time_list2 = fortschritt('tom20', 350, 2.5)
  except:
    pass
  try:
    peak_list3, vorspannung_list3, inzisur_list3, time_list3 = fortschritt('tom30', 250, 2.5)
  except:
    pass
  try:
    peak_list01, vorspannung_list01, inzisur_list01, time_list01 = fortschritt('tom01', 550, 4)
  except:
      pass
  try:
    peak_list11, vorspannung_list11, inzisur_list11, time_list11 = fortschritt('tom11', 450, 4)
  except:
    pass
  try:
    peak_list21, vorspannung_list21, inzisur_list21, time_list21 = fortschritt('tom21', 350, 4)
  except:
    pass
  try:
    peak_list31, vorspannung_list31, inzisur_list31, time_list31 = fortschritt('tom31', 250, 4)
  except:
    pass
  
  peak_fehler_list =sorted(peak_list0 + peak_list1 + peak_list2 + peak_list3 + peak_list01 + peak_list11 + peak_list31 + peak_list21)
  vorspannung_fehler_list = sorted(vorspannung_list0 + vorspannung_list1 + vorspannung_list2 + vorspannung_list3 + vorspannung_list01 + vorspannung_list11 + vorspannung_list21 + vorspannung_list31)
  inzisur_fehler_list = sorted(inzisur_list0 + inzisur_list1 + inzisur_list2 + inzisur_list3 + inzisur_list01 + inzisur_list11 + inzisur_list21 + inzisur_list31)
  time_fehler_list = sorted(time_list0 + time_list1 + time_list2 + time_list3 + time_list01 + time_list11 + time_list21+ time_list31)
  return peak_fehler_list, vorspannung_fehler_list, inzisur_fehler_list, time_fehler_list

def main():
  plot()
  plt.show()


if __name__ == '__main__':
  plot()
  plt.show()
  
  
  