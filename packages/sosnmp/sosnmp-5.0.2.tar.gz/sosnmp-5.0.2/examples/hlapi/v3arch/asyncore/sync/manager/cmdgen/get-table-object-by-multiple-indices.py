"""
Fetch table row by composite index
++++++++++++++++++++++++++++++++++

Send SNMP GET request using the following options:

* with SNMPv3, user 'usr-sha-aes128', SHA auth, AES128 privacy
* over IPv4/UDP
* to an Agent at demo.snmplabs.com:161
* for TCP-MIB::tcpConnLocalAddress."0.0.0.0".22."0.0.0.0".0 MIB object

Functionally similar to:

| $ snmpget -v3 -l authPriv -u usr-md5-des -A authkey1 -X privkey1 -a SHA -x AES demo.snmplabs.com TCP-MIB::tcpConnLocalAddress."0.0.0.0".22."0.0.0.0".0

"""#
from pysnmp.hlapi import *

iterator = getCmd(
    SnmpEngine(),
    UsmUserData(
        'usr-sha-aes128', 'authkey1', 'privkey1',
        authProtocol=USM_AUTH_HMAC96_SHA,
        privProtocol=USM_PRIV_CFB128_AES
    ),
    UdpTransportTarget(('demo.snmplabs.com', 161)),
    ContextData(),
    ObjectType(
        ObjectIdentity(
            'TCP-MIB',
            'tcpConnLocalAddress',
            '0.0.0.0', 22,
            '0.0.0.0', 0
        )
    ).addAsn1MibSource('http://mibs.snmplabs.com/asn1/@mib@')
)

errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

if errorIndication:
    print(errorIndication)

elif errorStatus:
    print('%s at %s' % (errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

else:
    for varBind in varBinds:
        print(' = '.join([x.prettyPrint() for x in varBind]))
