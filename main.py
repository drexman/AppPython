import tkinter as tk
import keyboard
import time
from tkinter import messagebox
from pymem import *

dwEntityList = (0x17BB820)
m_iTeamNum = (0x3bf) 
m_clrRender = (0x70)

rgbT = [255,51,0]
rgbCT = [0,51,255]

app = tk.Tk()

app.title("Cheat CS")
app.geometry("500x300")
app.configure(background="#008")

def show_message():
    messagebox.showinfo("Message","Active wall hack")
    activate_wall()
    
def show_message_error(msg):
    messagebox.showerror("error", msg)
    
def stop_wall():
    messagebox.showinfo("Message","Desactive wall hack")
    
btn = tk.Button(app,text="Active wall hack",command=show_message)
btn.place(x=10,y=10,width=150,height=20)


def activate_wall():
    try:
        pm = pymem.Pymem('cs2.exe')
        client = pymem.process.module_from_name(pm.process_handle,"client.dll").lpBaseOfDll
        
        while True:
            if keyboard.read_key() == 'esc':
                print('desactive wall hack')
                stop_wall()
                break
            time.sleep(0.01)
            
            for i in range(32):
                list_entry = pm.read_int(client + dwEntityList + (i * 0x10))
             
                
                if list_entry:
                    entity_team_id = pm.read_int(list_entry+ m_iTeamNum)
                    print(entity_team_id)
                    
    except Exception as e: 
        show_message_error(e)
    
app.mainloop()