import cv2
import threading
import os
import numpy as np
import tensorflow as tf
import tkinter as tk
from tkinter import messagebox
from tools import CustomVideoCapture, preprocess, parse_output

# -------------------------
# GUI 設定 (用於輸入目標次數)
# -------------------------
def button_event():
    global key_in
    if myentry.get():
        tk.messagebox.showinfo('Confirm', f"You want to exercise for {myentry.get()} times")
        key_in = int(myentry.get())
        root.destroy()

def validate(P):
    if str.isdigit(P) or P == '':
        return True
    else:
        return False

root = tk.Tk()
root.title('Exercise Time')
root.geometry('250x50')

mylabel = tk.Label(root, text='Number of times')
mylabel.grid(row=0, column=0)

vcmd = (root.register(validate), '%P')
myentry = tk.Entry(root, validate='key', validatecommand=vcmd)
myentry.grid(row=0, column=1)

mybutton = tk.Button(root, text='Enter', command=button_event)
mybutton.grid(row=1, column=0)

mybutton2 = tk.Button(root, text='Exit', command=root.destroy)
mybutton2.grid(row=1, column=1)

root.mainloop()

# -------------------------
# AI 模型與參數設置
# -------------------------
labels = ["Relax", "Move", "Curl"]  # 動作標籤
model = tf.keras.models.load_model("keras_model.h5", compile=False)  # 加載模型

# 設定運動計數相關變數
Curl_Count = 0
last_trg_class = ''

# 設定影像擷取
vid = CustomVideoCapture()
vid.set_title('Biovlsi')
vid.start_stream()

# -------------------------
# 運動次數計算邏輯
# -------------------------
while not vid.isStop:
    ret, frame = vid.get_current_frame()
    if not ret:
        continue  # 確保有效幀數

    # AI 推論
    data = preprocess(frame, resize=(224, 224), norm=True)
    prediction = model(data)[0]
    trg_id, trg_class, trg_prob = parse_output(prediction, labels)

    # 判斷動作次數
    if last_trg_class == labels[2] and trg_class == labels[0]:  # 從 Curl 到 Relax
        Curl_Count += 1
        print(f"Curl Count: {Curl_Count}")

    # 停止條件
    if Curl_Count == key_in:
        print("Finish curl")
        break

    last_trg_class = trg_class
    vid.info = f'{trg_class}, Count: {Curl_Count}'

# -------------------------
# 完成後顯示訊息
# -------------------------
vid.info = f'Finish {Curl_Count} times curls. Please press Esc'
while vid.isStop:
    root1 = tk.Tk()
    root1.title('Congratulations')
    root1.geometry('500x500')
    mylabel1 = tk.Label(root1, text=f'You finished {key_in} curls', fg='red', bd=200, cursor='cross', font=('Times New Roman', 30)).pack()
    mybutton2 = tk.Button(root1, text='OK', command=root1.destroy).pack()
    root1.mainloop()

# -------------------------
# 結束程式
# -------------------------
time.sleep(1)
print('-' * 30)
print(f'影像串流的線程是否已關閉 : {not vid.t.is_alive()}')
print('離開程式')
