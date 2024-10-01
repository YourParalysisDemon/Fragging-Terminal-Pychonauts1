import keyboard
import tkinter as tk
import pygame
import pymem.exception
import webbrowser
from threading import Thread
from pymem import *
from pymem.process import *
from pymem.ptypes import RemotePointer
from time import sleep

while True:
    password = input("Enter password ")
    if password == "115":
        print("Welcome")
        break
    else:
        print("Try again retard")


mem = Pymem("Psychonauts")

module1 = module_from_name(mem.process_handle, "Psychonauts.exe").lpBaseOfDll

health1_offsets = [0X0, 0X4, 0X0, 0X100, 0X10, 0X0, 0X2C8]
gravity1_offsets = [0X0, 0X94]


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


def multi_run_legendary():
    new_thread = Thread(target=Legendary_mode, daemon=True)
    new_thread.start()


def god_hack():
    addr = getpointeraddress(module1 + 0x0038CBB8, health1_offsets)
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


def Legendary_mode():
    addr = getpointeraddress(module1 + 0x0038CBB8, health1_offsets)
    while 1:
        try:
            mem.write_int(addr, 0x0)
        except pymem.exception.MemoryWriteError as e:
            print(f"Error writing memory: {e}")
        if keyboard.is_pressed("F1"):
            break


def fuck_gravity():
    addr = getpointeraddress(module1 + 0x00386AE0, gravity1_offsets)
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
photo = tk.PhotoImage(file="back/155.png")
root.wm_iconphoto(False, photo)
root.attributes("-topmost", True)
root.title("Fragging Terminal")
root.configure(background='dark red')
root.geometry("265x145")


def callback(url):
    webbrowser.open_new(url)


def show():
    root.deiconify()


def hide():
    root.withdraw()


button1 = tk.Button(root, text="God Mode", bg='black', fg='white', command=multi_run_god)
button1.grid(row=1, column=0)
button2 = tk.Button(root, text="Fuck Gravity", bg='black', fg='white', command=multi_run_gravity)
button2.grid(row=2, column=0)
button3 = tk.Button(root, text="Legendary Mode", bg='black', fg='white', command=multi_run_legendary)
button3.grid(row=3, column=0)
button4 = tk.Button(root, text="Exit", bg='white', fg='black', command=root.destroy)
button4.grid(row=4, column=0)
label1 = tk.Label(master=root, text='C Show GUI', bg='red', fg='black')
label1.grid(row=0, column=3)
label2 = tk.Label(master=root, text='V Hide GUI', bg='red', fg='black')
label2.grid(row=1, column=3)
label3 = tk.Label(master=root, text='F1 KILLS LOOPS', bg='red', fg='black')
label3.grid(row=2, column=3)
label4 = tk.Label(master=root, text='F Fuck Gravity', bg='red', fg='black')
label4.grid(row=3, column=3)
label5 = tk.Label(master=root, text='K KILL EXE', bg='red', fg='black')
label5.grid(row=4, column=3)
label6 = tk.Label(master=root, text='Main Loops', bg='red', fg='black')
label6.grid(row=0, column=0)
label8 = tk.Label(master=root, text='C Fix Gravity', bg='red', fg='black')
label8.grid(row=5, column=3)
link1 = tk.Label(root, text="Your Sleep Paralysis Demon", bg="black", fg="red", cursor="hand2")
link1.grid(row=5, column=0)
link1.bind("<Button-1>", lambda e: callback("https://steamcommunity.com/profiles/76561198259829950/"))


keyboard.add_hotkey("c", show)
keyboard.add_hotkey("v", hide)
keyboard.add_hotkey("F", fuck_gravity)
keyboard.add_hotkey("k", root.destroy)
root.mainloop()
