def image_register(path,public_key,private_key):
    import base58
    import ecdsa
    import filelock
    import hashlib
    import json
    import io
    import datetime

    from tkinter import messagebox as mess
    from PIL import Image, ImageFilter
    from tkinter import messagebox as mbox
    from tkinter import filedialog

    time = datetime.datetime.now()
    time = time.strftime('%Y/%m/%d %H:%M:%S')

    #ファイルのハッシュ値計算
    im = Image.open(path)
    with io.BytesIO() as output:
        im.save(output, format="PNG")
        image = output.getvalue()

    pub_key = base58.b58decode(public_key)
    pri_key = base58.b58decode(private_key)

    hs_i = hashlib.sha256(image).hexdigest().encode('ascii')
    print(hs_i)

    sha = hashlib.sha256()
    sha.update(pub_key)
    sha.update(hs_i)
    hs = sha.digest()

    key = ecdsa.SigningKey.from_string(pri_key, curve=ecdsa.SECP256k1)
    sig = key.sign(hs)
    print(type(hs_i))

    with filelock.FileLock('image.lock', timeout=10):
        try:
            with open('image.txt', 'r') as file:
                tx_list = json.load(file)
        except:
                tx_list = []

        tx_list.append({
        'time': time,
        'in': pub_key.hex(),
        'image hash': hs_i.hex(),
        'sig': sig.hex()
        })

    with open('image.txt', 'w') as file:
        json.dump(tx_list, file, indent=2)

    return hs_i

if __name__ == '__main__':
    image_register(path,pub_key,pri_key)
