import sounddevice as sd
import numpy as np
from data_setup import *
from Distance import *

duration=2.5
sd.default.samplerate = 1000

print('Set up the dictionary.')
D=data_setup()
print('Dictionary set up end.')

print('Set up the testset.')
T=data_setup()
print('testset set up end.')

Euc_lable=[]
dtw_lable=[]

for i in range(len(T)):
    name=T[i][0]
    record=T[i][1]
    infinity = float("inf")
    min_Euc=infinity
    min_dtw=infinity
    for j in range(len(D)):
        dtwd=dtw(record,D[j][1])
        Eucd=Euclidean(record,D[j][1])
        if dtwd<min_dtw:
            min_dtw=dtwd
            min_dtw_name=D[j][0]
        if Eucd<min_Euc:
            min_Euc=Eucd
            min_Euc_name=D[j][0]
    Euc_lable.append(min_Euc_name)
    dtw_lable.append(min_dtw_name)

Euc_correct=0
dtw_correct=0

for k in range(len(T)):
    if Euc_lable[k]==T[k][0]:
        Euc_correct=Euc_correct+1
    if dtw_lable[k]==T[k][0]:
        dtw_correct=dtw_correct+1

Euc_acc=Euc_correct/len(T)
dtw_acc=dtw_correct/len(T)

print('The accuracy of Euclidean distance is', Euc_acc)
print('The accuracy of dtw distance is', dtw_acc)
