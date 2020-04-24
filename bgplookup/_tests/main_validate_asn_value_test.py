from asyncclick.core import Context, Option
from asyncclick.exceptions import BadParameter

import pytest

from main import validateAsn


def testValidateAsn_enterAsnLowValue_returnBadParameterException():

  testAsnValue: int = 0
  sut: int = -1

  with pytest.raises(BadParameter) as exception:

    sut = validateAsn(ctx=Context, option=Option, asnValue=testAsnValue)

  assert sut == -1
  assert exception.match('0 - must be an integer between 1 and 64496.')
  assert exception.type == BadParameter


def testValidateAsn_enterAsnLowThresholdValue_returnLowThreshold():

  testAsnValue: int = 1
  sut: int = -1

  sut = validateAsn(ctx=Context, option=Option, asnValue=testAsnValue)

  assert sut == 1


def testValidateAsn_enterAsnHighThresholdValue_returnHighThreshold():

  testAsnValue: int = 64496
  sut: int = -1

  sut = validateAsn(ctx=Context, option=Option, asnValue=testAsnValue)

  assert sut == 64496


def testValidateAsn_enterAsnHighValue_returnBadParameterException():

  testAsnValue: int = 64497
  sut: int = -1

  with pytest.raises(BadParameter) as exception:

    sut = validateAsn(ctx=Context, option=Option, asnValue=testAsnValue)

  assert sut == -1
  assert exception.match('64497 - must be an integer between 1 and 64496.')
  assert exception.type == BadParameter
