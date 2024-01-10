#
# This file is part of pysnmp software.
#
# Copyright (c) 2005-2019, Ilya Etingof <etingof@gmail.com>
# License: http://snmplabs.com/pysnmp/license.html
#
from socket import AF_INET

from pysnmp.carrier.asyncore.dgram.base import DgramSocketTransport
from pysnmp.carrier.base import AbstractTransportAddress

DOMAIN_NAME = SNMP_UDP_DOMAIN = (1, 3, 6, 1, 6, 1, 1)


class UdpTransportAddress(tuple, AbstractTransportAddress):
    pass


class UdpSocketTransport(DgramSocketTransport):
    SOCK_FAMILY = AF_INET
    ADDRESS_TYPE = UdpTransportAddress


UdpTransport = UdpSocketTransport
