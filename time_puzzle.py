from tkinter import *
import tkinter as tk
import time

class Watch(tk.Frame):
    def __init__(self, parent, **kw):
        tk.Frame.__init__(self, parent, kw)
        self._start = 0.0
        self._elapsedtime = 0.0
        self._running = 0
        self.timestr = StringVar()
        self.makeWidgets()
    def makeWidgets(self):
        ceas = tk.Label(self, textvariable=self.timestr,font=("Arial Bold", 14), bg="white")
        self._setTime(self._elapsedtime)
        ceas.pack(fill=X, expand=NO, pady=3, padx=3)
    def _update(self):
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)
    def _setTime(self, elap):
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        self.timestr.set('%02d:%02d' % (minutes, seconds))
    def Start(self):
        if not self._running:
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1
    def Stop(self):
       self.timer_running=False
