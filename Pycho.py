import keyboard
import tkinter as tk
import pygame
import pymem.exception
import time
from threading import Thread
from pymem import *
from pymem.process import *
from pymem.ptypes import RemotePointer
from time import sleep

mem = Pymem("Psychonauts")

module = module_from_name(mem.process_handle, "Psychonauts.exe").lpBaseOfDll

health_offsets = [0X0, 0X4, 0X0, 0X100, 0X10, 0X0, 0X2C8]
gravity_offsets = [0X0, 0X94]


def getpointeraddress(base, offsets):
    remote_pointer = RemotePointer(mem.process_handle, base)
    for offset in offsets:
        if offset != offsets[-1]:
            remote_pointer = RemotePointer(mem.process_handle, remote_pointer.value + offset)
        else:
            return remote_pointer.value + offset


def multi_run_god():
    new_thread = Thread(target=god_hack, daemon=True)
    new_thread.start()


def multi_run_gravity():
    new_thread = Thread(target=fuck_gravity, daemon=True)
    new_thread.start()


def god_hack():
    addr = getpointeraddress(module + 0x0038CBB8, health_offsets)
    while 1:
        try:
            mem.write_int(addr, 0x47960000)

            sleep(0.02)
            if keyboard.is_pressed("space"):
                keyboard.press_and_release("space")
                sleep(0.07)
                continue
        except pymem.exception.MemoryWriteError as e:
            print(f"Error writing memory: {e}")
        if keyboard.is_pressed("F1"):
            break


def fuck_gravity():
    addr = getpointeraddress(module + 0x00386AE0, gravity_offsets)
    while 1:
        try:
            mem.write_int(addr, 0x1380)
        except pymem.exception.MemoryWriteError as e:
            print(f"Error writing memory: {e}")
        if keyboard.is_pressed("C"):
            mem.write_int(addr, 0x1)
            break


pygame.init()
pygame.mixer_music.load("music/mod.mp3")
pygame.mixer_music.play(1)

root = tk.Tk()
root.title("Fragging Terminal")
root.geometry("200x180")
root.configure(background='dark red')
root.attributes("-topmost", True)


def show():
    root.deiconify()


def hide():
    root.withdraw()


button1 = tk.Button(root, text="God Mode", bg='black', fg='white', command=multi_run_god)
button1.grid(row=0, column=0)
button2 = tk.Button(root, text="Fuck Gravity", bg='black', fg='white', command=multi_run_gravity)
button2.grid(row=1, column=0)
button4 = tk.Button(root, text="Exit", bg='white', fg='black', command=root.destroy)
button4.grid(row=3, column=0)
label4 = tk.Label(master=root, text='C Show GUI', bg='red', fg='black')
label4.grid(row=0, column=3)
label5 = tk.Label(master=root, text='V Hide GUI', bg='red', fg='black')
label5.grid(row=1, column=3)
label6 = tk.Label(master=root, text='F1 KILLS LOOPS', bg='red', fg='black')
label6.grid(row=2, column=3)
label6 = tk.Label(master=root, text='F Fuck Gravity', bg='red', fg='black')
label6.grid(row=3, column=3)
label8 = tk.Label(master=root, text='K KILL EXE', bg='red', fg='black')
label8.grid(row=4, column=3)

keyboard.add_hotkey("c", show)
keyboard.add_hotkey("v", hide)
keyboard.add_hotkey("F", fuck_gravity)
keyboard.add_hotkey("k", root.destroy)
root.mainloop()
