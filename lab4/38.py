import requests
import json
import logging

# Logging configuratie
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Device info
DEVICE = {
    "host": "192.168.128.200",
    "username": "netmiko",
    "password": "netmiko"
}

# RESTCONF basis URL
BASE_URL = f"https://{DEVICE['host']}/restconf/data"

# Headers RESTCONF (JSON/YANG)
HEADERS = {
    "Content-Type": "application/yang-data+json",
    "Accept": "application/yang-data+json"
}

# URL GitHub-config (raw)
CONFIG_URL = "https://raw.githubusercontent.com/TibePrincenPXL/Tibe-Princen-Network-Expert-PE2/main/lab4/taak38-config.json"

def fetch_config():
    """Haalt JSON-config van GitHub"""
    response = requests.get(CONFIG_URL)
    if response.status_code == 200:
        logging.info("Configuratie succesvol opgehaald van GitHub")
        config = response.json()
        print("DEBUG: opgehaalde config:", config)  # <<<<<<<<<<
        return response.json()
    else:
        logging.error(f"Kon configuratie niet ophalen: {response.status_code}")
        return None

def apply_hostname(config):
    url = f"{BASE_URL}/Cisco-IOS-XE-native:native/hostname"
    data = {"Cisco-IOS-XE-native:hostname": config['hostname']}
    r = requests.put(url, auth=(DEVICE['username'], DEVICE['password']), headers=HEADERS, json=data, verify=False)
    if r.status_code in [200,201,204]:
        logging.info(f"Hostname '{config['hostname']}' toegepast")
    else:
        logging.error(f"Fout bij hostname: {r.status_code} {r.text}")

def apply_loopbacks(config):
    """Configureer loopbacks via IETF-interfaces en juiste namespaces"""
    for lb in config.get('loopbacks', []):
        url = f"{BASE_URL}/ietf-interfaces:interfaces/interface={lb['name']}"
        data = {
            "ietf-interfaces:interface": {
                "name": lb['name'],
                "description": f"Loopback {lb['name']} via RESTCONF",
                "type": "iana-if-type:softwareLoopback",
                "enabled": True,
                "ietf-ip:ipv4": {
                    "address": [
                        {
                            "ip": lb['ip'],
                            "netmask": lb['mask']
                        }
                    ]
                },
                "ietf-ip:ipv6": {}
            }
        }
        r = requests.put(url, auth=(DEVICE['username'], DEVICE['password']),
                         headers=HEADERS, json=data, verify=False)
        if r.status_code in [200,201,204]:
            logging.info(f"{lb['name']} toegepast met IP {lb['ip']}")
        else:
            logging.error(f"Fout bij {lb['name']}: {r.status_code} {r.text}")

def apply_ospf(config):
    """Configure OSPF via Cisco IOS-XE model with PATCH"""
    ospf = config.get('ospf', {})
    networks = ospf.get('networks', [])
    if not networks:
        logging.warning("Geen OSPF-netwerken gespecificeerd")
        return

    data = {
        "Cisco-IOS-XE-ospf:ospf": {
            "id": ospf.get('process_id', 1),
            "router-id": ospf.get('router_id', "1.1.1.1"),
            "network": [
                {
                    "ip": net['network'],
                    "mask": net['mask'],
                    "area": net['area']
                } for net in networks
            ]
        }
    }

    url = f"{BASE_URL}/Cisco-IOS-XE-native:native/router/Cisco-IOS-XE-ospf:ospf"
    r = requests.patch(
        url,
        auth=(DEVICE['username'], DEVICE['password']),
        headers=HEADERS,
        json=data,
        verify=False
    )

    if r.status_code in [200, 201, 204]:
        logging.info("OSPF-config toegepast via PATCH")
    else:
        logging.error(f"Fout bij OSPF-config: {r.status_code} {r.text}")


def main():
    config = fetch_config()
    if not config:
        return
    apply_hostname(config)
    apply_loopbacks(config)
    apply_ospf(config)

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    main()
