# Audo recording App 
# This is a simple which let you record audio and save

# In this project we are using sounddevice and scipy library to record and save audio

# Author Details 
# Name  :  Er. Amar kumar 
# Email :  amarkumar9685079691@gmail.com 

# Start of a source code

import sounddevice as sd
import wavio as vw


class AudioRecordApp:
    _channels = 2
    _freq = 48000
    _duration = 5
    
    def record(self):
        recording = sd.rec(int(self._duration * self._freq), samplerate=self._freq, channels=2)
        sd.wait()
        vw.write("live_record.wav",recording,self._freq,sampwidth=2)
        print("Recording End: ")
        



if __name__ == "__main__":
    app = AudioRecordApp()
    print("Recording Start: ")
    app.record()

