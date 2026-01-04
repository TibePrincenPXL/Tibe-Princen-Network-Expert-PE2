# Task 38 – RESTCONF Python Automatisering

## Doel
Ontwikkel een Python-automatiseringsoplossing die configuratiegegevens van GitHub ophaalt en deze via RESTCONF toepast op een Cisco IOS-XE toestel met behulp van YANG-modellen.

## Gebruikte Technieken
- **RESTCONF** voor configuratie (PUT en PATCH)
- **YANG-compliant JSON** voor datarepresentatie
- **GitHub** als single source of truth voor configuratie
- **Python logging** voor succes- en foutmeldingen

## Script-functionaliteit
1. **Configuratie ophalen van GitHub**
   - URL: `https://raw.githubusercontent.com/.../taak38-config.json`
   - JSON wordt ingeladen en verwerkt.

2. **Hostname configureren**
   - RESTCONF PUT naar `/Cisco-IOS-XE-native:native/hostname`
   - Controle op HTTP-statuscodes
   - Logging van succes of fout

3. **Loopback-interfaces configureren**
   - RESTCONF PUT naar `/ietf-interfaces:interfaces/interface={name}`
   - Configuratie van IPv4-adressen
   - Logging van succes of fout

4. **OSPF configureren**
   - RESTCONF PATCH naar `/Cisco-IOS-XE-native:native/router/Cisco-IOS-XE-ospf:ospf`
   - Ondersteuning voor meerdere netwerken
   - Logging van succes of fout

## Resultaten
- Configuratie is zichtbaar in de running-config van het apparaat.
- Script is herhaalbaar en redelijk idempotent.
- Logging geeft duidelijk inzicht in welke configuratie succesvol werd toegepast.

## Opmerkingen / Problemen
- **Body formatting:** Af en toe problemen met de exacte JSON-structuur voor sommige YANG-modellen, wat leidde tot foutmeldingen van RESTCONF.
- **GitHub permissions:** Toegang tot de raw-config kan fout gaan als permissies of netwerkbeperkingen aanwezig zijn.

## Conclusie
Het script voldoet aan de vereisten van Task 38. Alle kernfunctionaliteit (hostname, interfaces, OSPF) werkt, maar er waren enkele uitdagingen met de juiste body formatting en fetch-permissions van GitHub. Over het algemeen verliep de uitvoering redelijk goed.
