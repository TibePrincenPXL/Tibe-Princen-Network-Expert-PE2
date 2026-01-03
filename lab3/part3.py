#! /usr/bin/env python

from netmiko import ConnectHandler
import os

# • Connect using a Python Dictionary
# • Send show commands to multiple devices
# • Send configuration commands to multiple devices
devices = [
    {"device_type": "cisco_ios",
     "host": "192.168.128.200",
      "username": "netmiko",
       "password": "netmiko"},
]

# • Execute a script with functions or classes
def connect_and_configure(device):
    try:
        conn = ConnectHandler(**device)
        host = device["host"]
        
        # • Send show commands to a single device
        # • Run show commands and save the output
        output = conn.send_command("show ip interface brief")
        with open("output.txt", "a") as f:
            f.write(f"\n{'='*60}\n{host}\n{'='*60}\n{output}\n")
        
        # • Backup the device configurations to an external file
        config = conn.send_command("show running-config")
        with open(f"backup_{host}.txt", "w") as f:
            f.write(config)
        
        # • Send device configuration using an external file
        if os.path.exists("config.txt"):
            with open("config.txt") as f:
                commands = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            conn.send_config_set(commands)
            print(f"  ✓ Applied config from file")
        
        # • Send configuration commands to a single device
        # • Configure a subset of interfaces
        conn.send_config_set([
            "interface GigabitEthernet1",
            "description Primary Interface",
            "no shutdown"
        ])
        
        conn.save_config()
        conn.disconnect()
        print(f"✓ {host}")
        
    except Exception as e:
        print(f"✗ Error with {device['host']}: {e}")

# • Execute a script with conditional statements (if, else)
if __name__ == "__main__":
    print("\n=== Network Device Management ===")
    
    if not os.path.exists("config.txt"):
        with open("config.txt", "w") as f:
            f.write("# Sample config\ninterface GigabitEthernet2\ndescription Configured\nno shutdown\n")
        print("✓ Sample config.txt created\n")
    
    if devices:
        print("Processing devices:")
        for device in devices:
            connect_and_configure(device)
    else:
        print("No devices configured")
    
    print("\n=== Complete ===")


