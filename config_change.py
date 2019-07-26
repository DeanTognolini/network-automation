#!/usr/bin/env python
from netmiko import Netmiko

#  set device dictionary to pass to net_connect
iosv_l2_s1 = {
    "host": "10.1.1.1",
    "username": "admin",
    "password": "admin",
    "device_type": "cisco_ios",
}

iosv_r1 = {
   "host": "10.1.1.254",
   "username": "admin",
   "password": "admin",
   "device_type": "cisco_ios",
}

# set list of commands to pass to net_command.send_config_set
commands_s1 = ["interface ra g0/0 - 3",
   "desc TEST",
]

commands_r1 = ["interface g0/2",
    "desc TEST",
]

#  ssh to device, pass in dictionary to net_connect
net_connect = Netmiko(**iosv_l2_s1)

print("")
print("Running commands to S1...")
print("")
# verify connection, will return "S1#"
print(net_connect.find_prompt())
# send list of commands from "commands"
output = net_connect.send_config_set(commands_s1)
output = net_connect.save_config()
print(output)
print("")
output = net_connect.send_command("show int des")
print(output)
print("")
print("Commands to S1 complete")
net_connect.disconnect()

net_connect = Netmiko(**iosv_r1)

print("")
print("Running commands to R1...")
print(net_connect.find_prompt())
output = net_connect.send_config_set(commands_r1)
output = net_connect.save_config()
print(output)
print("")
output = net_connect.send_command("show int des")
print(output)
print("")
print("Commands to R1 complete")
