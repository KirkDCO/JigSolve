#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from math import *
import matplotlib.pyplot as plt

def EucDist(X, Y):
    # X and Y are lists with coordinates of points in arbitrary dimensions
    return sqrt(sum([ (x-y)**2 for x,y in zip(X,Y) ]))

def sd(data):
    n = len(data)

    if n <= 1:
        return 0.0

    mean, sd = avg(data), 0.0

    # calculate stan. dev.
    for el in data:
        sd += (float(el) - mean)**2
    sd = sqrt(sd / float(n-1))

    return sd

def avg(ls):
    n, mean = len(ls), 0.0

    if n <= 1:
        return ls[0]

    # calculate average
    for el in ls:
        mean = mean + float(el)
    mean = mean / float(n)

    return mean

def GetAlignedWindows(M, N, m_pt, n_pt, window):
    
    # for the given point in each set of points
    # extract the window of interest
    # align the sequence of points
    # calculate and return the distance between aligned windows
    
    # get the window of points for M
    M_pts = [ m_pt + v for v in range(-window,window+1)]
    for i,v in enumerate(M_pts):
        if v < 0:
            M_pts[i] += len(M)
        elif v >= len(M):
            M_pts[i] -= len(M)
    
    M_window = { pt:{'x':M[list(M.keys())[pt]]['x'],
                     'y':M[list(M.keys())[pt]]['y']} for pt in M_pts }

    # find the shift needed to align the given points
    # 2-dimensional for now
    x_shift = M[list(M.keys())[m_pt]]['x'] - N[list(N.keys())[n_pt]]['x']
    y_shift = M[list(M.keys())[m_pt]]['y'] - N[list(N.keys())[n_pt]]['y']
    
    # get window of points for N and apply shift
    N_pts = [ n_pt + v for v in range(-window,window+1)]
    for i,v in enumerate(N_pts):
        if v < 0:
            N_pts[i] += len(N)
        elif v >= len(N):
            N_pts[i] -= len(N)
    
    N_window = { pt:{'x':N[list(N.keys())[pt]]['x'] + x_shift,
                     'y':N[list(N.keys())[pt]]['y'] + y_shift} for pt in N_pts} 

    return M_window, N_window

def AlignScore(M, N, m_pt, n_pt, window):
    
    # get the aligned windows
    M_window, N_window = GetAlignedWindows(M, N, m_pt, n_pt, window)
    
    # compute similarity score 
    # similarity in this case is the sum of Euclidean distances 
    # between matched points
    sum = 0.0
    for M_pt, N_pt in zip(M_window.keys(), N_window.keys()):
        sum += EucDist( [ M_window[M_pt]['x'], M_window[M_pt]['y'] ],
                        [ N_window[N_pt]['x'], N_window[N_pt]['y'] ])
    return sqrt(sum)

def AlignPieces_Euclid(M, N, mode = 'max distance', window=10, 
             cutoff = 100, distr_score = False, avg = 25, sd = 5): 
      
    
    # places to store maximum score and which position
    mx = 0.0
    mx_M = 0
    mx_N = 0
    
    # Create suffix table
    SuffTable = [[0 for k in range(len(N)+1)] for l in range(len(M)+1)] 
      
    # Build suffix table
    cutoff_multiplier = 2 # penalty for extended ranges outsisde cutoff
    for i in range(len(M) + 1): 
        for j in range(len(N) + 1): 
            if (i == 0 or j == 0): 
                SuffTable[i][j] = 0
            else:
                d = AlignScore(M, N, i-1, j-1, window)
                if mode == 'max distance': #return actual distances - used to establish cutoff
                    SuffTable[i][j] = d
                elif mode == 'min distance': #return actual distances - used to establish cutoff
                    SuffTable[i][j] = 1/d
                elif mode == 'NW_align': # Needleman-Wunsch - global alignment
                    if d < cutoff: 
                        SuffTable[i][j] = SuffTable[i-1][j-1] + 1
                    else: #ignore distances above cutoff
                        SuffTable[i][j] = SuffTable[i-1][j-1] - 1
                elif mode == 'SW align': #Smith-Waterman - local alignment
                    if distr_score:
                        qtile = (d-avg)/sd
                        if qtile > 0:
                            SuffTable[i][j] = SuffTable[i-1][j-1] - qtile * cutoff_multiplier
                            cutoff_multiplier *= 2
                        else:
                            SuffTable[i][j] = SuffTable[i-1][j-1] - qtile
                            cutoff_multiplier = 2
                    else:
                        if d < cutoff: # small distance improve our score
                            SuffTable[i][j] = SuffTable[i-1][j-1] + 1
                            cutoff_multiplier = 1
                        else: #large distances degrade our score
                            SuffTable[i][j] = SuffTable[i-1][j-1] - cutoff_multiplier
                            cutoff_multiplier *= 2
                    SuffTable[i][j] = max(0,SuffTable[i][j])

                if SuffTable[i][j] > mx:
                    mx = SuffTable[i][j]
                    mx_M = i
                    mx_N = j
    
    # determine the length of the best scoring window
    length = 1
    for length in range( 1, min(mx_M,mx_N) ):
        if SuffTable[mx_M-length][mx_N-length] == 0:
            break

    return SuffTable, mx, mx_M, mx_N, length-1