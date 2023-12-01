import tkinter as tk
import keyboard
import time
from tkinter import messagebox
from pymem import *

dwEntityList = (0x4D4F25C)
m_iTeamNum = (0xF4) 
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
    exit(0)
    
btn = tk.Button(app,text="Active wall hack",command=show_message)
btn.place(x=10,y=10,width=150,height=20)


def activate_wall():
    try:
        pm = pymem.Pymem('cs2.exe')
        client = pymem.process.module_from_name(pm.process_handle,"client.dll").lpBaseOfDll
        
        while True: 
            if keyboard.press('shift+f10'):
                stop_wall(0)
            time.sleep(0.001)
            for i in range(32):
                entity = pm.read_int(client + dwEntityList * i * 0x10)
                if entity:
                    entity_team_id = pm.read_int(entity + m_iTeamNum)
                    
                    if entity_team_id == 2: 
                        pm.write_int(entity + m_clrRender, (rgbT[0]))
                        pm.write_int(entity + m_clrRender + 0x1, (rgbT[1]))
                        pm.write_int(entity + m_clrRender + 0x2, (rgbT[2]))
                    elif entity_team_id == 3:
                        pm.write_int(entity + m_clrRender, (rgbCT[0]))
                        pm.write_int(entity + m_clrRender + 0x1, (rgbCT[1]))
                        pm.write_int(entity + m_clrRender + 0x2, (rgbCT[2]))    
        
    except Exception as e: 
        show_message_error(e)
    
app.mainloop()