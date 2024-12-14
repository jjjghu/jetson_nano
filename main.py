import cv2
import tkinter as tk
from tkinter import messagebox
import tensorflow as tf
from tools import CustomVideoCapture, preprocess, parse_output

# GUI：輸入需要運動的次數
def button_event():
    global key_in
    if myentry.get().isdigit():
        tk.messagebox.showinfo('Confirm', "You want to exercise for %s times" % (myentry.get()))
        key_in = int(myentry.get())
        root.destroy()
    else:
        tk.messagebox.showerror("Invalid Input", "Please enter a valid number.")

root = tk.Tk()
root.title('Exercise Time')
root.geometry('250x100')

mylabel = tk.Label(root, text='Number of times')
mylabel.grid(row=0, column=0)

myentry = tk.Entry(root)
myentry.grid(row=0, column=1)

mybutton = tk.Button(root, text='Enter', command=button_event)
mybutton.grid(row=1, column=0, columnspan=2)

root.mainloop()

# 加載模型與標籤
label = ["Relax", "Move", "Curl"]
model = tf.keras.models.load_model("keras_model.h5", compile=False)

# 初始化參數
Curl_Count = 0
last_trg_class = ""

# 設定影像擷取
vid = CustomVideoCapture()
vid.set_title('Biovlsi')
vid.start_stream()

while not vid.isStop:
    # 取得當前圖片
    ret, frame = vid.get_current_frame()
    if not ret:
        continue

    # 進行預處理與推論
    data = preprocess(frame, resize=(224, 224), norm=True)
    prediction = model(data)[0]

    # 解析 AI 輸出
    trg_id, trg_class, trg_prob = parse_output(prediction, label)

    # 檢測「卷曲」與「放鬆」的切換，計數次數
    if last_trg_class == label[2] and trg_class == label[0]:  # 上次是 Curl，這次是 Relax
        Curl_Count += 1
        print(f"Count: {Curl_Count}")

    # 終止條件
    if Curl_Count == key_in:
        print("Finish curl")
        break

    last_trg_class = trg_class
    vid.info = f'{trg_class} , Count: {Curl_Count}'

# 顯示完成訊息
vid.info = ('Finish %s times curls! Please press Esc' % Curl_Count)
root1 = tk.Tk()
root1.title('Congratulation')
root1.geometry('300x100')
mylabel1 = tk.Label(root1, text='You finish %s times curls' % key_in, fg='red', font=('Times New Roman', 20))
mylabel1.pack()
mybutton2 = tk.Button(root1, text='OK', command=root1.destroy)
mybutton2.pack()
root1.mainloop()
