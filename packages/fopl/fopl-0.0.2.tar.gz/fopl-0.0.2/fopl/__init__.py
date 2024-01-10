import os
import re
from tkinter import *
from tkinter import ttk


def main():
    command = 'curl https://www.besoccer.com/team/squad/internazionale'
    res = os.popen(command).read()
    players = re.findall('<a href=.* data-cy=\"player\">(.*)<\/a>', res)

    window = Tk()
    window.title("Internazionale Squad")
    frm = ttk.Frame(window, padding=100)
    frm.grid()
    ttk.Label(frm, text="Hello, Internazionale soccer team players are: ").grid(column=0, row=0)

    for idp, player in enumerate(players):
       ttk.Label(frm, text=player).grid(column=0, row=idp+1)

    window.mainloop()
