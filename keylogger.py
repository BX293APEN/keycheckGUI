import tkinter
import tkinter.scrolledtext as scrolledtext
import tkinter.messagebox as messagebox
from tkinter import colorchooser
import subprocess, threading, sys
import pyautogui
from pynput import keyboard
from pystray import MenuItem, Icon
from PIL import Image

def cmd(command):
    subprocess.Popen(command, shell=True)

def tray_thread():
    global icon
    icon.run()

def closewindow():
    global icon
    statusbar["text"] = "確認"
    msgvalue = messagebox.askquestion( "確認", "終了しますか？")
    if msgvalue == "yes":
        icon.stop()
        body.destroy()
        sys.exit()
        
    else:
        statusbar["text"] = "続行"

def bgc():
    color = colorchooser.askcolor()
    body.configure(background = color[1])
    langLabel.configure(background = color[1])
    statusbar["text"] = "背景色を変更しました"
    
def ccolor():
    color = colorchooser.askcolor()
    langLabel.configure(foreground = color[1])
    textarea.configure(foreground = color[1])
    statusbar["text"] = "文字色を変更しました"
    
def remove_log():
    if button_run["text"] == "ログの削除":
        textarea.configure(state='normal')
        textarea.delete("1.0","end")
        textarea.configure(state='disabled')
        statusbar["text"] = "ログの削除完了"
        button_run["text"] = "ログの開始"
    elif button_run["text"] == "ログの開始":
        statusbar["text"] = "ログを開始しました"
        button_run["text"] = "ログの停止"
    elif button_run["text"] == "ログの停止":
        statusbar["text"] = "ログを停止しました"
        button_run["text"] = "ログの削除"

def right_click_menu(event):
    #右クリック設定
    name = str(event.widget.extra)
    right_menu = tkinter.Menu(eval(name), tearoff=0, font=("HGPｺﾞｼｯｸE", 15))
    right_menu.add_command(label="コピー",command = lambda:copytxt(name))
    right_menu.post(event.x_root, event.y_root)

def copytxt(wname):
    try:
        eval(wname).clipboard_clear()
        cptxt = eval(wname).get(tkinter.SEL_FIRST, tkinter.SEL_LAST)
        eval(wname).clipboard_append(cptxt)
        statusbar["text"] = cptxt  + " をコピー"
    except:
        statusbar["text"] = "コピー出来ませんでした"
        eval(wname).clipboard_clear()
    
def keyfunc(data):
    sc = open('keysc.ini','r',encoding="utf-8_sig")
    scdata = sc.read()
    sc.close()
    scsep = scdata.split("\n")

    defsc = open('defaultkey','r',encoding="utf-8_sig")
    defscdata = defsc.read()
    defsc.close()
    defscsep = defscdata.split("\n")

    i = 0
    for d in scsep:
        if d.count("=") > 0:
            if data.count(d.split("=")[0]) > 0:
                for k in defscsep:
                    if k.count("=") > 0:
                        if d.split("=")[1] == k.split("==")[0]:
                            exec(k.split("==")[1])
                            i = 1
                            break
                if i != 1:
                    cmd(d.split("=")[1])
                break

class keylog:
    def __init__(self, txtarea, txtbox, button):
        self.txtarea = txtarea
        self.txtbox = txtbox
        self.button = button
        listener = keyboard.Listener(on_press = self.on_press,on_release = self.on_release)
        listener.start()
        
    def on_press(self, key):
        try:
            if(str(key).count("'") > 0 ):
                stkey = str(key).split("'")[1]
                self.log(stkey+",")
            else:
                stkey = str(key)
                self.log(stkey+",")
            
            if self.button["text"] == "ログの停止":
                textarea.configure(state='normal')
                self.txtarea.insert('end', stkey+",")
                self.txtarea.see("end")
                textarea.configure(state='disabled')
            
        except AttributeError:
            if(str(key).count("'") > 0 ):
                stkey = str(key).split("'")[1]
            else:
                stkey = str(key)
            
    def on_release(self, key):
        data = self.log("read")
        th2= threading.Thread(target=keyfunc, args=(data,))
        th2.start()
        self.log("reset")
                    
    def log(self, cmd):
        if cmd == "reset":
            self.txtbox.configure(state="normal")
            self.txtbox.delete(0, tkinter.END)
            self.txtbox.configure(state='disabled')
        elif cmd == "read":
            logdata =  self.txtbox.get()
            return logdata
        else:
            self.txtbox.configure(state="normal")
            self.txtbox.insert(tkinter.END, str(cmd))
            self.txtbox.configure(state='disabled')

