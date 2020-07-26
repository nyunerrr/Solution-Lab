def verify_remittance():
    import ecdsa
    import filelock
    import hashlib
    import json

    with filelock.FileLock('trans.lock', timeout=10):
        with open('trans.txt', 'r') as file:
            tx_list = json.load(file)

    result = []

    for tx in tx_list:
            tx_in = bytes.fromhex(tx['in'])
            tx_out = bytes.fromhex(tx['out'])
            tx_sig = bytes.fromhex(tx['sig'])

            sha = hashlib.sha256()
            sha.update(tx_in)
            sha.update(tx_out)
            hash=sha.digest()

            key = ecdsa.VerifyingKey.from_string(tx_in, curve=ecdsa.SECP256k1)
            #print('verify:', key.verify(tx_sig, hash))
            result.append(key.verify(tx_sig, hash))

    if(len(result)==0):
        result = "-"
        s = "No transactions made"
        return s
    else:
        t = len(result)
        s = "transactions made"
        turn = "%d %s | verification: %s" % (t,s,result)
        return turn

if __name__ == '__main__':
    verify()
