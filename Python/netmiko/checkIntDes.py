from ciscoconfparse2 import CiscoConfParse
from netmiko import ConnectHandler
import getpass

def backup_device_configs_to_memory(all_devices):
    """
    Connects to a list of devices, retrieves their configurations,
    and stores the configurations in a dictionary for further processing.

    Parameters:
    - all_devices (list): A list of dictionaries, each containing connection parameters for a device.

    Returns:
    - dict: A dictionary where keys are hostnames and values are the configuration contents.
    """
    configs = {}

    for a_device in all_devices:
        try:
            # Establish connection to the device
            net_connect = ConnectHandler(**a_device)

            # Get the hostname
            hostname = net_connect.send_command("show run | include hostname").split()[1]
            print("\nConnecting to " + hostname + "...")

            # Set terminal length to avoid pagination and retrieve the full running config
            net_connect.send_command("terminal length 0")
            output = net_connect.send_command("show run")

            # Store the configuration in the dictionary
            configs[hostname] = output
            print(f"Configuration for {hostname} retrieved successfully.")

            # Disconnect from the device
            net_connect.disconnect()

        except Exception as e:
            print(f"Failed to process device {a_device.get('host', 'Unknown')}: {e}")

    return configs


def parse_int_configuration(config):
    """
    Parses a Cisco IOS BGP configuration file and extracts:
    - Hostname
    - Interface Names
    - Interface Descriptions
    """
    # Parse the configuration file using CiscoConfParse
    parse = CiscoConfParse(config)

    # Extract the device hostname
    hostname = parse.re_match_iter_typed(r"^hostname\s+(\S+)", default="")

    # Extract GRT BGP neighbors
    print(f"""
------------------------------------------------
Hostname: {hostname}
------------------------------------------------
   Interfaces
------------------------""")
    branches = parse.find_object_branches(["interface",""])
    for branch in branches:
        intf_name = branch[0].re_match_typed(r"^interface\s+(\S+)", default="")
        intf_desc = branch[1].re_match_typed(r".description\s+(\S+)", default="None")
        
        if "shutdown" in branch:
            intf_status = "Shutdown"
        else: 
            intf_status = "Up"
        
        print(f"Name: {intf_name}, Description: {intf_desc}, Status: {intf_status}")

username = input("Enter username: ")
password = getpass.getpass("Enter password: ")

all_devices = [
    {
        "device_type": "cisco_xe",
        "host": "10.29.252.194",
        "username": username,
        "password": password
    },
    {
        "device_type": "cisco_xe",
        "host": "10.29.252.164",
        "username": username,
        "password": password
    }
    ]

configs = backup_device_configs_to_memory(all_devices)

for config in configs:
    parse_int_configuration(configs[config])