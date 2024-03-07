import tkinter as tk
import keyboard
import time
import base64
import json
import wave
from tkinter import messagebox, ttk
from pymem import *
import pyaudio
from websocket._abnf import ABNF
import threading
import configparser
import base64
import datetime
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import numpy as np


flag = False

class settings:
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE =  44100
    CHUNCK = 1024
    DURATION = 10

REGION_MAP = {
    'us-east': 'gateway-wdc.watsonplatform.net',
    'us-south': 'stream.watsonplatform.net',
    'eu-gb': 'stream.watsonplatform.net',
    'eu-de': 'stream-fra.watsonplatform.net',
    'au-syd': 'gateway-syd.watsonplatform.net',
    'jp-tok': 'gateway-syd.watsonplatform.net',
}

def show_message():
    messagebox.showinfo("Message","Active wall hack")
 
def show_message_error(msg):
    messagebox.showerror("error", msg)

def on_message(self, msg):
    print(msg)


def on_error(self, error):
    """Print any errors."""
    print(error)

def on_close(ws):
    print('encerrando serviço ws')

def get_apikey():
    config = configparser.RawConfigParser()
    config.read('config.cfg')
    apikey = config.get('auth', 'apikey')
    return apikey


def list_audio_devices():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')

    devices = []
    for i in range(num_devices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        device_name = device_info.get('name')
        print(device_info)
        devices.append(device_name)

    p.terminate()
    return devices

def activate_listening_mode(service):
    audio = pyaudio.PyAudio()
    stream = audio.open(rate=settings.RATE, channels=settings.CHANNELS, format=settings.FORMAT, input=True,frames_per_buffer=settings.CHUNCK)
    stream.start_stream()
    print('Escutando....')
    frames = []
    index = 0

    while True:
        global flag
        if flag:
            break
        else:
            data = stream.read(settings.CHUNCK)
            frames.append(data)
            array = np.array(frames)
            memory_usage = array.itemsize * len(array)
            
            print(index)
            print(memory_usage)
            if(memory_usage > 102400):
                print('removido')
            index = index + 1
     
    # Disconnect the audio stream
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    today_date = datetime.date.today()
    today_format = today_date.strftime("-%d-%m-%Y")
    filename = "output{}.wav".format(today_format)

    #Save audio to file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(settings.CHANNELS)
    wf.setsampwidth(audio.get_sample_size(settings.FORMAT))
    wf.setframerate(settings.RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print('Audio foi gravado com sucesso')
    
    with open("output{}.wav".format(today_format), mode="rb") as wav: 
        result = service.recognize(
            audio=wav, 
            content_type='audio/wav',
            timestamps=True,
            word_confidence=True
        ).get_result()
        if 'results' in result and len(result['results']) > 0:
            transcript = result['results'][0]['alternatives'][0]['transcript']
            print("Transcription:", transcript)
        else:
            print("No transcription available.")
  


def open_listening_mode(service):
    global listening_button
    global stop_button
    global flag
    flag = False
    listening_button['state'] = "disabled"
    stop_button['state'] = 'active'
    global t
    
    t = threading.Thread(target=activate_listening_mode, args=[service,])
    t.start()

def stop_listening_mode():
    global listening_button
    global stop_button
    listening_button['state'] = "active"
    stop_button['state'] = 'disabled'
    global flag
    flag=True

def on_closing():
    global t
    global app
    try:
        if t.is_alive():
            stop_listening_mode()
        app.destroy()
    except NameError:
        app.destroy()
       
def main():
    global listening_button
    global stop_button
    global app
    global service
    app = tk.Tk()
    print(list_audio_devices())

    app.title("Traslate App")
    app.geometry("600x400")
    app.configure(background="#E8E0C8")
    app.protocol("WM_DELETE_WINDOW", on_closing)


    authenticator = IAMAuthenticator('mwifKfeLVtW6wWQvx2WcWLMR22WzsfHQy_kx20CayPzf')
    service = SpeechToTextV1(authenticator=authenticator)
    service.set_service_url('https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/890d865a-8921-4e6d-8b01-dc4acf9eee55')
    models = service.list_models().get_result()
    print(json.dumps(models, indent=2))

    

    model = service.get_model('en-US_BroadbandModel').get_result()
    print(json.dumps(model, indent=2))

    labelFrame = tk.LabelFrame(app,text='Dipositivos',height=80,width=500)
    labelFrame.pack(side=tk.TOP)  
    devices_combobox = ttk.Combobox(labelFrame, width=40, value=list_audio_devices())
    devices_combobox.grid(column=0, row=0, padx=10, pady=10, sticky='w')
    listening_icon = tk.PhotoImage(file='./assets/listening.png')
    stop_icon = tk.PhotoImage(file='./assets/stop.png')


    labelFrameAction = tk.LabelFrame(app,text='Ação',height=80,width=500)
    labelFrameAction.pack(side=tk.BOTTOM)

    listening_button = tk.Button(
        labelFrameAction,
        width=180,
        image=listening_icon,
        text='Active listening mode',
        compound=tk.LEFT,
        command=lambda: open_listening_mode(service)
    )
    listening_button.grid(column=3, row=0, padx=10, pady=10, sticky='w')

    stop_button = tk.Button(
        labelFrameAction,
        width=180,
        image=stop_icon,
        text='Stop listening',
        compound=tk.LEFT,
        command= stop_listening_mode,
        state=tk.DISABLED
    )
    stop_button.grid(column=4, row=0, padx=10, pady=10, sticky='w')

    app.mainloop()

if __name__ == "__main__":
    main()