import requests

url = "https://ios-xe-mgmt-latest.cisco.com:9443/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces"

user = 'root'
pw = 'D_Vay!_10&'

payload = {}
headers = {
  'Accept': 'application/yang-data+json',
  'Content-Type': 'application/yang-data+json'
}

response = requests.request("GET", url, headers=headers, data = payload)

print(response.text.encode('utf8'))