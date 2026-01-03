import json
import requests

# Disable SSL warnings
requests.packages.urllib3.disable_warnings()

# Device RESTCONF URL
api_url = "https://192.168.128.200/restconf/data/ietf-interfaces:interfaces"

# HTTP headers for RESTCONF
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

# Basic authentication credentials
basicauth = ("netmiko", "netmiko")  # updated username/password

# Send GET request to RESTCONF API
resp = requests.get(api_url, auth=basicauth, headers=headers, verify=False)

# Print the response status code
print(f"HTTP Response Code: {resp.status_code}")

# Convert response to JSON and pretty print
response_json = resp.json()
print(json.dumps(response_json, indent=4))
