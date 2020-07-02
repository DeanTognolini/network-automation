#!/usr/bin/env python
from netmiko import ConnectHandler
from datetime import datetime

iosv_l2_s1 = {"host": "10.1.1.1",
              "username": "admin",
              "password": "admin",
              "device_type": "cisco_ios",}

iosv_r1 = {"host": "10.1.1.254",
           "username": "admin",
           "password": "admin",
           "device_type": "cisco_ios",}

all_devices = [iosv_l2_s1, iosv_r1]

start_time = datetime.now()
for a_device in all_devices:
   net_connect = ConnectHandler(**a_device)
   output = net_connect.send_command("show arp")
   print("\n------ Host: "+ a_device['host'] +" Device Type: "+ a_device['device_type']+ " ------\n\n" + output +
         "\n\n-------- End --------")

end_time = datetime.now()
total_time = str(end_time - start_time)
print("\nCompleted in: " + total_time + "\n")