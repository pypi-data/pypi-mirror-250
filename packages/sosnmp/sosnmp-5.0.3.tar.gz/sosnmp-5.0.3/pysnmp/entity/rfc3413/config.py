#
# This file is part of pysnmp software.
#
# Copyright (c) 2005-2019, Ilya Etingof <etingof@gmail.com>
# License: http://snmplabs.com/pysnmp/license.html
#
from pysnmp.entity import config
from pysnmp.smi.error import NoSuchInstanceError
from pysnmp.smi.error import SmiError


def getTargetAddr(snmpEngine, snmpTargetAddrName):
    mibBuilder = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder

    snmpTargetAddrEntry, = mibBuilder.importSymbols(
        'SNMP-TARGET-MIB', 'snmpTargetAddrEntry'
    )

    cache = snmpEngine.getUserContext('getTargetAddr')
    if cache is None:
        cache = {'id': -1}
        snmpEngine.setUserContext(getTargetAddr=cache)

    if cache['id'] != snmpTargetAddrEntry.branchVersionId:
        cache['nameToTargetMap'] = {}

    nameToTargetMap = cache['nameToTargetMap']

    if snmpTargetAddrName not in nameToTargetMap:
        (snmpTargetAddrTDomain,
         snmpTargetAddrTAddress,
         snmpTargetAddrTimeout,
         snmpTargetAddrRetryCount,
         snmpTargetAddrParams) = mibBuilder.importSymbols(
            'SNMP-TARGET-MIB', 'snmpTargetAddrTDomain',
            'snmpTargetAddrTAddress', 'snmpTargetAddrTimeout',
            'snmpTargetAddrRetryCount', 'snmpTargetAddrParams'
        )
        snmpSourceAddrTAddress, = mibBuilder.importSymbols(
            'PYSNMP-SOURCE-MIB', 'snmpSourceAddrTAddress')

        tblIdx = snmpTargetAddrEntry.getInstIdFromIndices(snmpTargetAddrName)

        try:
            snmpTargetAddrTDomain = snmpTargetAddrTDomain.getNode(
                snmpTargetAddrTDomain.name + tblIdx
            ).syntax

            snmpTargetAddrTAddress = snmpTargetAddrTAddress.getNode(
                snmpTargetAddrTAddress.name + tblIdx
            ).syntax

            snmpTargetAddrTimeout = snmpTargetAddrTimeout.getNode(
                snmpTargetAddrTimeout.name + tblIdx
            ).syntax

            snmpTargetAddrRetryCount = snmpTargetAddrRetryCount.getNode(
                snmpTargetAddrRetryCount.name + tblIdx
            ).syntax

            snmpTargetAddrParams = snmpTargetAddrParams.getNode(
                snmpTargetAddrParams.name + tblIdx
            ).syntax

            snmpSourceAddrTAddress = snmpSourceAddrTAddress.getNode(
                snmpSourceAddrTAddress.name + tblIdx
            ).syntax

        except NoSuchInstanceError:
            raise SmiError('Target %s not configured to LCD' % snmpTargetAddrName)

        transport = snmpEngine.transportDispatcher.getTransport(snmpTargetAddrTDomain)

        if snmpTargetAddrTDomain[:len(config.SNMP_UDP_DOMAIN)] == config.SNMP_UDP_DOMAIN:
            SnmpUDPAddress, = mibBuilder.importSymbols('SNMPv2-TM', 'SnmpUDPAddress')

            snmpTargetAddrTAddress = transport.ADDRESS_TYPE(
                SnmpUDPAddress(snmpTargetAddrTAddress)
            ).setLocalAddress(SnmpUDPAddress(snmpSourceAddrTAddress))

        elif snmpTargetAddrTDomain[:len(config.SNMP_UDP6_DOMAIN)] == config.SNMP_UDP6_DOMAIN:
            TransportAddressIPv6, = mibBuilder.importSymbols('TRANSPORT-ADDRESS-MIB', 'TransportAddressIPv6')

            snmpTargetAddrTAddress = transport.ADDRESS_TYPE(
                TransportAddressIPv6(snmpTargetAddrTAddress)
            ).setLocalAddress(TransportAddressIPv6(snmpSourceAddrTAddress))

        elif snmpTargetAddrTDomain[:len(config.snmpLocalDomain)] == config.snmpLocalDomain:
            snmpTargetAddrTAddress = transport.ADDRESS_TYPE(
                snmpTargetAddrTAddress
            )

        nameToTargetMap[snmpTargetAddrName] = (
            snmpTargetAddrTDomain,
            snmpTargetAddrTAddress,
            snmpTargetAddrTimeout,
            snmpTargetAddrRetryCount,
            snmpTargetAddrParams
        )

        cache['id'] = snmpTargetAddrEntry.branchVersionId

    return nameToTargetMap[snmpTargetAddrName]


