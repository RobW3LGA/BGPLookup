from asyncclick.core import Context, Option
from asyncclick.exceptions import BadParameter

from ipaddress import IPv4Network, IPv6Network

import pytest

from main import validatePrefix


def testValidatePrefix_enterPrefixInvalidIpv4Value_returnBadParameterException():

  testPrefixValue: str = '192.168.0.0/8'
  sut: str = None

  with pytest.raises(BadParameter) as exception:

    sut = validatePrefix(ctx=Context, option=Option, prefixValue=testPrefixValue)

  assert sut == None
  assert exception.match('192.168.0.0/8 is an invalid network/mask.')
  assert exception.type == BadParameter


def testValidatePrefix_enterPrefixValidIpv4Value_returnValidIpv4Value():

  testPrefixValue: str = '192.168.0.0/24'
  sut: str = -1

  sut = validatePrefix(ctx=Context, option=Option, prefixValue=testPrefixValue)

  assert type(sut) == IPv4Network
  assert str(sut) == '192.168.0.0/24'


def testValidatePrefix_enterPrefixInvalidIpv6Value_returnBadParameterException():

  testPrefixValue: str = '2001:1200:10::/24'
  sut: str = None

  with pytest.raises(BadParameter) as exception:

    sut = validatePrefix(ctx=Context, option=Option, prefixValue=testPrefixValue)

  assert sut == None
  assert exception.match('2001:1200:10::/24 is an invalid network/mask.')
  assert exception.type == BadParameter


def testValidatePrefix_enterPrefixValidIpv6Value_returnValidIpv6Value():

  testPrefixValue: str = '2001:1200:10::/48'
  sut: str = -1

  sut = validatePrefix(ctx=Context, option=Option, prefixValue=testPrefixValue)

  assert type(sut) == IPv6Network
  assert str(sut) == '2001:1200:10::/48'
