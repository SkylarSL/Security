import nacl
import requests
import base64
import nacl.hash
import nacl.encoding
import nacl.secret
from nacl.public import PrivateKey, Box, PublicKey

# create fingerprint to share with others, shold not be too encrypted
HASHER = nacl.hash.blake2b
url = "https://hash-browns.cs.uwaterloo.ca/api/pke/get-key"
payload = {
    "Accept" : "application/json",
    "Content-Type" : "application/json",
    "api_token" : "9b687d169f5fd5efe4f7ae96a752e0a6f8baaf70390cf558acd9b52681f20313",
    "user" : "Scholar"
}
req = requests.post(url, data = payload)
print(req, req.json())
scholarpkey = base64.b64decode(req.json()["public_key"])
print("public key: ", scholarpkey)
hash = HASHER(scholarpkey, encoder = nacl.encoding.HexEncoder)
print("hash: ", hash)

# share the public key
skey = PrivateKey.generate()
pkey = skey.public_key
epkey = pkey.encode(encoder = nacl.encoding.Base64Encoder)
url = "https://hash-browns.cs.uwaterloo.ca/api/pke/set-key"
payload = {
    "Accept" : "application/json",
    "Content-Type" : "application/json",
    "api_token" : "9b687d169f5fd5efe4f7ae96a752e0a6f8baaf70390cf558acd9b52681f20313",
    "public_key" : epkey
}
req = requests.post(url, data = payload)
print(req, req.json())

# send a message
msg = b"hello"
scholarpkey = PublicKey(scholarpkey)
box = Box(skey, scholarpkey)
nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
emsg = base64.b64encode(box.encrypt(msg, nonce))
url = "https://hash-browns.cs.uwaterloo.ca/api/pke/send"
payload = {
    "Accept" : "application/json",
    "Content-Type" : "application/json",
    "api_token" : "9b687d169f5fd5efe4f7ae96a752e0a6f8baaf70390cf558acd9b52681f20313",
    "to" : "Scholar",
    "message" : emsg
}
req = requests.post(url, data = payload)
print(req, req.json())

# recieve a message
msg = b"hello"
url = "https://hash-browns.cs.uwaterloo.ca/api/pke/inbox"
payload = {
    "Accept" : "application/json",
    "Content-Type" : "application/json",
    "api_token" : "9b687d169f5fd5efe4f7ae96a752e0a6f8baaf70390cf558acd9b52681f20313",
}
req = requests.post(url, data = payload)
print(req, req.json())
emsg = req.json()[0]["message"]
print(emsg)
msg = base64.b64decode(emsg)
msg = box.decrypt(msg)
print(msg)