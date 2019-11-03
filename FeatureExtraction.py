import csv
import numpy as np
import pandas as pd
from statistics import mean
import matplotlib.pyplot as plt
from IPython.core.pylabtools import figsize
from scipy.signal import find_peaks

#import the Dataset (Time Series)
data = pd.read_csv('FHRDataCol.csv', header=None)
#Initialisation of lists which is used in the Programs
baselineOne=[]
baselineTwo=[]
baselineThree=[]
# Lists used inside the for loop
ListBaseOne = []
ListBaseTwo = []
ListBaseThree = []

# Baseline FHR, Loop used to Calculate the Mean and
#the Rolling Mean for 552 Observations(Columns)
for iterate in range(0,552):
  start = 0 # Start set to 0
  stop = 8000 # Set till the length of the TimeSeries Dataset
  FHRSeries = pd.Series(data[iterate])
  FHRRolMean = FHRSeries[start:stop]

  wn = 70 # Moving window is set to 70 to smoothen the peaks
  # Calculating the rolling mean to remove the peaks
  #which is used to calculate the Baseline FHR
  rolmean = FHRRolMean.rolling(window=wn).mean()
  #For first 10 Minute Window
  ListBaseOne = rolmean[70:2470]
  #For Second 10 Minute Window
  ListBaseTwo = rolmean[2471:4870]
  #For Third 10 Minute Window
  ListBaseThree = rolmean[4871:7270]
  #Mean Value of each Baseline is stored in the Lists ->
  #baselineOne,baselineTwo,baselineThree
  baselineOne.append(mean(ListBaseOne))
  baselineTwo.append(mean(ListBaseTwo))
  baselineThree.append(mean(ListBaseThree))

# Data Visualisations -> Mean, Rolling Mean, Baseline 1, Baseline2, Baseline3
for iterate in range(0,8):
  FHRSeries = pd.Series(data[iterate])
  FHRRolMean = FHRSeries[start:stop-730]
  rolmean = FHRRolMean.rolling(window=wn).mean()
  orig = plt.plot(FHRRolMean, color='mediumspringgreen',label='Original')
  mean = plt.plot(rolmean, color='salmon',label='Rolling Mean')
  plt.hlines(y=baselineOne[iterate],xmin=1, xmax=2400, color='b', linestyle='-',label='Baseline for first 10 minutes window')
  plt.hlines(y=baselineTwo[iterate],xmin=2401, xmax=4800, color='m', linestyle='-.',label='Baseline for second 10 minutes window')
  plt.hlines(y=baselineThree[iterate],xmin=4801, xmax=7200, color='k', linestyle='--',label='Baseline for third 10 minutes window')
  plt.grid(True)
  plt.legend(loc='best')
  print('Baseline for the Time Series', iterate+1)
  plt.show()

# Calculating the Variabalility
delta12 = []
delta23 = []
for i in range(0,552):
  delta12.append(abs(baselineTwo[i]-baselineOne[i]))
  delta23.append(abs(baselineThree[i]-baselineTwo[i]))
 # calculated variability is to set to a CSV File.
with open('variability.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',')
    filewriter.writerow(["BaseLine 1", "BaseLine 2",
    "BaseLine 3","Variability(Delta(B1B2))",
    "Variteratebility(Delta(B2B3))"])
    for i in range(len(baselineOne)):
        row = []
        row.append(baselineOne[i])
        row.append(baselineTwo[i])
        row.append(baselineThree[i])
        row.append(delta12[i])
        row.append(delta23[i])
        filewriter.writerow(row)

# Finding the Accelerations with reference to the Baseline
for i in range(0,8):
    list1 = []
    list2 = []
    list3 = []
    resultList = []
    # Distance 60 -> 4 observations in the Dataset gives 1 Second,
    #Therefore 15 Seconds = 15*4 = 60 Observations
    for j in range(0,3):
        if(j == 0):
            peaks, _ = find_peaks(x=data[i][1:2400],
            height= baselineOne[i] + 15, distance=60)
            list1 = peaks
        if(j == 1):
            peaks, _ = find_peaks(x=data[i][1:4800],
            height= baselineTwo[i] + 15, distance=60)
            list2 = peaks
        if(j == 2):
            peaks, _ = find_peaks(x=data[i][1:7200],
            height= baselineThree[i] + 15, distance=60)
            list3 = peaks
    for k in list1:
        resultList.append(int(k))
    for r in list2:
        if(int(r)>2400):
            resultList.append(int(r))
    for h in list3:
        if(int(h)>4800):
            resultList.append(int(h))
    plt.plot(data[i])
    plt.plot(resultList, data[i][resultList], "x")
    plt.show()
