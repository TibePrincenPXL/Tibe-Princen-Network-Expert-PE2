# Lab 3 - Netmiko Network Device Management

---

## Part 1: Install the Virtual Lab Environment

### 1. Task Preparation and Implementation
- Opzet van basis virtualisatie omgeving
- Configuratie van netwerk voor lab
- Voorbereiding van VirtualBox/hypervisor

### 2. Task Troubleshooting
**Opmerking:** Documentatie volledig gevolgd - geen problemen tegengekomen tijdens implementatie.  
**Resourceproblemen:** Uitsluitend eigenveroorzaakte PC-resource limitaties (geen invloed op opdracht).  
**Resultaat:** ✅

### 3. Task Verification
- ✅ Virtualisatie omgeving operationeel
- ✅ Netwerk correct geconfigureerd
- ✅ Lab environment klaar

---

## Part 2: Install the CSR1000v VM

### 1. Task Preparation and Implementation
- Download en import CSR1000v VM image
- Configuratie van VM netwerk interfaces
- Instelling van SSH access

### 2. Task Troubleshooting
**Opmerking:** Documentatie volledig gevolgd - geen problemen tegengekomen tijdens implementatie.  
**Resourceproblemen:** Uitsluitend eigenveroorzaakte PC-resource limitaties (geen invloed op opdracht).  
**Resultaat:** ✅

### 3. Task Verification
- ✅ CSR1000v VM succesvol geïnstalleerd
- ✅ Netwerk connectiviteit werkend
- ✅ SSH toegang beschikbaar op 192.168.128.200

---

## Part 3: Advanced Script Organization & Multiple Device Support

### 1. Task Preparation and Implementation
- Implementatie van `connect_and_configure()` functie
- Gebruikt Netmiko voor SSH-verbinding naar Cisco router
- Device dictionary voor connectie parameters
- File I/O voor backups en output opslag
- Support voor meerdere apparaten

### 2. Task Troubleshooting
**Probleem:** `TypeError: look_for_keys parameter unsupported`  
**Oorzaak:** Verouderde Netmiko parameterversie  
**Oplossing:** Verwijderde verouderde parameters uit device dictionary  
**Resultaat:** Script draait succesvol ✅

### 3. Task Verification

#### Requirements per Regel:

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

---

## Part 4: Explore YANG Models

### 1. Task Preparation and Implementation
- Exploratie van YANG model structuur
- Inzicht in device capabilities
- Data model hierarchie begrijpen
- Model validatie en toepassing

### 2. Task Troubleshooting
**Opmerking:** Documentatie volledig gevolgd - geen problemen tegengekomen tijdens implementatie.  
**Resourceproblemen:** Uitsluitend eigenveroorzaakte PC-resource limitaties (geen invloed op opdracht).  
**Resultaat:** ✅

### 3. Task Verification
- ✅ YANG models succesvol geladen
- ✅ Data model structuur begrepen
- ✅ Capabilities correct geïdentificeerd

---

## Part 5: Use NETCONF to Access an IOS XE Device

### Part 5.1: Launch the VMs and Verify Connectivity

#### 1. Task Preparation and Implementation
- VMs opstarten (DEVASC VM en CSR1000v VM)
- Verificatie van IP-connectiviteit
- SSH-verbinding tot stand brengen
- NETCONF protocol voorbereiding

#### 2. Task Troubleshooting
**Opmerking:** 
**Resourceproblemen:**   
**Resultaat:** 

#### 3. Task Verification

**Step 1-2:** VMs en connectiviteit
- ✅ Beide VMs succesvol opgestart
- ✅ CSR1000v IP: 192.168.128.200
- ✅ Ping naar router succesvol

**Step 3:** SSH Connectiviteit
```bash
ssh netmiko@192.168.128.200
Password: netmiko
```
- ✅ SSH connectiviteit geverifieerd
- ✅ Authenticity accepted
- ✅ Privileged EXEC prompt bereikt
- ✅ NETCONF port 830 beschikbaar

**Credentials (aangepast voor lab setup):**
- **Handleiding:** cisco / cisco123!
- **Huidige setup:** netmiko / netmiko

**Screenshot:** [Verwijzing naar SSH verbindingsbewijs]
<img width="760" height="431" alt="ssh-partt5" src="https://github.com/user-attachments/assets/314aaee1-149d-4bfa-931b-11962a053d6b" />
<img width="716" height="217" alt="netconfig-session-part5" src="https://github.com/user-attachments/assets/d0d7ec01-8139-41c2-bdbc-787bf0fed69e" />

---

## Part 6: Use RESTCONF to Access an IOS XE Device

### 1. Task Preparation and Implementation
- RESTCONF endpoint: https://192.168.128.200/restconf
- Authenticatie: basic auth (netmiko / netmiko)
- Headers: `Accept: application/yang-data+json`, `Content-Type: application/yang-data+json`
- GET ter verificatie (bijv. interfaces)
- PUT/PATCH voor config update (bijv. Loopback description)

### 2. Task Troubleshooting
**Probleem:** PUT → 415 Unsupported Media Type  
**Oorzaak:** Ontbrekende/juiste `Content-Type` header  
**Oplossing:** Headers gezet op `application/yang-data+json` (zowel Accept als Content-Type) en body als geldige JSON verstuurd  
**Resultaat:** ✅ PUT werkte na header fix

### 3. Task Verification
- ✅ GET bevestigt bereikbaarheid en dataformaat
- ✅ PUT/PATCH geeft 2xx na correcte headers
- ✅ Config change zichtbaar in opvolgende GET

<img width="1170" height="452" alt="postmanget-part6" src="https://github.com/user-attachments/assets/3233fe1e-3d5a-4943-a0a8-dd4368e3d4e9" />

---

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
