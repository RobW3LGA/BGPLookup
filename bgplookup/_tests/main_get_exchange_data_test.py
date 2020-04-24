import asyncio

from typing import List, Tuple

import pytest

from _models import CliOption
from main import main

testValidExchangeResponse: dict = {
  "status": "ok",
  "status_message": "Query was successful",
  "data": {
    "name": "TEST-IX",
    "members": [
      {
        "asn": 1234,
        "name": "TEST-ASN",
        "description": "Test Exchange ASN",
        "country_code": "TST",
        "ipv4_address": "218.100.24.17",
        "ipv6_address": None,
        "speed": 1000
      }
    ]
  }
}

testValidExchangeBadDatakeyResponse: dict = {
  "status": "ok",
  "status_message": "Query was successful",
  "data": {
    "name": "TEST-IX",
    "badmembers": [
      {
        "asn": 1234,
        "name": "TEST-ASN",
        "description": "Test Exchange ASN",
        "country_code": "TST",
        "ipv4_address": "218.100.24.17",
        "ipv6_address": None,
        "speed": 1000
      }
    ]
  }
}

testErrorExchangeResponse: dict = {
  "status": "error",
  "status_message": "Could not find IX",
  "@meta": {
    "time_zone": "UTC",
    "api_version": 1,
    "execution_time": "5.74 ms"
  }
}

testUri: str = None
testOutput: List[Tuple] = list(tuple())


def outputTest(lineItem: str, depth: int = 0) -> None:

  testOutput.append((lineItem, depth))


def initTestRequest(response: dict) -> callable:

  async def testRequest(uri: str) -> list:

    testUri = uri

    return response['data']

  return testRequest


@pytest.mark.asyncio
async def testGetExchangeData_enterBaseExchange_returnRootExchangeData():

  testOption: dict = { 'exchange': 1234, 'datakeys': list() }

  sut: dict = await main(cliOption=CliOption(**testOption), getRequest=initTestRequest(testValidExchangeResponse), writeOutput=outputTest)

  assert sut['name'] == 'TEST-IX'
  assert str(testOutput) == "[('IX:', 0), ('NAME: TEST-IX', 1), ('MEMBERS:', 1), ('ASN: 1234', 2), ('NAME: TEST-ASN', 2), ('DESCRIPTION: Test Exchange ASN', 2), ('COUNTRY_CODE: TST', 2), ('IPV4_ADDRESS: 218.100.24.17', 2), ('IPV6_ADDRESS: None', 2), ('SPEED: 1000', 2)]"


@pytest.mark.asyncio
async def testGetExchangeData_enterBaseExchangeWithDatakey_returnRootExchangeDatakeyData():

  testOption: dict = { 'exchange': 1234, 'datakeys': ['MEMBERS'] }

  sut: dict = await main(cliOption=CliOption(**testOption), getRequest=initTestRequest(testValidExchangeResponse), writeOutput=outputTest)

  assert sut['name'] == 'TEST-IX'
  assert str(testOutput) == "[('IX:', 0), ('NAME: TEST-IX', 1), ('MEMBERS:', 1), ('ASN: 1234', 2), ('NAME: TEST-ASN', 2), ('DESCRIPTION: Test Exchange ASN', 2), ('COUNTRY_CODE: TST', 2), ('IPV4_ADDRESS: 218.100.24.17', 2), ('IPV6_ADDRESS: None', 2), ('SPEED: 1000', 2), ('MEMBERS:', 0), ('ASN: 1234', 1), ('NAME: TEST-ASN', 1), ('DESCRIPTION: Test Exchange ASN', 1), ('COUNTRY_CODE: TST', 1), ('IPV4_ADDRESS: 218.100.24.17', 1), ('IPV6_ADDRESS: None', 1), ('SPEED: 1000', 1)]"


@pytest.mark.asyncio
async def testGetExchangeData_enterBaseExchange_returnRootExchangeBadDatakeyError():

  testOption: dict = { 'exchange': 1234, 'datakeys': ['MEMBERS'] }

  sut: dict = await main(cliOption=CliOption(**testOption), getRequest=initTestRequest(testValidExchangeBadDatakeyResponse), writeOutput=outputTest)

  assert sut['name'] == 'TEST-IX'
  assert str(testOutput) == "[('IX:', 0), ('NAME: TEST-IX', 1), ('MEMBERS:', 1), ('ASN: 1234', 2), ('NAME: TEST-ASN', 2), ('DESCRIPTION: Test Exchange ASN', 2), ('COUNTRY_CODE: TST', 2), ('IPV4_ADDRESS: 218.100.24.17', 2), ('IPV6_ADDRESS: None', 2), ('SPEED: 1000', 2), ('MEMBERS:', 0), ('ASN: 1234', 1), ('NAME: TEST-ASN', 1), ('DESCRIPTION: Test Exchange ASN', 1), ('COUNTRY_CODE: TST', 1), ('IPV4_ADDRESS: 218.100.24.17', 1), ('IPV6_ADDRESS: None', 1), ('SPEED: 1000', 1)]"
