from math import *
import matplotlib.pyplot as plt

def angle(ref, tar):
    
    # calculate the angle between the supplied points/vectors
    # the angle is from ref(erence) to tar(get)
    
    dot = ( ref[0] * tar[0] + ref[1] * tar[1] ) # dot product
    det = ( ref[0] * tar[1] - ref[1] * tar[0] ) # determinant
    
    return atan2(det, dot) * 180/pi

def euc_dist(X, Y):
    # X and Y are lists with coordinates of points in arbitrary dimensions
    return sqrt(sum([ (x-y)**2 for x,y in zip(X,Y) ]))

def std(data):
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

def median(lst):
    sortedLst = sorted(lst)
    lstLen = len(lst)
    index = (lstLen - 1) // 2

    if (lstLen % 2):
        return sortedLst[index]
    else:
        return (sortedLst[index] + sortedLst[index + 1])/2.0
