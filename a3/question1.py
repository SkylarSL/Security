import requests
import base64

r = requests.get('https://xkcd.com/1906/')
print(r)
print("ASDF")

url = "https://hash-browns.cs.uwaterloo.ca/api/plain/send"
msg = "hello"
emsg = base64.b64encode(msg.encode("utf-8"))
payload = {
    "Accept" : "application/json",
    "Content-Type" : "application/json",
    "api_token": "9b687d169f5fd5efe4f7ae96a752e0a6f8baaf70390cf558acd9b52681f20313",
    "to" : "Scholar",
    "message" : emsg
}
req = requests.post(
    url,
    data = payload
)
print("Sending msg to Scholar: ", req)

url = "https://hash-browns.cs.uwaterloo.ca/api/plain/inbox"
payload = {
    "Accept" : "application/json",
    "Content-Type" : "application/json",
    "api_token" : "9b687d169f5fd5efe4f7ae96a752e0a6f8baaf70390cf558acd9b52681f20313"
}
req = requests.post(
    url,
    data = payload
)
#print(req.json()[0])
escholarMsg = base64.b64decode(req.json()[0]["message"])
scholarMsg = escholarMsg.decode("utf-8")
print(scholarMsg)


