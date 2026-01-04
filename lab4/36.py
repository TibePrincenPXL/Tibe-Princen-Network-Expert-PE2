#!/usr/bin/env python3
import logging
from ncclient import manager
import requests

# ---------- CONFIGURATIE ---------- #

DEVICE = {
    "host": "192.168.128.200",  # Pas aan naar jouw router IP
    "port": 830,
    "username": "netmiko",
    "password": "netmiko",
}

GITHUB_CONFIG_URL = "https://raw.githubusercontent.com/TibePrincenPXL/Tibe-Princen-Network-Expert-PE2/main/lab4/taak36-config.xml"

# RAW URL naar jouw config.xml op GitHub

logging.basicConfig(level=logging.INFO)

# ---------- FUNCTIES ---------- #

def fetch_config(url):
    """Haalt XML-config op uit GitHub"""
    r = requests.get(url)
    if r.status_code == 200:
        logging.info("Configuratie succesvol opgehaald uit GitHub")
        return r.text
    else:
        raise Exception(f"Kan configuratie niet ophalen: {r.status_code}")

def deploy_config(device, config_xml):
    """Deployt XML-config via NETCONF naar candidate datastore"""
    try:
        with manager.connect(
            host=device["host"],
            port=device["port"],
            username=device["username"],
            password=device["password"],
            hostkey_verify=False,
            device_params={'name': 'iosxe'},
            look_for_keys=False,
            allow_agent=False
        ) as m:
            logging.info("NETCONF sessie geopend")

            # ---------- Controleer candidate support ----------
            caps = [str(cap) for cap in m.server_capabilities]
            if not any('candidate' in cap for cap in caps):
                raise Exception("Device ondersteunt geen candidate datastore! Dit is verplicht voor Task 36.")
            logging.info("Candidate datastore beschikbaar")

            # ---------- Lock candidate ----------
            m.lock(target='candidate')
            logging.info("Candidate datastore gelockt")

            # ---------- Edit-config naar candidate ----------
            m.edit_config(target='candidate', config=config_xml)
            logging.info("Configuratie naar candidate toegepast")

            # ---------- Commit naar running ----------
            m.commit()
            logging.info("Configuratie succesvol gecommit naar running")

            # ---------- Unlock candidate ----------
            m.unlock(target='candidate')
            logging.info("Candidate datastore unlocked")

    except Exception as e:
        logging.error(f"Fout tijdens deployment: {e}")
        try:
            if 'm' in locals():
                m.discard_changes()
                logging.info("Veranderingen teruggedraaid (discard-changes)")
        except Exception as discard_e:
            logging.warning(f"Kon discard-changes niet uitvoeren: {discard_e}")
        raise

# ---------- MAIN ---------- #
if __name__ == "__main__":
    # 1. Haal configuratie op uit GitHub
    config_xml = fetch_config(GITHUB_CONFIG_URL)

    # 2. Deploy via NETCONF naar candidate
    deploy_config(DEVICE, config_xml)
