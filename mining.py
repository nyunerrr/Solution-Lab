def  mining(pub_key):
    import base58
    import ecdsa
    import filelock
    import hashlib
    import json
    import re
    import sys
    import datetime
    import time

    #難易度の設定
    DIFFICULTY = 3
    #引数(マイニング報酬を送付する公開鍵)の処理
    public_key = base58.b58decode(pub_key).hex()

    #ファイルオープン
    #過去のブロック
    with filelock.FileLock('block.lock', timeout=10):
        try:
            with open('block.txt', 'r') as file:
                block_list = json.load(file)
            previous_hash = block_list[-1]['hash']
        except:
            block_list = []
            previous_hash = ''

    #新規作成されたトランザクション
    with filelock.FileLock('trans.lock', timeout=10):
        try:
            with open('trans.txt', 'r') as file:
                tx_list = json.load(file)
        except:
            tx_list = []

    #登録したい画像データ
    with filelock.FileLock('image.lock', timeout=10):
        try:
            with open('image.txt', 'r') as file:
                image_list = json.load(file)
        except:
            image_list = []

    #環境データ
    with filelock.FileLock('data.lock', timeout=10):
        try:
            with open('data.txt', 'r') as file:
                envi_data_list = json.load(file)
        except:
            envi_data_list = []
    #print(envi_data_list[0])


    #ブロックに登録される全てのデータをハッシュする
    old_in = []
    old_out = []
    for block in block_list:
        for tx in block['tx']:
            old_in.append(tx['in'])
            old_out.append(tx['out'])

    sha = hashlib.sha256()
    for tx in tx_list:
        sha.update(bytes.fromhex(tx['in']))
        sha.update(bytes.fromhex(tx['out']))
        sha.update(bytes.fromhex(tx['sig']))

    for im in image_list:
        sha.update(bytes.fromhex(im['in']))
        sha.update(bytes.fromhex(im['image hash']))
        sha.update(bytes.fromhex(im['sig']))

    for da in envi_data_list:
        sha.update(da['humidity'].encode('utf-8'))
        sha.update(da['tempreture'].encode('utf-8'))
        sha.update(da['pressure'].encode('utf-8'))

    tx_hash = sha.digest()

    #マイニング処理
    for nonce in range(100000000):
        sha = hashlib.sha256()
        sha.update(bytes(nonce))
        sha.update(bytes.fromhex(previous_hash))
        sha.update(tx_hash)
        hash = sha.digest()

        if re.match(r'0{' + str(DIFFICULTY) + r'}', hash.hex()):
            break

    #現在時刻
    time = datetime.datetime.now()
    time_now = time.strftime('%Y/%m/%d %H:%M:%S')

    block_list.append({
        'hash' : hash.hex(),
        'time' : time_now,
        'nonce': nonce,
        'previous_hash': previous_hash,
        'tx_hash': tx_hash.hex(),
        'tx'   : tx_list,
        'image': image_list,
        'envi data': envi_data_list
    })

    with filelock.FileLock('block.lock', timeout=10):
        with open('block.txt', 'w') as file:
            json.dump(block_list, file, indent=2)


    with filelock.FileLock('trans.lock', timeout=10):
        try:
            with open('trans.txt', 'r') as file:
                file_tx_list = json.load(file)
        except:
            file_tx_list = []

        tx_list = []

        for tx in file_tx_list:
            if (tx['in'] not in old_in and
                tx['out'] not in old_in and tx['out'] not in old_out):
                tx_list.append(tx)

        with open('trans.txt', 'w') as file:
            json.dump(tx_list, file, indent=2)


    image_list = []

    with open('image.txt', 'w') as file:
            json.dump(image_list, file, indent=2)

    envi_data_list = []

    with open('data.txt', 'w') as file:
            json.dump(envi_data_list, file, indent=2)

    return nonce

if __name__ == '__main__':
    mining(pub_key)
