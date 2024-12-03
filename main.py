import cv2
import threading 
import numpy as np
import tensorflow as tf
import platform as plt
from tools import CustomVideoCapture, preprocess, parse_output
import time
import socket
import tkinter as tk
from tkinter import messagebox

def button_event():
    global key_in
    print(myentry.get())
    while myentry.get():
        tk.messagebox.showinfo('Confirm', "You want to exercise for %s s" % myentry.get())
        break
    key_in = int(myentry.get())
    