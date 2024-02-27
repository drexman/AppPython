import tkinter as tk
import keyboard
import time
import base64
import json
import wave
from tkinter import messagebox
from pymem import *
import pyaudio
import websocket
from websocket._abnf import ABNF
import threading
import configparser
import base64
import datetime

flag = False

class WorkerThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            print("Thread is running...")
            time.sleep(1)

    def stop(self):
        self._stop_event.set()

class settings:
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
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

def get_auth():
    config = configparser.RawConfigParser()
    config.read('config.cfg')
    apikey = config.get('auth', 'apikey')
    return ("apikey", apikey)

def get_url():
    config = configparser.RawConfigParser()
    config.read('config.cfg')
    region = config.get('auth','region')
    host = REGION_MAP['us-east']
    return ("wss://{}/speech-to-text/api/v1/recognize"
           "?model=en-AU_BroadbandModel").format(host)


def activate_listening_mode():
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
    app = tk.Tk()

    headers = {}
    userpass = ":".join(get_auth())
    headers["Authorization"] = "Basic " + base64.b64encode(
        userpass.encode()).decode()
    url = get_url()

    #ws = websocket.WebSocket(url, header=headers, on_message=on_message, on_error=on_error, on_close=on_close)
    data = {
        "action": "start",
        # this means we get to send it straight raw sampling
        "content-type": "audio/l16;rate=%d" % settings.RATE,
        "continuous": True,
        "interim_results": True,
        # "inactivity_timeout": 5, # in order to use this effectively
        # you need other tests to handle what happens if the socket is
        # closed by the server.
        "word_confidence": True,
        "timestamps": True,
        "max_alternatives": 3
    }
    #print(json.dumps(data).encode('utf8'))
    #ws.send(json.dumps(data).encode('utf8'))

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