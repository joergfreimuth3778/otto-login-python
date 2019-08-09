import requests
from Cryptodome import Random
from Cryptodome.Cipher import PKCS1_v1_5
from Cryptodome.Hash import SHA
from Cryptodome.PublicKey import RSA

from otto_login import settings


def login():
    login_params = get_login_params()
    print(crypt(login_params, '123456'))


def get_login_params():
    url = f'{settings.firewall_url}/RSASettings'
    return requests.get(url, verify=False).json()


def crypt(login_params, password):

    # public_key = key.publickey().exportKey('PEM')
    # message = input('plain text for RSA encryption and decryption:')
    # message = str.encode(message)
    #
    # rsa_public_key = RSA.importKey(public_key)
    # rsa_public_key = PKCS1_v1_5.new(rsa_public_key)
    #
    # return rsa_public_key.encrypt(message)
    # key = RSA.generate(2048)
    # message = f"{login_params['loginToken']}{password}"
    # keystream = StringIO(str(key.publickey().export_key('PEM')))
    # pubkey = RSA.importKey(keystream.read())
    # h = SHA.new(message)
    #
    # cipher = PKCS1_v1_5.new(pubkey)
    #
    # return base64.encodebytes(cipher.encrypt(message+h.digest()))
    message = input(f"{login_params['loginToken']}{password}")
    message = str.encode(message)

    h = SHA.new(message)
    key = RSA.generate(1024, Random.get_random_bytes)
    cipher = PKCS1_v1_5.new(key)

    return cipher.encrypt(message+h.digest()).hex()
