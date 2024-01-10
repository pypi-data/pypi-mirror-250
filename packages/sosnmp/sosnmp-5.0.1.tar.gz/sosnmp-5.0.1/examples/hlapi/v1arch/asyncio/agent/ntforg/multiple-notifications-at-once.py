"""
Multiple concurrent notifications
+++++++++++++++++++++++++++++++++

Send multiple SNMP notifications at once using the following options:

* SNMPv2c
* with community name 'public'
* over IPv4/UDP
* send INFORM notification
* to multiple Managers
* with TRAP ID 'coldStart' specified as a MIB symbol

Functionally similar to:

| $ snmptrap -v2c -c public demo.snmplabs.com 12345 1.3.6.1.6.3.1.1.5.2
| $ snmpinform -v2c -c public demo.snmplabs.com 12345 1.3.6.1.6.3.1.1.5.2

"""#
import asyncio

from pysnmp.hlapi.v1arch.asyncio import *


@asyncio.coroutine
def sendone(snmpDispatcher, hostname, notifyType):

    iterator = sendNotification(
        snmpDispatcher,
        CommunityData('public'),
        UdpTransportTarget((hostname, 162)),
        notifyType,
        NotificationType(
            ObjectIdentity('1.3.6.1.6.3.1.1.5.2')
        ).loadMibs('SNMPv2-MIB')
    )

    errorIndication, errorStatus, errorIndex, varBinds = yield from iterator

    if errorIndication:
        print(errorIndication)

    elif errorStatus:
        print('%s: at %s' % (errorStatus.prettyPrint(), errorIndex and
                             varBinds[int(errorIndex) - 1][0] or '?'))

    else:
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))


snmpDispatcher = SnmpDispatcher()

loop = asyncio.get_event_loop()
loop.run_until_complete(
    asyncio.wait(
        [sendone(snmpDispatcher, 'demo.snmplabs.com', 'trap'),
         sendone(snmpDispatcher, 'demo.snmplabs.com', 'inform')]
    )
)
