import requests

url = "https://sandboxsdwan.cisco.com:8443/j_security_check"

payload = "j_username=devnetuser&j_password=Cisco123%21"
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": "JSESSIONID=gAtTbW5sKBxydWfiTxPsyY9iiXZVzsHwR5hN3Vhh.4854266f-a8ad-4068-9651-d4e834384f51",
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text.encode("utf8"))