import re

def cdpNeighbors(txt):
    fields = [ ('deviceId', r'Device ID: ([\w\._-]+)'),
               ('ipAddress', r'IP address: (\d+\.\d+\.\d+\.\d+)'),
               ('platform', r'Platform: (\w[^,\r\n]*\w|\w)'),
               ('capabilities', r'Capabilities: (\w[^,\r\n]*\w|\w)'),
               ('localInterface', r'Interface: (\w[^,\r\n]*\w|\w)'),
               ('interface', r'Port ID \(outgoing port\): (\w[^,\r\n]*\w|\w)'),
               ('version', r'Version\s*:\s*\r?\n(\w[^\r\n]*)'),
               ('nativeVlan', r'Native VLAN: (\d+)'),
               ('duplex', r'Duplex: (\w[^\r\n]*\w|\w)')]
    for rawNeighbor in (n.group(1) for n in re.finditer(r'-{25}((?:.(?!-{25}))+)', txt, re.S)):
        parsedNeighbor = dict()
        for label, exp in fields:
            m = re.search(exp, rawNeighbor)
            if m:
                parsedNeighbor[label] = m.group(1)
        if parsedNeighbor:
            yield parsedNeighbor

testData = '''
sh cdp nei det
-------------------------
Device ID: TEST-SW-1.example.local
Entry address(es): 
  IP address: 10.10.10.10
Platform: cisco WS-C3560-48PS,  Capabilities: Switch IGMP 
Interface: GigabitEthernet1/5,  Port ID (outgoing port): GigabitEthernet0/1
Holdtime : 168 sec

Version :
Cisco IOS Software, C3560 Software (C3560-IPBASEK9-M), Version 12.2(53)SE2, RELEASE SOFTWARE (fc3)

Native VLAN: 1
Duplex: full

-------------------------
Device ID: TEST-SW-2.example.local
Entry address(es): 
  IP address: 10.10.10.11
Platform: cisco WS-C3560-48PS,  Capabilities: Switch IGMP 
Interface: GigabitEthernet1/6,  Port ID (outgoing port): GigabitEthernet0/1
Holdtime : 153 sec

Version :
Cisco IOS Software, C3560 Software (C3560-IPBASEK9-M), Version 12.2(53)SE2, RELEASE SOFTWARE (fc3)

Native VLAN: 1
Duplex: full
'''

for nei in cdpNeighbors(testData):
    print(nei)
    print()

'''
Output looks like:

> python cdpNeighbors.py
{'deviceId': 'TEST-SW-1.example.local', 'ipAddress': '10.10.10.10', 'platform': 'cisco WS-C3560-48PS', 'capabilities': 'Switch IGMP',
'localInterface': 'GigabitEthernet1/5', 'interface': 'GigabitEthernet0/1', 'version': 'Cisco IOS Software, C3560 Software
(C3560-IPBASEK9-M), Version 12.2(53)SE2, RELEASE SOFTWARE (fc3)', 'nativeVlan': '1', 'duplex': 'full'}

{'deviceId': 'TEST-SW-2.example.local', 'ipAddress': '10.10.10.11', 'platform': 'cisco WS-C3560-48PS', 'capabilities': 'Switch IGMP',
'localInterface': 'GigabitEthernet1/6', 'interface': 'GigabitEthernet0/1', 'version': 'Cisco IOS Software, C3560 Software
(C3560-IPBASEK9-M), Version 12.2(53)SE2, RELEASE SOFTWARE (fc3)', 'nativeVlan': '1', 'duplex': 'full'}
'''