def getTargetParams(snmpEngine, paramsName):
    mibBuilder = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder

    snmpTargetParamsEntry, = mibBuilder.importSymbols(
        'SNMP-TARGET-MIB', 'snmpTargetParamsEntry'
    )

    cache = snmpEngine.getUserContext('getTargetParams')
    if cache is None:
        cache = {'id': -1}
        snmpEngine.setUserContext(getTargetParams=cache)

    if cache['id'] != snmpTargetParamsEntry.branchVersionId:
        cache['nameToParamsMap'] = {}

    nameToParamsMap = cache['nameToParamsMap']

    if paramsName not in nameToParamsMap:
        (snmpTargetParamsMPModel, snmpTargetParamsSecurityModel,
         snmpTargetParamsSecurityName,
         snmpTargetParamsSecurityLevel) = mibBuilder.importSymbols(
            'SNMP-TARGET-MIB', 'snmpTargetParamsMPModel',
            'snmpTargetParamsSecurityModel', 'snmpTargetParamsSecurityName',
            'snmpTargetParamsSecurityLevel'
        )

        tblIdx = snmpTargetParamsEntry.getInstIdFromIndices(paramsName)

        try:
            snmpTargetParamsMPModel = snmpTargetParamsMPModel.getNode(
                snmpTargetParamsMPModel.name + tblIdx
            ).syntax

            snmpTargetParamsSecurityModel = snmpTargetParamsSecurityModel.getNode(
                snmpTargetParamsSecurityModel.name + tblIdx
            ).syntax

            snmpTargetParamsSecurityName = snmpTargetParamsSecurityName.getNode(
                snmpTargetParamsSecurityName.name + tblIdx
            ).syntax

            snmpTargetParamsSecurityLevel = snmpTargetParamsSecurityLevel.getNode(
                snmpTargetParamsSecurityLevel.name + tblIdx
            ).syntax

        except NoSuchInstanceError:
            raise SmiError('Parameters %s not configured at LCD' % paramsName)

        nameToParamsMap[paramsName] = (snmpTargetParamsMPModel,
                                       snmpTargetParamsSecurityModel,
                                       snmpTargetParamsSecurityName,
                                       snmpTargetParamsSecurityLevel)

        cache['id'] = snmpTargetParamsEntry.branchVersionId

    return nameToParamsMap[paramsName]


def getTargetInfo(snmpEngine, snmpTargetAddrName):
    # Transport endpoint
    (snmpTargetAddrTDomain,
     snmpTargetAddrTAddress,
     snmpTargetAddrTimeout,
     snmpTargetAddrRetryCount,
     snmpTargetAddrParams) = getTargetAddr(snmpEngine, snmpTargetAddrName)

    (snmpTargetParamsMPModel,
     snmpTargetParamsSecurityModel,
     snmpTargetParamsSecurityName,
     snmpTargetParamsSecurityLevel) = getTargetParams(
        snmpEngine, snmpTargetAddrParams)

    return (snmpTargetAddrTDomain, snmpTargetAddrTAddress,
            snmpTargetAddrTimeout, snmpTargetAddrRetryCount,
            snmpTargetParamsMPModel, snmpTargetParamsSecurityModel,
            snmpTargetParamsSecurityName, snmpTargetParamsSecurityLevel)


def getNotificationInfo(snmpEngine, notificationTarget):
    mibBuilder = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder

    snmpNotifyEntry, = mibBuilder.importSymbols(
        'SNMP-NOTIFICATION-MIB', 'snmpNotifyEntry')

    cache = snmpEngine.getUserContext('getNotificationInfo')
    if cache is None:
        cache = {'id': -1}
        snmpEngine.setUserContext(getNotificationInfo=cache)

    if cache['id'] != snmpNotifyEntry.branchVersionId:
        cache['targetToNotifyMap'] = {}

    targetToNotifyMap = cache['targetToNotifyMap']

    if notificationTarget not in targetToNotifyMap:
        snmpNotifyTag, snmpNotifyType = mibBuilder.importSymbols(
            'SNMP-NOTIFICATION-MIB', 'snmpNotifyTag', 'snmpNotifyType')

        tblIdx = snmpNotifyEntry.getInstIdFromIndices(notificationTarget)

        try:
            snmpNotifyTag = snmpNotifyTag.getNode(
                snmpNotifyTag.name + tblIdx
            ).syntax

            snmpNotifyType = snmpNotifyType.getNode(
                snmpNotifyType.name + tblIdx
            ).syntax

        except NoSuchInstanceError:
            raise SmiError('Target %s not configured at LCD' % notificationTarget)

        targetToNotifyMap[notificationTarget] = (
            snmpNotifyTag,
            snmpNotifyType
        )

        cache['id'] = snmpNotifyEntry.branchVersionId

    return targetToNotifyMap[notificationTarget]


def getTargetNames(snmpEngine, tag):
    mibBuilder = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder

    snmpTargetAddrEntry, = mibBuilder.importSymbols(
        'SNMP-TARGET-MIB', 'snmpTargetAddrEntry')

    cache = snmpEngine.getUserContext('getTargetNames')
    if cache is None:
        cache = {'id': -1}
        snmpEngine.setUserContext(getTargetNames=cache)

    if cache['id'] == snmpTargetAddrEntry.branchVersionId:
        tagToTargetsMap = cache['tagToTargetsMap']

    else:
        cache['tagToTargetsMap'] = {}

        tagToTargetsMap = cache['tagToTargetsMap']

        (SnmpTagValue, snmpTargetAddrName,
         snmpTargetAddrTagList) = mibBuilder.importSymbols(
            'SNMP-TARGET-MIB', 'SnmpTagValue', 'snmpTargetAddrName',
            'snmpTargetAddrTagList'
        )

        mibNode = snmpTargetAddrTagList

        while True:
            try:
                mibNode = snmpTargetAddrTagList.getNextNode(mibNode.name)

            except NoSuchInstanceError:
                break

            idx = mibNode.name[len(snmpTargetAddrTagList.name):]

            _snmpTargetAddrName = snmpTargetAddrName.getNode(snmpTargetAddrName.name + idx).syntax

            for _tag in mibNode.syntax.asOctets().split():
                _tag = SnmpTagValue(_tag)

                if _tag not in tagToTargetsMap:
                    tagToTargetsMap[_tag] = []

                tagToTargetsMap[_tag].append(_snmpTargetAddrName)

        cache['id'] = snmpTargetAddrEntry.branchVersionId

    if tag not in tagToTargetsMap:
        raise SmiError('Transport tag %s not configured at LCD' % tag)

    return tagToTargetsMap[tag]

# convert cmdrsp/cmdgen into this api
