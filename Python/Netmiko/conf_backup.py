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

start_time = datetime.now()
for a_device in all_devices:
    net_connect = ConnectHandler(**a_device)
    hostname = net_connect.send_command("sh run | i hostname")
    hostname = hostname.split(" ")
    net_connect.send_command("terminal length 0")
    output = net_connect.send_command("sh run")
    outfile = open(hostname[1] + ".conf", "w")
    outfile.write(output)
    outfile.close()

end_time = datetime.now()
total_time = str(end_time - start_time)
print("\nCompleted in: " + total_time + "\n")
