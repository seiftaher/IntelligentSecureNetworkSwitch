import pandas as pd
import numpy as np




def BuildFinalDataSet(dict,finalDataSet):
  for key in dict:

    outPackets = dict[key]['out'].sum()
    inPackets = dict[key]['in'].sum()

    try:
      packetRatio = inPackets / outPackets
    except:
      packetRatio = float('NaN')

    sumLengthOut = dict[key]['packet length'].where(dict[key]['out'] == 1).sum()
    sumLengthIn = dict[key]['packet length'].where(dict[key]['in'] == 1).sum()
    maxLengthOut = dict[key]['packet length'].where(dict[key]['out'] == 1).max()
    maxLengthIn = dict[key]['packet length'].where(dict[key]['in'] == 1).max()
    meanLengthOut = dict[key]['packet length'].where(dict[key]['out'] == 1).mean()
    meanLengthIn = dict[key]['packet length'].where(dict[key]['in'] == 1).mean()
    stdLengthOut = dict[key]['packet length'].where(dict[key]['out'] == 1).std()
    stdLengthIn = dict[key]['packet length'].where(dict[key]['in'] == 1).std()
    
    try:
      byteRatio = sumLengthIn / sumLengthOut
    except:
      byteRatio = float('NaN')

    sumInterArrivalOut = dict[key]['Delta time'].where(dict[key]['out'] == 1).sum()
    sumInterArrivalIn = dict[key]['Delta time'].where(dict[key]['in'] == 1).sum()
    minInterArrivalOut = dict[key]['Delta time'].where(dict[key]['out'] == 1).min()
    minInterArrivalIn = dict[key]['Delta time'].where(dict[key]['in'] == 1).min()
    meanInterArrivalOut = dict[key]['Delta time'].where(dict[key]['out'] == 1).mean()
    meanInterArrivalIn = dict[key]['Delta time'].where(dict[key]['in'] == 1).mean()
    stdInterArrivalOut = dict[key]['Delta time'].where(dict[key]['out'] == 1).std()
    stdInterArrivalIn = dict[key]['Delta time'].where(dict[key]['in'] == 1).std()

    minTTLOut = dict[key]['Time to Live'].where(dict[key]['out'] == 1).min()
    minTTLIn = dict[key]['Time to Live'].where(dict[key]['in'] == 1).min()
    TTLPercent = minTTLIn/minTTLOut

    diffDataFrame = abs(dict[key]['Delta time'].diff())
    periodicity = diffDataFrame.mean()

    stdPeriodicity= diffDataFrame.std()
    
    counterOut = 0
    counterEndOut = 0
    counterIn = 0
    counterEndIn = 0
    burstOut = []
    burstIn = []
    flagIn = 0
    flagOut = 0
    for _, row in dict[key].iterrows():  
        if row['out'] == 1:
            counterOut += 1
            counterEndOut = 0
            flagOut = 1
        elif row['out'] == 0:
            counterEndOut += 1
            if counterEndOut == 2:
              if counterOut > 2:
                  burstOut.append(counterOut)
                  flagOut = 0
                  counterOut = 0
                  counterEndOut = 0
            
        if row['in'] == 1:
            counterIn += 1
            counterEndIn = 0
            flagIn = 1
        elif row['in'] == 0:
            counterEndIn += 1
            if counterEndIn == 2:
                if counterIn > 2:
                    burstIn.append(counterIn)
                    flagIn = 0
                    counterIn = 0
                    counterEndIn = 0

    if flagOut == 1:
      burstOut.append(counterOut)
    if flagIn == 1:
       burstIn.append(counterIn)

    minBurstOut = float("NaN")
    maxBurstOut = float("NaN")
    meanBurstOut = float("NaN")

    minBurstIn = float("NaN")
    maxBurstIn = float("NaN")
    meanBurstIn = float("NaN")

    if len(burstOut) != 0:
      minBurstOut = float(np.amin(burstOut, axis=0))
      maxBurstOut = float(np.amax(burstOut, axis=0))
      meanBurstOut = float(np.mean(burstOut))
    if len(burstIn) != 0:
      minBurstIn = float(np.amin(burstIn, axis=0))
      maxBurstIn = float(np.amax(burstIn, axis=0))
      meanBurstIn = float(np.mean(burstIn))
      
    
    x = np.array([ outPackets, sumLengthOut, maxLengthOut, meanLengthOut, stdLengthOut, sumInterArrivalOut,
                        minInterArrivalOut, meanInterArrivalOut, stdInterArrivalOut,
                        maxBurstOut, minBurstOut, meanBurstOut,
                        inPackets, sumLengthIn, maxLengthIn,
                        meanLengthIn, stdLengthIn, sumInterArrivalIn,
                        minInterArrivalIn, meanInterArrivalIn, stdInterArrivalIn,
                        maxBurstIn, minBurstIn, meanBurstIn,
                        packetRatio, byteRatio, periodicity, stdPeriodicity, TTLPercent])
    finalDataSet[key] = x

def dataTransformation(packets):
  finalDataSet = {}
  length = len(packets)
  dict = {}
  for x in range(0,length):  
    compareTuple = (packets[x][0],packets[x][1],packets[x][2],packets[x][3],packets[x][4])
    compareTupleR = (packets[x][1],packets[x][0],packets[x][3],packets[x][2],packets[x][4])
    if compareTuple in dict:
      packets[x].extend([1,0])
      dict[compareTuple].append(packets[x])
    elif compareTupleR in dict:
      packets[x].extend([0,1])
      dict[compareTupleR].append(packets[x])

    else: 
      packets[x].extend([1,0])
      dict.update({compareTuple : [packets[x]]})

  for key1 in dict:
    dict[key1] = pd.DataFrame(dict[key1], columns=["Source address", "Destination address", "Source port", "Destination port",
            "Protocol", "packet length",  "Time to Live", "time", "out", "in"])
    diffDataFrame = abs(dict[key1]['time'].diff()).tolist()
    dict[key1]['Delta time'] = diffDataFrame

  BuildFinalDataSet(dict,finalDataSet)
    
  return finalDataSet

