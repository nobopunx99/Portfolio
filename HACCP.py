### HACCP衛生管理プログラム ###

# オーディオ再生インポート
import sounddevice as sd
import wave
import numpy as np

# 時間インポート
import datetime
from time import strftime

# DB作成用インポート
import pandas as pd
import sqlite3

# GUIインポート
import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk, Image

# オーディオ再生関数
def voice():
    wf = wave.open("eiseikannri.wav")
    fs = wf.getframerate()
    data = wf.readframes(wf.getnframes())
    data = np.frombuffer(data, dtype='int16')
    sd.play(data, fs)
    # status = sd.wait()
voice()

# 原材料の受入確認の画面
def accept():
    win = tk.Toplevel() #Toplevel=別ウインドウ作成
    win.title("一般的衛生管理")
    win.geometry("300x200+1030+250")
    label = ttk.Label(win, text="\n①原材料の受入確認\n")
    label.pack(anchor=tk.N)
    button1 = ttk.Button(win, text="良", command=lambda:[ok1(), win.destroy(), temp()])
    button1.pack(anchor=tk.N)
    button2 = ttk.Button(win, text="否", command=lambda:[ng1(), win.destroy(), temp()])
    button2.pack(anchor=tk.N)
    # 別ウィンドウで画像表示
    global pwin
    pwin = tk.Tk() #Toplevel=別ウインドウ作成
    pwin.title("一般的衛生管理マニュアル")
    pwin.geometry("630x800+400+0")
    canvas = tk.Canvas(pwin, bg="grey", width=630, height=800)
    canvas.pack()
    global img #グローバル宣言。ローカルオブジェクトは消滅する為。
    img = Image.open("HACCP_ippan.png")
    img = img.resize(size=(630, 800))
    global photo #グローバル宣言。ローカルオブジェクトは消滅する為。
    photo = ImageTk.PhotoImage(img, master=pwin)
    canvas.place(x=0, y=0)
    canvas.create_image(320, 400, image=photo) #画像位置(x, y)

#冷蔵庫の温度チェックする画面設定
def temp():
    win = tk.Toplevel() #Toplevel=別ウインドウ作成
    win.title("一般的衛生管理")
    win.geometry("300x200+1030+250")
    label = ttk.Label(win, text="\n②庫内温度の確認\n")
    label.pack(anchor=tk.N)
    label = ttk.Label(win, text="冷蔵庫(℃)")
    label.pack(anchor=tk.N)
    global entry_fr
    entry_fr = tk.Entry(win, width=10)
    entry_fr.pack(anchor=tk.N)
    label = ttk.Label(win, text="冷凍庫(℃)")
    label.pack(anchor=tk.N)
    global entry_fz
    entry_fz = tk.Entry(win, width=10)
    entry_fz.pack(anchor=tk.N)
    button1 = ttk.Button(win, text="OK", command=lambda:[temp_get(), win.destroy(), check_infect()])
    button1.pack(anchor=tk.N)

#入力した温度の入力内容を取得して変数定義する関数
def temp_get():
    global fr_temp
    fr_temp = entry_fr.get()
    global fz_temp
    fz_temp = entry_fz.get()

#二次感染をチェックする画面
def check_infect():
    win = tk.Toplevel() #Toplevel=別ウインドウ作成
    win.title("一般的衛生管理")
    win.geometry("300x200+1030+250")
    label = ttk.Label(win, text="\n③-1交差汚染・二時汚染の防止\n")
    label.pack(anchor=tk.N)
    button1 = ttk.Button(win, text="良", command=lambda:[ok3_1(), win.destroy(), tool_disinfect()])
    button1.pack(anchor=tk.N)
    button2 = ttk.Button(win, text="否", command=lambda:[ng3_1(), win.destroy(), tool_disinfect()])
    button2.pack(anchor=tk.N)

def tool_disinfect():
    win = tk.Toplevel() #Toplevel=別ウインドウ作成
    win.title("一般的衛生管理")
    win.geometry("300x200+1030+250")
    label = ttk.Label(win, text="\n③-2器具等の洗浄・消毒・殺菌\n")
    label.pack(anchor=tk.N)
    button1 = ttk.Button(win, text="良", command=lambda:[ok3_2(), win.destroy(), toilet_disinfect()])
    button1.pack(anchor=tk.N)
    button2 = ttk.Button(win, text="否", command=lambda:[ng3_2(), win.destroy(), toilet_disinfect()])
    button2.pack(anchor=tk.N)
    
