from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256


def generate_keys():
    keyPair = RSA.generate(bits=1024)
    public_key = keyPair.publickey().export_key()
    return keyPair, public_key


def sign(message, private_key):
    hash = SHA256.new(bytes(str(message), 'utf-8'))
    signer = PKCS115_SigScheme(private_key)
    signature = signer.sign(hash)
    return signature

def verify(message, signature, public_key_pem):
    public_key = RSA.import_key(public_key_pem)
    hash = SHA256.new(bytes(str(message), 'utf-8'))
    verifier = PKCS115_SigScheme(public_key)
    try:
        signature = verifier.verify(hash, signature)
        return True
    except:
        return False
