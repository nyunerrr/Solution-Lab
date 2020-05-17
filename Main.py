#モジュールインポート
import tkinter as tk
from tkinter import messagebox as mbox

#自作モジュールのインポート
import GUI
import key
import wallet
import verify_remittance
import demon

f_path_list = [0]*2

#各関数の定義
# アドレス生成ボタン処理
def key_generate():
    keys = key.key()
    label_pri_Key['text'] = keys[0]
    label_pub_Key['text'] = keys[1]
    result = "秘密鍵:" + keys[0] + "\n" + "公開鍵:" + keys[1]
    mbox.showinfo('秘密鍵と公開鍵',result)

#送金画面生成
def remittance():
    GUI.remittance_GUI()

#マイニング画面生成
def mining():
    GUI.mining_GUI()

#残高表示
def balance():
    bal = wallet.balance()
    label_balance['text'] = bal

#画像登録画面生成
def image_register():
    GUI.image_register_GUI()

#取引認証画面生成
def verify_rem():
    result = verify_remittance.verify_remittance()
    mbox.showinfo('result',result)

#画像認証画面生成
def verify_image():
    GUI.verify_image_GUI()

def verify_image_sign_():
    GUI.image_sign_verify_GUI()

def p2p_background():
    win.destrpy()
    demon.demon()

#ウィンドウを作成
win = tk.Tk()
win.title("BlockChain GUI")
win.geometry("800x500")

#メニュー作成
menu = tk.Menu(win)
win.config(menu=menu)
menu_file = tk.Menu(win)
menu.add_cascade(label='操作', menu=menu_file)
menu_file.add_command(label='送金', command=remittance)
menu_file.add_command(label='マイニング',command=mining)
menu_file.add_command(label='画像登録',command=image_register)
menu_file.add_command(label='取引検証', command=verify_rem)
menu_file.add_command(label='画像認証', command=verify_image)
menu_file.add_command(label='画像署名検証', command=verify_image＿sign_)
menu_file.add_command(label='P2Pモード', command=p2p_background)

#アドレス生成画面
key_gen_Button = tk.Button(win, text=u'秘密鍵・公開鍵（アドレス）作成', width=50)
key_gen_Button["command"] = key_generate
key_gen_Button.place(x=10,y=100)
key_gen_Button.pack()

labelpub = tk.Label(win, text=u'公開鍵')
labelpub.pack()

label_pub_Key = tk.Label(win, text=u'----')
label_pub_Key.pack()

labelpri = tk.Label(win, text=u'秘密鍵')
labelpri.pack()

label_pri_Key = tk.Label(win, text=u'----')
label_pri_Key.pack()

balance_Button = tk.Button(win, text=u'残高表示')
balance_Button['command'] = balance
balance_Button.pack()

label_balance = tk.Label(win, text=u'----')
label_balance.pack()


#ウィンドウを動かす
win.mainloop()
