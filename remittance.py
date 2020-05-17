def remittance(tx_key_,tx_in_,tx_out_):
    import base58
    import ecdsa
    import filelock
    import hashlib
    import json
    import sys
    import datetime


    #if len(sys.argv) != 4:
    #    print('usage:', sys.argv[0], 'in-private in-public out-public')
    #    exit()
    time = datetime.datetime.now()
    time = time.strftime('%Y/%m/%d %H:%M:%S')

    tx_key = base58.b58decode(tx_key_)
    tx_in  = base58.b58decode(tx_in_)
    tx_out = base58.b58decode(tx_out_)

    print(type(tx_key))
    #print('in  hex:', tx_in.hex())
    #print('out hex:', tx_out.hex())

    sha = hashlib.sha256()
    sha.update(tx_in)
    sha.update(tx_out)
    hash = sha.digest()

    #送金print('hash len:', len(hash))
    #print('hash hex:', hash.hex())

    key = ecdsa.SigningKey.from_string(tx_key, curve=ecdsa.SECP256k1)
    sig = key.sign(hash)

    #print('sig len:', len(sig))
    #print('sig hex:', sig.hex())

    with filelock.FileLock('trans.lock', timeout=10):
        try:
            with open('trans.txt', 'r') as file:
                tx_list = json.load(file)
        except:
            tx_list = []

        tx_list.append({
            'time': time,
            'in': tx_in.hex(),
            'out': tx_out.hex(),
            'sig': sig.hex()
        })

        with open('trans.txt', 'w') as file:
            json.dump(tx_list, file, indent=2)

    s = "Success"
    return s

if __name__ == '__main__':
    remittance(tx_key,tx_in,tx_out)
