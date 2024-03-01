import tkinter as tk
import keyboard
import time
import base64
import json
import wave
from tkinter import messagebox
from pymem import *
import pyaudio
from websocket._abnf import ABNF
import threading
import configparser
import base64
import datetime
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


flag = False

class settings:
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 16000
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

def get_url():
    config = configparser.RawConfigParser()
    config.read('config.cfg')
    region = config.get('auth','region')
    host = REGION_MAP['us-east']
    return ("wss://{}/speech-to-text/api/v1/recognize"
           "?model=en-AU_BroadbandModel").format(host)


def activate_listening_mode():
    print(get_apikey())
    authenticator = IAMAuthenticator('mwifKfeLVtW6wWQvx2WcWLMR22WzsfHQy_kx20CayPzf')
    service = SpeechToTextV1(authenticator=authenticator)
    service.set_service_url('https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/890d865a-8921-4e6d-8b01-dc4acf9eee55')
    models = service.list_models().get_result()
    
    print(json.dumps(models, indent=2))

    model = service.get_model('en-US_BroadbandModel').get_result()
    print(json.dumps(model, indent=2))
    audio = pyaudio.PyAudio()
    stream = audio.open(rate=settings.RATE, channels=settings.CHANNELS, format=settings.FORMAT, input=True,
                        frames_per_buffer=settings.CHUNCK)
    stream.start_stream()
    print('Escutando....')
    frames = []

    while True:
        global flag
        if flag:
            break
        else:
            data = stream.read(settings.CHUNCK)
            frames.append(data)
     
    # Disconnect the audio stream
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    today_date = datetime.date.today()
    today_format = today_date.strftime("-%d-%m-%Y")
   
    #Save audio to file
    wf = wave.open("output{}.wav".format(today_format), 'wb')
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

def open_listening_mode():
    global listening_button
    global stop_button
    listening_button['state'] = "disabled"
    stop_button['state'] = 'active'
    global t
    t = threading.Thread(target=activate_listening_mode)

    threading.Event
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
    if t.is_alive():
        stop_listening_mode()
    app.destroy()

        
def main():
    global listening_button
    global stop_button
    global app
    global service
    app = tk.Tk()

    app.title("Traslate App")
    app.geometry("600x400")
    app.configure(background="#E8E0C8")
    app.protocol("WM_DELETE_WINDOW", on_closing)
    listening_icon = tk.PhotoImage(file='./assets/listening.png')
    stop_icon = tk.PhotoImage(file='./assets/stop.png')

    listening_button = tk.Button(
        app,
        image=listening_icon,
        text='Active listening mode',
        compound=tk.LEFT,
        command=open_listening_mode
    )

    listening_button.place(
        width=170,
        x=230,
        y=120
    )

    stop_button = tk.Button(
        app,
        image=stop_icon,
        text='Stop listening',
        compound=tk.LEFT,
        command= stop_listening_mode,
        state=tk.DISABLED
    )

    stop_button.place(
        width=170,
        x=230,
        y=180
    )
   
    app.mainloop()

if __name__ == "__main__":
    main()