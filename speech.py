import speech_recognition as sr

#Recognize audio files
#harvard = sr.AudioFile('harvard.wav')
#r=sr.Recognizer()

#with harvard as source:
#    audio=r.record(source)    
#r.recognize_google(audio)


#Recognize microphone input
mic=sr.Microphone()
with mic as source:
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)
