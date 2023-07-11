import nacl
import requests
import base64
from nacl.encoding import Base64Encoder
from nacl.signing import SigningKey

signingKey = SigningKey.generate()
vkey = signingKey.verify_key
evkey = vkey.encode(encoder = Base64Encoder)
url = "https://hash-browns.cs.uwaterloo.ca/api/signed/set-key"
payload = {
    "Accept" : "application/json",
    "Content-Type" : "application/json",
    "api_token" : "9b687d169f5fd5efe4f7ae96a752e0a6f8baaf70390cf558acd9b52681f20313",
    "public_key" : evkey
}
req = requests.post(url, data = payload)
print(req)


url = "https://hash-browns.cs.uwaterloo.ca/api/signed/send"
msg = b"hello"
signed = signingKey.sign(msg)
e = base64.b64encode(signed)
payload = {
    "Accept" : "application/json",
    "Content-Type" : "application/json",
    "api_token" : "9b687d169f5fd5efe4f7ae96a752e0a6f8baaf70390cf558acd9b52681f20313",
    "to" : "Scholar",
    "message" : e
}
req = requests.post(url, data = payload)
print(req)
