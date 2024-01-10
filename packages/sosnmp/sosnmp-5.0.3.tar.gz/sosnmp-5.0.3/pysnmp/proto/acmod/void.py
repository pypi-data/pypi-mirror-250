#
# This file is part of pysnmp software.
#
# Copyright (c) 2005-2019, Ilya Etingof <etingof@gmail.com>
# License: http://snmplabs.com/pysnmp/license.html
#
from pysnmp import debug
from pysnmp.proto import errind
from pysnmp.proto import error


# rfc3415 3.2
# noinspection PyUnusedLocal
class Vacm(object):
    """Void Access Control Model"""
    ACCESS_MODEL_ID = 0

    def isAccessAllowed(self, snmpEngine, securityModel, securityName,
                        securityLevel, viewType, contextName, variableName):
        debug.logger & debug.FLAG_ACL and debug.logger(
            'isAccessAllowed: viewType %s for variableName '
            '%s - OK' % (viewType, variableName))

        # rfc3415 3.2.5c
        return error.StatusInformation(errorIndication=errind.accessAllowed)
