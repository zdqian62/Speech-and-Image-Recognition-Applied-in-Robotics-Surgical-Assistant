import sounddevice as sd
import numpy as np

def record_adjust(record,threshold):
    record=record[250:len(record),:]  # remove the noise at the start
    ave=np.mean(abs(record))
    noise=(abs(record)<ave)
    top=0
    bottom=len(noise)-1
    for i in range(len(noise)):
        if noise[i]==False:
            temp=noise[i+1:min(len(noise),i+threshold)]
            compare=np.ones(len(temp))
            temp=temp.astype(int)
            if ~(temp==compare).all():
                top=i
                break
    
    for j in range(len(noise)-1,-1,-1):
        if noise[j]==False:
            temp=noise[max(0,j-threshold):j-1]
            compare=np.ones(len(temp))
            temp=temp.astype(int)
            if ~(temp==compare).all():
                bottom=j
                break
                
    record=record[top:bottom,:]
    return(record)           
        
    

def data_setup():
    sd.default.samplerate = 1000 #the minimum samplerate is 1000, lower will cause Invalid sample rate
    sd.default.channels = 1
    duration=2.5  #seconds
    threshold=10
    
    toolName=input('Please input the name of the tools to be recorded next:')
    record= sd.rec(int(duration * 1000))
    record=record_adjust(record,threshold)
    sd.wait(print('Speaking...'))
    data=([[toolName,record]])
    toolName=input('Please input the name of the tools to be recorded next:')
    
    while toolName!='\end':
        record= sd.rec(int(duration * 1000))
        record=record_adjust(record,threshold)
        sd.wait(print('Speaking...'))
        data.append([toolName,record])
        toolName=input('Please input the name of the tools to be recorded next:')
    
    return(data)