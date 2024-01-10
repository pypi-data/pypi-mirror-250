#
# This file is part of pysnmp software.
#
# Copyright (c) 2005-2019, Ilya Etingof <etingof@gmail.com>
# License: http://snmplabs.com/pysnmp/license.html
#
from twisted.internet import reactor

from pysnmp.carrier import error
from pysnmp.carrier.base import AbstractTransportAddress
from pysnmp.carrier.twisted.dgram.base import DgramTwistedTransport

DOMAIN_NAME = SNMP_LOCAL_DOMAIN = (1, 3, 6, 1, 2, 1, 100, 1, 13)


class UnixTransportAddress(str, AbstractTransportAddress):
    pass


class UnixTwistedTransport(DgramTwistedTransport):
    ADDRESS_TYPE = UnixTransportAddress
    _lport = None

    # AbstractTwistedTransport API

    def openClientMode(self, iface=''):
        try:
            self._lport = reactor.connectUNIXDatagram(iface, self)

        except Exception as exc:
            raise error.CarrierError(exc)

        return self

    def openServerMode(self, iface):
        try:
            self._lport = reactor.listenUNIXDatagram(iface, self)

        except Exception as exc:
            raise error.CarrierError(exc)

        return self

    def closeTransport(self):
        if self._lport is not None:
            deferred = self._lport.stopListening()
            if deferred:
                deferred.addCallback(lambda x: None)

        DgramTwistedTransport.closeTransport(self)


UnixTransport = UnixTwistedTransport
