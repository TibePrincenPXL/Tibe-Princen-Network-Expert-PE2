from ncclient import manager
import xml.dom.minidom

# Connect to the NETCONF device
m = manager.connect(
    host="192.168.128.200",
    port=830,
    username="netmiko",
    password="netmiko",
    hostkey_verify=False
)

# Print supported capabilities
print("# Supported Capabilities (YANG models):")
for capability in m.server_capabilities:
    print(capability)

# Get the running configuration
netconf_reply = m.get_config(source="running")
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

# Get the running configuration with a filter for Cisco native config
netconf_filter = """
<filter>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native" />
</filter>
"""
netconf_reply = m.get_config(source="running", filter=netconf_filter)
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

# Change the hostname
netconf_hostname = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname>R3</hostname>
  </native>
</config>
"""
netconf_reply = m.edit_config(target="running", config=netconf_hostname)
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

# Create a first Loopback interface
netconf_loopback = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <Loopback>
        <name>1</name>
        <description>My NETCONF loopback</description>
        <ip>
          <address>
            <primary>
              <address>10.1.1.1</address>
              <mask>255.255.255.0</mask>
            </primary>
          </address>
        </ip>
      </Loopback>
    </interface>
  </native>
</config>
"""
netconf_reply = m.edit_config(target="running", config=netconf_loopback)
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

# Create a second Loopback interface
netconf_newloop = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <Loopback>
        <name>2</name>
        <description>My second NETCONF loopback</description>
        <ip>
          <address>
            <primary>
              <address>10.1.1.2</address>
              <mask>255.255.255.0</mask>
            </primary>
          </address>
        </ip>
      </Loopback>
    </interface>
  </native>
</config>
"""
netconf_reply = m.edit_config(target="running", config=netconf_newloop)
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
