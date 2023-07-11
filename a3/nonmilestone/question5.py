import nacl
import requests
import base64
import nacl.hash
import nacl.encoding
import nacl.secret
import nacl.bindings

#generate public and secret key and share public key
myPublicKey, mySecretKey = nacl.bindings.crypto_kx_keypair()
print("secret: ", mySecretKey, "public: ", myPublicKey)
myEncodedPublicKey = base64.b64encode(myPublicKey)
url = "https://hash-browns.cs.uwaterloo.ca/api/keyex/set-key"
payload = {
    "Accept" : "application/json",
    "Content-Type" : "application/json",
    "api_token" : "9b687d169f5fd5efe4f7ae96a752e0a6f8baaf70390cf558acd9b52681f20313",
    "public_key" : myEncodedPublicKey
}
req = requests.post(url, data = payload)
print(req, req.json())

#get the public key Scholar has
url = "https://hash-browns.cs.uwaterloo.ca/api/keyex/get-key"
payload = {
    "Accept" : "application/json",
    "Content-Type" : "application/json",
    "api_token" : "9b687d169f5fd5efe4f7ae96a752e0a6f8baaf70390cf558acd9b52681f20313",
    "user" : "Scholar"
}
req = requests.post(url, data = payload)
print(req, req.json())
scholarPublicKey = req.json()["public_key"]
decodedScholarPublicKey = base64.b64decode(scholarPublicKey)
print("scholar public key: ", decodedScholarPublicKey)

#get the message from inbox
url = "https://hash-browns.cs.uwaterloo.ca/api/keyex/inbox"
payload = {
    "Accept" : "application/json",
    "Content-Type" : "application/json",
    "api_token" : "9b687d169f5fd5efe4f7ae96a752e0a6f8baaf70390cf558acd9b52681f20313",
}
req = requests.post(url, data = payload)
print(req, req.json())
msg = req.json()[0]["message"]
scholarMsg = base64.b64decode(msg)
print("scholar message: ", scholarMsg)

#decrypt message using generate shared key
inputDecrypt, outputEncrypt = nacl.bindings.crypto_kx_client_session_keys(
    myPublicKey,
    mySecretKey,
    decodedScholarPublicKey,
)
print("decrypt: ", inputDecrypt, "\nencrypt: ", outputEncrypt)
box = nacl.secret.SecretBox(inputDecrypt)
scholarMsg = box.decrypt(scholarMsg)
print(scholarMsg)