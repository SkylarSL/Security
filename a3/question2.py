import requests
import base64
import nacl.secret
import nacl.utils

url = "https://hash-browns.cs.uwaterloo.ca/api/psk/send"
msg = "hello"
msg = msg.encode("utf-8")
key = "735d423379357df8f3f5887499c60f2ca44f055c1a03772f03884cc22f73cfb0"
key = bytes.fromhex(key)
nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
box = nacl.secret.SecretBox(key)
encrypted = box.encrypt(msg, nonce)
emsg = base64.b64encode(encrypted)
payload = {
    "Accept" : "application/json",
    "Content-Type" : "application/json",
    "api_token" : "9b687d169f5fd5efe4f7ae96a752e0a6f8baaf70390cf558acd9b52681f20313",
    "to" : "Scholar",
    "message" : emsg
}
req = requests.post(url = url, data = payload)

url = "https://hash-browns.cs.uwaterloo.ca/api/psk/inbox"
payload = {
    "Accept" : "application/json",
    "Content-Type" : "application/json",
    "api_token" : "9b687d169f5fd5efe4f7ae96a752e0a6f8baaf70390cf558acd9b52681f20313"
}
req = requests.post(url, data = payload)
#print(req.json())
msg = req.json()[0]["message"]
msg = base64.b64decode(msg)
print(msg)
msg = box.decrypt(msg)
print(msg.decode("utf-8"))