def toilet_disinfect():
    win = tk.Toplevel() #Toplevel=別ウインドウ作成
    win.title("一般的衛生管理")
    win.geometry("300x200+1030+250")
    label = ttk.Label(win, text="\n③-3トイレの洗浄・消毒\n")
    label.pack(anchor=tk.N)
    button1 = ttk.Button(win, text="良", command=lambda:[ok3_3(), win.destroy(), manage_health()])
    button1.pack(anchor=tk.N)
    button2 = ttk.Button(win, text="否", command=lambda:[ng3_3(), win.destroy(), manage_health()])
    button2.pack(anchor=tk.N)

#従業員の健康チェックする画面
def manage_health():
    win = tk.Toplevel() #Toplevel=別ウインドウ作成
    win.title("一般的衛生管理")
    win.geometry("300x200+1030+250")
    label = ttk.Label(win, text="\n④-1従業員の健康管理等\n")
    label.pack(anchor=tk.N)
    button1 = ttk.Button(win, text="良", command=lambda:[ok4_1(), win.destroy(), wash_hand()])
    button1.pack(anchor=tk.N)
    button2 = ttk.Button(win, text="否", command=lambda:[ng4_1(), win.destroy(), wash_hand()])
    button2.pack(anchor=tk.N)

#手洗いをチェックする画面
def wash_hand():
    win = tk.Toplevel() #Toplevel=別ウインドウ作成
    win.title("一般的衛生管理")
    win.geometry("300x200+1030+250")
    label = ttk.Label(win, text="\n④-2手洗いの実施\n")
    label.pack(anchor=tk.N)
    button1 = ttk.Button(win, text="良", command=lambda:[ok4_2(), win.destroy(), name()])
    button1.pack(anchor=tk.N)
    button2 = ttk.Button(win, text="否", command=lambda:[ng4_2(), win.destroy(), name()])
    button2.pack(anchor=tk.N)

#チェック者の氏名入力画面
def name():
    win = tk.Toplevel() #Toplevel=別ウインドウ作成
    win.title("一般的衛生管理")
    win.geometry("300x200+1030+250")
    label1 = ttk.Label(win, text="\n日々チェック\n")
    label1.pack(anchor=tk.N)
    label2 = ttk.Label(win, text="名前を入力(このチェックを行なった人の)")
    label2.pack(anchor=tk.N)
    global entry_name
    entry_name = tk.Entry(win, width=20)
    entry_name.pack(anchor=tk.N)
    button2 = ttk.Button(win, text="OK", command=lambda:[name_get(), win.destroy(), memo_input()])
    button2.pack(anchor=tk.N)

# チェック者氏名の入力内容を取得して変数定義する関数
def name_get():
    global check_name
    check_name = entry_name.get()

# 特記事項入力の関数
def memo_input():
    win = tk.Toplevel() #Toplevel=別ウインドウ作成
    win.title("一般的衛生管理")
    win.geometry("300x200+1030+250")
    label = ttk.Label(win, text="\n特記事項メモ\n")
    label.pack(anchor=tk.N)
    global entry4
    entry4 = tk.Entry(win, width=50)
    entry4.pack(anchor=tk.N)
    entry4.insert(tk.END, "なし")
    button1 = ttk.Button(win, text="保存", command=lambda:[memo_get(), win.destroy(), wcheck_name()])
    button1.pack(anchor=tk.N)

# 特筆事項の入力内容を取得して変数定義する関数
def memo_get():
    global memo
    memo = entry4.get()

# Wチェック者の氏名入力画面
def wcheck_name():
    win = tk.Toplevel() #Toplevel=別ウインドウ作成
    win.title("一般的衛生管理")
    win.geometry("300x200+1030+250")
    label = ttk.Label(win, text="\n確認者の名前を入力\n")
    label.pack(anchor=tk.N)
    global wentry_name
    wentry_name = tk.Entry(win, width=20)
    wentry_name.pack(anchor=tk.N)
    button2 = ttk.Button(win, text="OK", command=lambda:[w_name_get(), create_database(), complete(), win.destroy(), pwin.destroy()])
    button2.pack(anchor=tk.N)

