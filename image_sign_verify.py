def image_sign_verify(hs_image):

    import hashlib
    import filelock
    import base58
    import ecdsa
    import json
    import itertools

    image_list = []
    result = []
    count = 0

    with filelock.FileLock('block.lock', timeout=10):
        with open('block.txt', 'r') as file:
            block = json.load(file)

    image_block_list = [0]*len(block)

    for i in range(0,len(block)):
        image_block_list[i] = block[i]['image']

    image_list = list(itertools.chain.from_iterable(image_block_list))

    for im in image_list:
        image_hs = bytes.fromhex(im['image hash'])
        if(hs_image == image_hs.hex()):
            pub_key = bytes.fromhex(im['in'])
            image_sig = bytes.fromhex(im['sig'])

            sha = hashlib.sha256()
            sha.update(pub_key)
            sha.update(image_hs)
            hash=sha.digest()

            key = ecdsa.VerifyingKey.from_string(pub_key,curve=ecdsa.SECP256k1)
            s = key.verify(image_sig, hash)
            result = "Hash: %s \n Signature verification: %s" % (hs_image,s)
            return result
        else:
            count += 1
            continue

    if(count==len(image_list)):
        s = "No such data exists"
        return s

if __name__ == '__main__':
    image_sign_verify(hs_image)
