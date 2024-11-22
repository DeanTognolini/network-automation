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


def parse_bgp_configuration(config):
    """
    Parses a Cisco IOS BGP configuration file and extracts:
    - Hostname
    - Local BGP ASN
    - GRT BGP Neighbors
    - VRF AF BGP Neighbors
    """
    # Parse the configuration file using CiscoConfParse
    parse = CiscoConfParse(config)

    # Extract the device hostname
    hostname = parse.re_match_iter_typed(r'^hostname\s+(\S+)', default='')

    # Extract the local BGP ASN
    parent = parse.find_parent_objects(["router bgp"])
    bgp_cmd = parent[0]
    local_asn = bgp_cmd.split()[-1]

    # Extract GRT BGP neighbors
    print(f"""
------------------------------------------------
Hostname: {hostname}
Local ASN: {local_asn}
------------------------------------------------
   GRT Neighbours
------------------------""")
    grt_branches = parse.find_object_branches(["router bgp", "remote-as"])
    for branch in grt_branches:
        neighbor_addr = branch[1].re_match_typed(r".neighbor\s+(\S+)", default="")
        remote_asn = branch[1].re_match_typed(r".remote-as\s+(\S+)", default="")
        if local_asn != remote_asn:
            print(f"eBGP: {neighbor_addr}")
        elif local_asn == remote_asn:
            print(f"iBGP: {neighbor_addr}")

    # Extract VRF AF BGP neighbors
    print("""
------------------------
   VRF Neighbours
------------------------""")
    vrf_branches = parse.find_object_branches(["router bgp", "address-family", "remote-as"])
    for branch in vrf_branches:
        neighbor_addr = branch[2].re_match_typed(r".neighbor\s+(\S+)", default="")
        af = branch[1].re_match_typed(r".vrf\s+(\S+)", default="")
        remote_asn = branch[2].re_match_typed(r".remote-as\s+(\S+)", default="")
        if local_asn != remote_asn:
            print(f"eBGP: {af} {neighbor_addr}")
        elif local_asn == remote_asn:
            print(f"iBGP: {af} {neighbor_addr}")

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
    parse_bgp_configuration(configs[config])