if __name__ == "__main__":
    #ウィンドウ設定
    body = tkinter.Tk()
    body.title(u"Key Logger (made by PEN)") # ウィンドウタイトル
    body.geometry("900x600") # ウィンドウサイズ
    body.configure(background = 'white')
    body.resizable(0,0) # リサイズ禁止
    body.iconbitmap("icon.ico")
    body.withdraw()
    
    #メニューボタン
    menu_bar = tkinter.Menu(body)
    body.config(menu = menu_bar)
    menu_file = tkinter.Menu(menu_bar, tearoff=0, font=("HGPｺﾞｼｯｸE", "10"))
    menu_file.add_cascade(label='閉じる', command=closewindow)
    
    menu_edit = tkinter.Menu(menu_bar, tearoff=0, font=("HGPｺﾞｼｯｸE", "10"))
    menu_edit.add_cascade(label='ショートカットの設定', command=lambda:cmd("notepad keysc.ini"))
    menu_edit.add_cascade(label='特殊キーの設定', command=lambda:cmd("notepad defaultkey"))
    
    menu_settings = tkinter.Menu(menu_bar, tearoff=0, font=("HGPｺﾞｼｯｸE", "10"))
    menu_settings.add_cascade(label='背景色の変更', command=bgc)
    menu_settings.add_cascade(label='文字色の変更', command=ccolor)
    
    menu_bar.add_cascade(label='ファイル', menu = menu_file) 
    menu_bar.add_cascade(label='設定', menu = menu_settings)
    menu_bar.add_cascade(label='編集', menu = menu_edit)
    
    #ボタン
    button_run = tkinter.Button(body, text = "ログの開始", command = remove_log , font=("HGPｺﾞｼｯｸE", "13"))
    button_run.pack(padx=10,pady = 10, anchor=tkinter.SE, expand=True, ipadx=30)
    
    #テキストボックス
    textbox1 = tkinter.Entry(body, width = 20 , font=("HGPｺﾞｼｯｸE", "15"),relief = tkinter.SOLID)
    textbox1.configure(state='disabled')
    textbox1.extra = "textbox1" # extraで変数名を登録
    textbox1.place(x = 200, y = 10)
    
    textarea = scrolledtext.ScrolledText(body, font=("HGPｺﾞｼｯｸE", 15), height=12, width=50)
    textarea.extra = "textarea" # extraで変数名を登録
    textarea.place(x = 10, y = 90)
    textarea.configure(state='disabled')
    textarea.bind("<Button-3>", right_click_menu)#右クリックが押されたら

    #テキスト表示
    langLabel = tkinter.Label(body, text='押されたキー:', font=("HGPｺﾞｼｯｸE", "15"),background='#ffffff')
    langLabel.place(x = 10, y = 10)
    
    #ステータスバー
    statusbar = tkinter.Label(body, text = "起動しました", bd = 1, relief = tkinter.SUNKEN, anchor = tkinter.W)
    statusbar.pack(side = tkinter.BOTTOM, fill = tkinter.X)
    
    # バックグラウンド処理
    th1 = threading.Thread(target=keylog, args=(textarea, textbox1,button_run))
    th1.start()
    
    # システムトレイへ表示
    global icon
    image = Image.open("icon.ico")
    menu = (MenuItem('表示', body.deiconify, default=True), MenuItem('ショートカットの設定', lambda:cmd("notepad keysc.ini")))
    icon=Icon(name ="Key Logger", icon = image, title ="Key Logger", menu =menu)
    tray_th = threading.Thread(target=tray_thread)
    tray_th.start()
    
    body.protocol("WM_DELETE_WINDOW", body.withdraw)
    body.mainloop() # ずっと表示させる