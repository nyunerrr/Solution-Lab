def image_register_GUI():

    import re, os
    import tkinter as tk
    import tkinter.ttk as ttk
    import tkinter.filedialog as tkfd
    import io
    import hashlib
    from PIL import Image, ImageFilter
    from tkinter import messagebox as mbox
    from tkinter import filedialog

    import image_register

    win = tk.Tk()
    win.title("画像登録")
    win.geometry("800x500")

    path = ''

    def imagepath():
        global path
        ftype = [('テキストファイル','*.png')]
        dir = 'C:\\pg'
        path = filedialog.askopenfilename(filetypes = ftype, initialdir = dir)
        label_path['text'] = path

    def image():
        global path
        pub_key = text_pub.get()
        pri_key = text_pri.get()
        hs = image_register.image_register(path,pub_key,pri_key)
        mbox.showinfo('ハッシュ値',hs)

    #画像選択ボタン
    image_register_Button = tk.Button(win, text=u'画像選択', width=50)
    image_register_Button["command"] = imagepath
    image_register_Button.pack()

    #パス表示ラベル
    label_path = tk.Label(win, text=u'----')
    label_path.pack()

    #公開鍵入力
    label_pub = tk.Label(win, text=u'自分の公開鍵')
    label_pub.pack()
    text_pub = tk.Entry(win)
    text_pub.insert(tk.END, '公開鍵')
    text_pub.pack()

    #秘密鍵入力
    label_pri = tk.Label(win, text=u'自分の秘密鍵')
    label_pub.pack()
    text_pri = tk.Entry(win)
    text_pri.insert(tk.END, '秘密鍵')
    text_pri.pack()

    image_hash_Button = tk.Button(win, text=u'登録', width=50)
    image_hash_Button["command"] = image
    image_hash_Button.pack()

    win.mainloop()

if __name__ == '__main__':
    image_regiater_GUI()

def mining_GUI():
    import tkinter as tk
    from tkinter import messagebox as mbox
    import mining

    def mine():
        p_key = text_pub.get()
        nonce = mining.mining(p_key)
        mbox.showinfo('nonce:',nonce)

    win = tk.Tk()
    win.title("マイニング")
    win.geometry("800x500")

    label_pub = tk.Label(win, text=u'自分の公開鍵')
    label_pub.pack()

    text_pub = tk.Entry(win)
    text_pub.insert(tk.END, '公開鍵')
    text_pub.pack()

    mine_Button = tk.Button(win, text=u'マイニング実行')
    mine_Button['command'] = mine
    mine_Button.pack()

    win.mainloop()

if __name__ == '__main__':
    mining_GUI()

def remittance_GUI():
    import tkinter as tk
    from tkinter import messagebox as mbox
    import remittance

    win = tk.Tk()
    win.title("送金")
    win.geometry("800x500")

    def send():
        tx_in = text_in.get()
        tx_key = text_key.get()
        tx_out = text_out.get()
        result = remittance.remittance(tx_key,tx_in,tx_out)
        mbox.showinfo("result",result)

    label_pub = tk.Label(win, text=u'自分の公開鍵')
    label_pub.pack()

    text_in = tk.Entry(win)
    text_in.insert(tk.END, '自分の公開鍵')
    text_in.pack()

    label_pri = tk.Label(win, text=u'自分の秘密鍵')
    label_pri.pack()

    text_key = tk.Entry(win)
    text_key.insert(tk.END, '自分の秘密鍵')
    text_key.pack()

    label_pri_y = tk.Label(win, text=u'相手の公開鍵')
    label_pri_y.pack()

    text_out = tk.Entry(win)
    text_out.insert(tk.END, '相手の公開鍵')
    text_out.pack()

    rem_Button = tk.Button(win, text=u'送金')
    rem_Button['command'] = send
    rem_Button.pack()

    win.mainloop()

if __name__ == '__main__':
    remittance_GUI()

def verify_image_GUI():
    import base58
    import io
    import tkinter as tk
    from tkinter import messagebox as mbox
    from tkinter import filedialog
    from PIL import Image

    import image_verify

    win = tk.Tk()
    win.title("画像登録")
    win.geometry("800x500")

    path = ''

    def imagepath():
        global path
        ftype = [('テキストファイル','*.png')]
        dir = 'C:\\pg'
        path = filedialog.askopenfilename(filetypes = ftype, initialdir = dir)
        label_path['text'] = path

    def im_verify():
        global path
        result = image_verify.image_verify(path)
        mbox.showinfo('認証結果',result)

    #画像選択ボタン
    image_register_Button = tk.Button(win, text=u'画像選択', width=50)
    image_register_Button["command"] = imagepath
    image_register_Button.pack()

    #パス表示ラベル
    label_path = tk.Label(win, text=u'----')
    label_path.pack()

    image_hash_Button = tk.Button(win, text=u'認証', width=50)
    image_hash_Button["command"] = im_verify
    image_hash_Button.pack()

    win.mainloop()

if __name__ == '__main__':
    verify_image_GUI()

def verify_remittance_GUI():

    import tkinter as tk
    import verify_remittance
    from tkinter import messagebox as mbox

    result = []

    def verify():
        s = verify_remittance.verify_remittance()
        mbox.showinfo('result',s)

    win = tk.Tk()
    win.title("BlockChain GUI")
    win.geometry("200x500")

    veri_Button = tk.Button(win, text=u'認証')
    veri_Button['command'] = verify
    veri_Button.pack()

    win.mainloop()

if __name__ == '__main__':
    verify_remittance_GUI()

def image_sign_verify_GUI():
    import re, os
    import tkinter as tk
    import tkinter.ttk as ttk
    import tkinter.filedialog as tkfd
    import io
    import hashlib
    import filelock
    from PIL import Image, ImageFilter
    from tkinter import messagebox as mbox
    from tkinter import filedialog


    import image_sign_verify

    win = tk.Tk()
    win.title("画像登録")
    win.geometry("800x500")

    path = ''

    def imagepath():
        global path
        ftype = [('テキストファイル','*.png')]
        dir = 'C:\\pg'
        path = filedialog.askopenfilename(filetypes = ftype, initialdir = dir)
        label_path['text'] = path


    def sign_verify():
        global path
        im_ = Image.open(path)
        with io.BytesIO() as output:
            im_.save(output, format="PNG")
            image = output.getvalue()
        hs_i = hashlib.sha256(image).hexdigest().encode('ascii')
        hs_image = hs_i.hex()

        result = image_sign_verify.image_sign_verify(hs_image)
        mbox.showinfo('result',result)


    #画像選択ボタン
    image_register_Button = tk.Button(win, text=u'画像選択', width=50)
    image_register_Button["command"] = imagepath
    image_register_Button.pack()

    #パス表示ラベル
    label_path = tk.Label(win, text=u'----')
    label_path.pack()


    image_hash_Button = tk.Button(win, text=u'署名の検証', width=50)
    image_hash_Button["command"] = sign_verify
    image_hash_Button.pack()

    win.mainloop()

if __name__ == '__main__':
    image_sign_verify_GUI()
