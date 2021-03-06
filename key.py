def key():
    import base58
    import ecdsa
    import filelock
    import json

    private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    public_key = private_key.get_verifying_key()

    private_key = private_key.to_string()
    public_key = public_key.to_string()

    private_b58 = base58.b58encode(private_key).decode('ascii')
    public_b58 = base58.b58encode(public_key).decode('ascii')

    with filelock.FileLock('key.lock', timeout=10):
        try:
            with open('key.txt', 'r') as file:
                key_list = json.load(file)
        except:
            key_list = []

        key_list.append({
            'private': private_b58,
            'public' : public_b58
        })

        with open('key.txt', 'w') as file:
            json.dump(key_list, file, indent=2)

    #text = "秘密鍵:{}\n公開鍵:{}"

    #keys = text.format(private_b58,public_b58)

    return private_b58,public_b58

if __name__ == '__main__':
    key()
