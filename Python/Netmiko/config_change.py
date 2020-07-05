#!/usr/bin/env python
from netmiko import Netmiko

#  set device dictionary to pass to net_connect
Router1 = {
    "host": "192.168.10.240",
    "username": "admin",
    "password": "admin",
    "device_type": "cisco_ios",
}

Router2 = {
    "host": "192.168.10.203",
    "username": "admin",
    "password": "admin",
    "device_type": "cisco_ios",
}

# set list of commands to pass to net_command.send_config_set
commands_Router1 = [
    "interface g0/0",
    "desc This has changed",
]

commands_Router2 = [
    "interface g0/1",
    "desc This has changed too",
]

#  ssh to device, pass in dictionary to net_connect
net_connect = Netmiko(**Router1)

print("\nRunning commands to S1...\n\n" + net_connect.find_prompt())
output = net_connect.send_config_set(commands_Router1)
output = net_connect.save_config
print(output)
print("\n\n")
output = net_connect.send_command("show int des")
print(output)
print("\n\nCommands to Router1 complete")
net_connect.disconnect()

net_connect = Netmiko(**Router2)

print("\nRunning commands to R1...\n\n" + net_connect.find_prompt())
output = net_connect.send_config_set(commands_Router2)
output = net_connect.save_config()
print(output)
output = net_connect.send_command("show int des")
print(output)
print("\n\nCommands to Router2 complete")
