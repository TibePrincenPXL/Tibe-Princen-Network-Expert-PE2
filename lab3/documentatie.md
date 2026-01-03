
## Router Configuration (Vereisten)

Voor remote programmability moet de router eerst geconfigureerd worden:

### SSH Verbinding:
```bash
ssh -oHostKeyAlgorithms=+ssh-rsa -oKexAlgorithms=+diffie-hellman-group14-sha1 netmiko@192.168.128.200
```

### Router CLI Configuratie:
```
enable
configure terminal

! Set router interface on LAN subnet
interface GigabitEthernet1
 ip address 192.168.128.200 255.255.254.0
 no shutdown
exit

! Set default route via LAN gateway
ip route 0.0.0.0 0.0.0.0 192.168.128.1

! SSH configuration
hostname R1
ip domain-name lab.local
username netmiko privilege 15 secret NetmikoPass123
crypto key generate rsa
ip ssh version 2
ip ssh time-out 60
ip ssh authentication-retries 3

line vty 0 4
 login local
 transport input ssh
 exec-timeout 30 0
exit

! Save config
write memory
```
---
# Lab 3 - Netmiko Network Device Management

## 1. Task Preparation and Implementation
- Implementatie van `connect_and_configure()` functie
- Gebruikt Netmiko voor SSH-verbinding naar Cisco router
- Device dictionary voor connectie parameters
- File I/O voor backups en output opslag
- Support voor meerdere apparaten

## 2. Task Troubleshooting
**Probleem:** `TypeError: look_for_keys parameter unsupported`  
**Oplossing:** Verwijderde verouderde parameters uit device dictionary  
**Resultaat:** Script draait succesvol ✅

## 3. Task Verification

### Requirements per Regel:

| # | Requirement | Regels | Code |
|---|-------------|--------|------|
| 1 | Connect using a Python Dictionary | 6-14 | `devices = [{"device_type": "cisco_ios", "host": "192.168.128.200", ...}]` |
| 2 | Send show commands to a single device | 25 | `output = conn.send_command("show ip interface brief")` |
| 3 | Run show commands and save the output | 25-27 | Save output naar `output.txt` met host info |
| 4 | Backup the device configurations to an external file | 30-32 | `show running-config` opslaan in `backup_{host}.txt` |
| 5 | Send device configuration using an external file | 34-39 | Lees `config.txt` en apply met `send_config_set()` |
| 6 | Configure a subset of interfaces | 41-45 | GigabitEthernet1 configureren direct |
| 7 | Execute a script with functions or classes | 18 | Functie `connect_and_configure(device)` |
| 8 | Execute a script with conditional statements (if, else) | 34, 61, 64 | if/else voor file check, devices check, loop |
| 9 | Send configuration commands to a single device | 41-45 | `conn.send_config_set([...])` |
| 10 | Send show commands to multiple devices | 63-65 | `for device in devices:` loop |
| 11 | Send configuration commands to multiple devices | 63-65 | Functie wordt voor elk device aangeroepen |

**Gegenereerde bestanden:** output.txt, config.txt, backup_192.168.128.200.txt

**Status:** ✅ Voltooid
