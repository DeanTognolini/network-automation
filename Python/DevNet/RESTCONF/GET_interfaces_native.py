import requests, json

# Define YANG Modules and Container (this is the DevNet always on IOS-XE Router)
url = "https://ios-xe-mgmt-latest.cisco.com:9443/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces"

# Credentials
user = "root"
pw = "D_Vay!_10&"

payload = {}
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json",
}

response = requests.request(
    "GET", url, auth=(user, pw), headers=headers, data=payload, verify=False).json()

print(json.dumps(response, indent=2))