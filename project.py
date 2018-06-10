# Final Project
# Topic: Tempo Analysis 

# CS591 project.py
# Laixian Wan
# wanlx@bu.edu

import audioUtilities as au
import numpy as np
import matplotlib.pyplot as plt
import statistics as stat

# Basic BPM detect function
# Based on hw05.py and lecture notes
# Uncomment all plt instructions for debugging
def detectBPM(Wave):
    '''
    takes a signal and calculate the tempo in BPM.
    '''
    # Step 1
    X = Wave
    rectification = [x * x for x in X]

    # Step 2
    A = []
    window = 0
    W = 1000
    while window < len(X):
        A.append(max(rectification[window:(window + W)]))
        window += W

    time= []
    for i in range(0, len(A)):
        time.append(i/44.1)

    #plt.plot(time, A)
    #plt.xlabel('Second')
    #plt.title('Max amplitude of squared signal, W = 1000')
    #plt.show()

    # Step 3
    difference = [0]
    for i in range(0, len(A) - 1):
        difference.append(A[i + 1] - A[i])

    #plt.plot(time, difference)
    #plt.ylabel('difference')
    #plt.title('Difference function')
    #plt.show()

    # Step 4
    D = []
    for sample in difference:
        if sample > 0:
            D.append(sample)
        else:
            D.append(0)

    #plt.plot(time, D)
    #plt.title('Half-wave rectify')
    #plt.show()

    # Step 5
    S = au.realFFT(D)
    bpm = []
    for i in range(0, len(S)):
        bpm.append(i)
    #plt.plot(bpm, S)
    #plt.xlabel('BPM')
    #plt.title('Beat Spectrum')
    #plt.show()
    
    peak = []
    threhold = 0.3 * max(S)
    for i in range(1, len(S) - 1):
        if (S[i] > threhold and S[i] - S[i - 1] > 0 and S[i] - S[i + 1] > 0) or S[i] == max(S):
            peak.append(i)
    return bpm[peak.pop(0)]

def split(Wave):
    '''
    splits the Wave according to amplitude changes.
    '''
    
    X = [abs(x) for x in Wave]
    Len = len(X)

    difference = [0]
    for i in range(0, Len - 1):
        difference.append(abs(X[i + 1] - X[i]))

    #time= []
    #for i in range(0, Len):
    #  time.append(i/44100)
    #plt.plot(time, difference)
    #plt.show()

    threhold = 0.3 * max(difference)

    mark = [0]
    for i in range(1, len(difference) - 1):
        if difference[i - 1] < threhold and difference[i + 1] > threhold:
            mark.append(i)

    # eliminate unnecessary timing points.
    # c is the constant deciding how to eliminate timing points
    
    #c = 4410 0.1s?
    c = 8820
    
    temp = []
    for i in range(1, len(mark) - 1):
        if mark[i + 1] - mark[i] <= c or mark[i] - mark[i - 1] <= c:
            temp.append(mark[i])
            
    for x in temp:
        a = mark.remove(x)
    
    mark.append(Len - 1)
    return mark

# Main function
def tempoAnalysis(Filename):
    '''
    takes a signal 'Filename' and roughly analyzes it's tempo using the BPM detection function.
    '''
    Wave = au.readWaveFile(Filename)
    Tempo = [] # List which stores BPMs
    
    timingPoint = split(Wave)
    
    for i in range(0, len(timingPoint) - 1):
        Tempo.append(detectBPM(Wave[timingPoint[i]:timingPoint[i + 1]]))

    time = []
    for i in range(0, len(Wave)):
        time.append(i)

    tempo = []

    k = 0
    for i in range(0, len(time)):
        if i >= timingPoint[k] and i < timingPoint[k + 1]:
            k += 0
        elif i == timingPoint[-1]:
            tempo.append(Tempo[k])
            break
        else:
            k += 1
        tempo.append(Tempo[k])

    time = [x/44100 for x in time]

    plt.plot(time, tempo)
    plt.xlabel('Time in seconds')
    plt.ylabel('BPM')
    plt.title('Tempo/Time')
    plt.show()

    