# Wチェック者氏名の入力内容を取得して変数定義する関数
def w_name_get():
    global Wcheck_name
    Wcheck_name = wentry_name.get()

# チェックが完了したことを表示する画面
def complete():
    win = tk.Toplevel() #Toplevel=別ウインドウ作成
    win.title("一般的衛生管理")
    win.geometry("300x200+550+250")
    label = ttk.Label(win, text="\nチェック完了\n\nデータベースへの保存完了\n")
    label.pack(anchor=tk.N)
    button = ttk.Button(win, text="OK", command=lambda:[win.destroy(), exit(root)])
    button.pack(anchor=tk.N)

# create_database関数内、DataFrame用に結果を格納する関数
def ok1():
    global n1
    n1 = "良"
def ng1():
    global n1
    n1 = "否"
def ok3_1():
    global n3_1
    n3_1 = "良"
def ng3_1():
    global n3_1
    n3_1 = "否"
def ok3_2():
    global n3_2
    n3_2 = "良"
def ng3_2():
    global n3_2
    n3_2 = "否"
def ok3_3():
    global n3_3
    n3_3 = "良"
def ng3_3():
    global n3_3
    n3_3 = "否"
def ok4_1():
    global n4_1
    n4_1 = "良"
def ng4_1():
    global n4_1
    n4_1 = "否"
def ok4_2():
    global n4_2
    n4_2 = "良"
def ng4_2():
    global n4_2
    n4_2 = "否"

# 時間の変数
now = datetime.datetime.now()
ym = now.strftime("%Y_%m")
date = now.strftime("%Y/%m/%d")
time1 = now.strftime("%H:%M:%S")

# DB作成関数
# 日付を遡ってチェックする場合f"{ymd}"を"yyyy/mm/dd"に変更
def create_database():
    df = pd.DataFrame([[f"{date}" ,f"{time1}", f"{n1}" ,f"{fr_temp},{fz_temp}", f"{n3_1}", f"{n3_2}", f"{n3_3}", f"{n4_1}", f"{n4_2}", f"{check_name}", f"{memo}", f"{Wcheck_name}"]],
                    columns = ["実施日", "実施時間", "①原材料の受入確認", "②庫内温度の確認(冷蔵庫, 冷凍庫)(℃)", "③-1交差汚染・二時汚染の防止", "③-2器具等の洗浄・消毒・殺菌", "③-3トイレの洗浄・消毒", "④-1従業員の健康管理等", "④-2手洗いの実施", "日々チェック(一般)", "特記事項(一般)", "確認者(一般)"]
                    )
    #df.drop("Unnamed: 0", axis=1)
    database = "HACCP.db"
    conn = sqlite3.connect(database)
    df.to_sql(f"{ym}", conn, if_exists="append", index=False)
    conn.close()
        
# rootフレームの設定
root = tk.Tk()
root.title("HACCP 衛生管理システム")
root.geometry("400x380+500+200")

frame = tk.Frame(root, width=300, height=300)
frame.pack(side=tk.TOP)

# 時計の関数定義
def time():
    clock = strftime("\n%Y/%m/%d %H:%M:%S\n")
    label1.config(text=clock)
    label1.after(1000, time)

# TOP画面の設定
label1 = tk.Label(frame)
time()
button1 = tk.Button(frame, text="チェックを開始", command=accept)
label3 = tk.Label(frame, text="\n<<< 一般衛生管理 >>>\n", justify="center")
label4 = tk.Label(frame, text="■①原材料の受入確認\n\n■②庫内温度の確認\n\n■③-1交差汚染・二時汚染の防止\n\n■③-2器具等の洗浄・消毒・殺菌\n\n■③-3トイレの洗浄・消毒\n\n■④-1従業員の健康管理等\n\n■④-2手洗いの実施\n\n", justify="left")

label1.pack(anchor=tk.N)
button1.pack(anchor=tk.N)
label3.pack(anchor=tk.N)
label4.pack(anchor=tk.W)

root.mainloop()
