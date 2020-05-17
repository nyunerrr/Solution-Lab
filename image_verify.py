def image_verify(path):

    import base58
    import ecdsa
    import filelock
    import hashlib
    import json
    import io
    import tkinter as tk
    from tkinter import messagebox as mbox
    from tkinter import filedialog
    from PIL import Image

    image_list = []

    im = Image.open(path)
    with io.BytesIO() as output:
        im.save(output, format="PNG")
        image = output.getvalue()

    with filelock.FileLock('block.lock', timeout=10):
        with open('block.txt', 'r') as file:
            block = json.load(file)

    height = len(block) - 1

    for im in range(0,height):
        image_list = block[im]['image']

    for im in image_list:
        pub_key = bytes.fromhex(im['in'])
        image_hs = bytes.fromhex(im['image hash'])
        image_sig = bytes.fromhex(im['sig'])
        time = im['time']

        hs_i = hashlib.sha256(image).hexdigest().encode('ascii')

        if(image_hs == hs_i):
            s = "Proof of Image Existence : True | time:" + time
            result = s
            return result
            break

    result = "Proof of Image Existance : False. \nNo such data exists."
    return result

if __name__ == '__main__':
    image_verify(path)
