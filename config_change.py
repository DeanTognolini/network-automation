#!/usr/bin/env python
from netmiko import Netmiko

#  set device dictionary to pass to net_connect
iosv_l2_s1 = {
    "host": "10.1.1.1",
    "username": "admin",
    "password": "admin",
    "device_type": "cisco_ios",
}

# set list of commands to pass to net_command.send_config_set
commands = ["interface g0/0",
   "desc TEST",
]

#  ssh to device, pass in dictionary to net_connect
net_connect = Netmiko(**iosv_l2_s1)


print("")
# verify connection, will return "S1#"
print(net_connect.find_prompt())
# send list of commands from "commands"
output = net_connect.send_config_set(commands)
output = net_connect.save_config()
print(output)
print("")
output = net_connect.send_command("show run interface g0/0")
print(output)
print("")

