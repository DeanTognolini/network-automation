#!/usr/bin/env python
from netmiko import ConnectHandler
from datetime import datetime

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


all_devices = [Router1, Router2]

# set list of commands to pass to net_command.send_config_set
commands = [
    "interface g0/0",
    "desc This has changed",
]

start_time = datetime.now()
for a_device in all_devices:
    net_connect = ConnectHandler(**a_device)
    # stores interface description in "output" var
    output = net_connect.send_command("sh run int g0/0 | i description")
    # if not equal to "output" then the commands stored in "commands" list is sent. Ensure the spacing is correct as Cisco ios displays it.
    if output != " description This has changed":
        net_connect.send_config_set(commands)
        net_connect.save_config
        print("\nChanged was applied to {}.".format(a_device["host"]))
    output = net_connect.send_command("sh run int g0/0 | i desc")

end_time = datetime.now()
total_time = str(end_time - start_time)
print("\nCompleted in: " + total_time + "\n")
