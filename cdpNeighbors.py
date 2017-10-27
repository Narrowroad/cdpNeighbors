import re

def cdpNeighbors(txt):
    fields = [ ('deviceId', r'Device ID:\s*([\w\._-]+)'),
               ('ipAddress', r'IP(?:v4)? Address: (\d+\.\d+\.\d+\.\d+)'),
               ('platform', r'Platform: (\w[^,\r\n]*\w|\w)'),
               ('capabilities', r'Capabilities: (\w[^,\r\n]*\w|\w)'),
               ('localInterface', r'Interface: (\w[^,\r\n]*\w|\w)'),
               ('interface', r'Port ID \(outgoing port\): (\w[^,\r\n]*\w|\w)'),
               ('version', r'Version\s*:\s*\r?\n(\w[^\r\n]*)'),
               ('vtpDomain', r"VTP Management Domain(?: Name)?: '?(\w+)'?"),
               ('nativeVlan', r'Native VLAN: (\d+)'),
               ('duplex', r'Duplex: (\w[^\r\n]*\w|\w)')]
    for rawNeighbor in (n.group(1) for n in re.finditer(r'-{10,100}((?:.(?!-{10})){10,1500})', txt, re.S)):
        parsedNeighbor = dict()
        for label, exp in fields:
            m = re.search(exp, rawNeighbor, re.I)
            if m:
                parsedNeighbor[label] = m.group(1)
        if parsedNeighbor:
            yield parsedNeighbor
            
import unittest
class TestStringMethods(unittest.TestCase):
    def loadTestData(self, path):
        with open(path) as f:
            return f.read()

    def test_ws_c4507(self):
        self.maxDiff = None
        self.assertEqual(list(cdpNeighbors(self.loadTestData(r'.\testData\WS-C4507RE.txt')))[0],
        {'deviceId': 'SW-02.example.com', 'ipAddress': '10.10.10.2', 'platform': 'cisco WS-C3560-48PS', 'capabilities':
         'Switch IGMP', 'localInterface': 'GigabitEthernet1/5', 'interface': 'GigabitEthernet0/1', 'version':
         'Cisco IOS Software, C3560 Software (C3560-IPBASEK9-M), Version 12.2(53)SE2, RELEASE SOFTWARE (fc3)',
         'vtpDomain': 'VTPDOMAIN', 'nativeVlan': '1', 'duplex': 'full'})

    def test_n77_c7706(self):
        self.assertEqual(list(cdpNeighbors(self.loadTestData(r'.\testData\N77-C7706.txt')))[0],
        {'deviceId': 'SW-01', 'vtpDomain': 'VTPDOMAIN', 'ipAddress': '10.5.5.1', 'platform': 'WS-C2960-48TT',
         'capabilities': 'Switch IGMP Filtering', 'localInterface': 'mgmt0', 'interface': 'FastEthernet0/46',
         'version': 'Cisco IOS Software, C2960 Software (C2960-LANBASEK9-M), Version '
         '12.2(44)SE2, RELEASE SOFTWARE (fc2)', 'nativeVlan': '776', 'duplex': 'full'})

    def test_asr1001(self):
        self.assertEqual(list(cdpNeighbors(self.loadTestData(r'.\testData\ASR1001.txt')))[0],
        {'deviceId': 'SW-21.example.com', 'ipAddress': '10.30.5.21', 'platform': 'cisco WS-C2960X-24TS-L', 'capabilities':
         'Switch IGMP', 'interface': 'GigabitEthernet1/0/16', 'localInterface': 'GigabitEthernet0/0/1',
         'version': 'Cisco IOS Software, C2960X Software (C2960X-UNIVERSALK9-M), Version 15.0(2)EX3, RELEASE SOFTWARE (fc1)',
         'nativeVlan': '1', 'duplex': 'full'})

if __name__ == '__main__':
    unittest.main()