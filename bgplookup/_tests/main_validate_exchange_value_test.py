from asyncclick.core import Context, Option
from asyncclick.exceptions import BadParameter

import pytest

from main import validateExchange


def testValidateExchange_enterIxLowValue_returnBadParameterException():

  testIxValue: int = 0
  sut: int = -1

  with pytest.raises(BadParameter) as exception:

    sut = validateExchange(ctx=Context, option=Option, ixValue=testIxValue)

  assert sut == -1
  assert exception.match('0 - must be an integer between 1 and 853.')
  assert exception.type == BadParameter


def testValidateExchange_enterIxLowThresholdValue_returnLowThreshold():

  testIxValue: int = 1
  sut: int = -1

  sut = validateExchange(ctx=Context, option=Option, ixValue=testIxValue)

  assert sut == 1


def testValidateExchange_enterIxHighThresholdValue_returnHighThreshold():

  testIxValue: int = 853
  sut: int = -1

  sut = validateExchange(ctx=Context, option=Option, ixValue=testIxValue)

  assert sut == 853


def testValidateExchange_enterIxHighValue_returnBadParameterException():

  testIxValue: int = 854
  sut: int = -1

  with pytest.raises(BadParameter) as exception:

    sut = validateExchange(ctx=Context, option=Option, ixValue=testIxValue)

  assert sut == -1
  assert exception.match('854 - must be an integer between 1 and 853.')
  assert exception.type == BadParameter
