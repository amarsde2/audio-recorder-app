# Audo recording App 
# This is a simple which let you record audio and save

# In this project we are using sounddevice and wavio library to record and save audio

# Author Details 
# Name  :  Er. Amar kumar 
# Email :  amarkumar9685079691@gmail.com 

# Start of a source code

''' 
  This is audio recording app which build using  following library and modules 
  1. sounddevice
  2. soundfile 
  3. tempfile 
  4. queue 
  5. sys 
  6. argparse 

'''

import sounddevice as sd
import soundfile as sf
import tempfile
import argparse 
import queue
import sys 


class AudioRecordApp:
    
    _parser = None
    _args = None
    _remaining = None
    _qs = None

    def __init__(self):
     
        self._parser = argparse.ArgumentParser(add_help=False)
        self._parser.add_argument('-l','--list-devices', action='store_true', help="show list of available audio devices")
        self._args, self._remaining = self._parser.parse_known_args()
        self._qs = queue.Queue()
     
    # start message to list available devices 
    def startMessage(self):  
        if self._args.list_devices:
            print(sd.query_devices())
            self._parser.exit(0)

    
    # callback function to process audio block into queue 
    def callback(self, data, frames, time, status):
        if status:
            print(status, file = sys.stderr)
        self._qs.put(data.copy())
    
    # helper function for convert str to int 
    def  str_to_int(self, text):
        try:
            return int(text)
        except:
            print("Error!")
            self._parser.exit(1)
            exit(1) 

    def setupArguments(self):
        self._parser = argparse.ArgumentParser(description=self.__dict__,
                                               formatter_class=argparse.RawDescriptionHelpFormatter,
                                               parents=[self._parser])
        self._parser.add_argument('filename',nargs='?',metavar='FILENAME', help='file to store audio recording')
        self._parser.add_argument('-d','--device', type=self.str_to_int,help='input device can be int id or str name')
        self._parser.add_argument('-r','--samplerate',type=int, help="sampling rate")
        self._parser.add_argument('-c','--channels',type=int,default=1,help="number of channels")
        self._parser.add_argument('-t','--subtype', type=str, help="sound file subtype")
        self._args = self._parser.parse_args(self._remaining)
    
    def record(self):
        self.startMessage()
        self.setupArguments()
        try:
           
            if self._args.samplerate is None:
               device_info = sd.query_devices(self._args.device,'input')
               self._args.samplerate = int(device_info['default_samplerate'])
            
            if self._args.filename is None:
                self._args.filename = tempfile.mktemp(prefix='audio_rec_', suffix='.wav', dir='')

            
            with sf.SoundFile(self._args.filename,mode='x',samplerate=self._args.samplerate,channels=self._args.channels,subtype=self._args.subtype) as file:
                with sd.InputStream(samplerate=self._args.samplerate,device=self._args.device,channels=self._args.channels, callback=self.callback):
                  while True:
                      file.write(self._qs.get())

        except KeyboardInterrupt:
            print("Recording saved: " + repr(self._args.filename))
            self._parser.exit(0)
        except Exception as e:
            self._parser.exit(type(e).__name__ + ':'+str(e))

           
        


if __name__ == "__main__":
    app = AudioRecordApp()
    print("*" * 80)
    print("Recording start....")
    print("Print Ctrl + C Key to stop and save recording")
    app.record()
    

