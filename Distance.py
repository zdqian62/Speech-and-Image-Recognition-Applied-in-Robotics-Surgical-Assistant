import numpy as np
import time

def dtw(s1,s2):
    m = len(s1)
    n = len(s2)
    c = np.zeros((m, n))
    c[0, 0] = abs(s1[0]-s2[0])
    for i in range(1, m):
        c[i, 0] = abs(s1[i]-s2[0])+c[i-1, 0]
    for j in range(1, n):
        c[0, j] = abs(s1[0]-s2[j])+c[0, j-1]
    for i in range(1, m):
        for j in range(1, n):
            c[i, j] = dtw(s1[i], s2[j])+min(c[i-1, j],c[i, j-1],c[i-1, j-1])
    return(c[m-1, n-1])

def Euclidean(s1,s2):
    start = time.time()
    c = 0
    m = min(len(s1),len(s2))
    for i in range(0,m):
        c=abs(s1[i]-s2[i])+c
    end = time.time()
    print(end-start)
    return(c)