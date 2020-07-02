import requests, json

# POST Token for auth
url = "https://sandboxdnac.cisco.com/dna/system/api/v1/auth/token"

user = 'devnetuser'
pw = 'Cisco123!'

response = requests.post(url, auth=(user, pw)).json()

token = response['Token']

# GET information
url = "https://sandboxdnac.cisco.com/dna/intent/api/v1/network-device"

payload = {}
headers = {
  'X-Auth-Token': token,
  'Accept': 'application/json'
}

response = requests.get(url, headers=headers).json()

for device in range(len(response['response'])):
  print("-" * 50)
  print("HOSTNAME: " + str(response['response'][device]['hostname']))
  print("Type: " + str(response['response'][device]['type']))
  print("MAC: " + str(response['response'][device]['macAddress']))
  print("Serial: " + str(response['response'][device]['serialNumber']))
  print("Management IP: " + str(response['response'][device]['managementIpAddress']))
  print("Up Time: " + str(response['response'][device]['upTime']))