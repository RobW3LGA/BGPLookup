import asyncio

from typing import List, Tuple

import pytest

from _models import CliOption
from main import main


testValidAsnResponse: dict = {
  "status": "ok",
  "status_message": "Query was successful",
  "data": {
    "asn": 1234,
    "name": "TEST-ASN",
    "rir_allocation": {
      "rir_name": "APNIC",
      "country_code": "JP",
      "date_allocated": "2011-04-12 00:00:00",
      "allocation_status": "assigned"
    }
  }
}

testValidAsnPeersResponse: dict = {
  "status": "ok",
  "status_message": "Query was successful",
  "data": {
    "ipv4_peers": [
      {      
        "asn": 9876,
        "name": "TEST-IPv4PEER"
      }
    ],
    "ipv6_peers": [
      {
        "asn": 9875,
        "name": "TEST-IPv6PEER"
      }
    ]
  }
}

testErrorAsnResponse: dict = {
    "status": "error",
    "status_message": "Malformed input",
    "@meta": {
        "time_zone": "UTC",
        "api_version": 1,
        "execution_time": "0.73 ms"
    }
}

testUri: str = None
testOutput: List[Tuple] = list(tuple())


def outputTest(lineItem: str, depth: int = 0) -> None:

  testOutput.append((lineItem, depth))


def initTestRequest(response: dict) -> callable:

  async def testRequest(uri: str) -> list:

    testUri = uri

    try:
      
      return response['data']

    except:

      return response

  return testRequest


@pytest.mark.asyncio
async def testGetAsnData_enterBaseAsn_returnRootAsnData():

  testOption: dict = { 'asn': 1234, 'peers': False, 'datakeys': list() }

  sut: dict = await main(cliOption=CliOption(**testOption), getRequest=initTestRequest(testValidAsnResponse), writeOutput=outputTest)

  assert sut['asn'] == 1234
  assert sut['name'] == 'TEST-ASN'
  assert str(testOutput) == "[('ASN:', 0), ('ASN: 1234', 1), ('NAME: TEST-ASN', 1), ('RIR_ALLOCATION:', 1), ('RIR_NAME: APNIC', 2), ('COUNTRY_CODE: JP', 2), ('DATE_ALLOCATED: 2011-04-12 00:00:00', 2), ('ALLOCATION_STATUS: assigned', 2)]"


@pytest.mark.asyncio
async def testGetAsnData_enterBaseAsnWithPeer_ReturnAsnPeerData():

  testOption: dict = { 'asn': 1234, 'peers': True, 'datakeys': list() }

  sut: dict = await main(cliOption=CliOption(**testOption), getRequest=initTestRequest(testValidAsnPeersResponse), writeOutput=outputTest)

  assert sut['ipv4_peers'][0]['asn'] == 9876
  assert sut['ipv4_peers'][0]['name'] == 'TEST-IPv4PEER'
  assert sut['ipv6_peers'][0]['asn'] == 9875
  assert sut['ipv6_peers'][0]['name'] == 'TEST-IPv6PEER'
  assert str(testOutput) == "[('ASN:', 0), ('ASN: 1234', 1), ('NAME: TEST-ASN', 1), ('RIR_ALLOCATION:', 1), ('RIR_NAME: APNIC', 2), ('COUNTRY_CODE: JP', 2), ('DATE_ALLOCATED: 2011-04-12 00:00:00', 2), ('ALLOCATION_STATUS: assigned', 2), ('IPV4:', 0), ('ASN: 9876', 1), ('NAME: TEST-IPv4PEER', 1), ('IPV6:', 0), ('ASN: 9875', 1), ('NAME: TEST-IPv6PEER', 1)]"


@pytest.mark.asyncio
async def testGetAsnData_enterBaseAsnWithDatakey_returnRootAsnDatakeyData():

  testOption: dict = { 'asn': 1234, 'peers': False, 'datakeys': ['rir_allocation'] }

  sut: dict = await main(cliOption=CliOption(**testOption), getRequest=initTestRequest(testValidAsnResponse), writeOutput=outputTest)

  assert sut['asn'] == 1234
  assert str(testOutput) == "[('ASN:', 0), ('ASN: 1234', 1), ('NAME: TEST-ASN', 1), ('RIR_ALLOCATION:', 1), ('RIR_NAME: APNIC', 2), ('COUNTRY_CODE: JP', 2), ('DATE_ALLOCATED: 2011-04-12 00:00:00', 2), ('ALLOCATION_STATUS: assigned', 2), ('IPV4:', 0), ('ASN: 9876', 1), ('NAME: TEST-IPv4PEER', 1), ('IPV6:', 0), ('ASN: 9875', 1), ('NAME: TEST-IPv6PEER', 1), ('RIR_ALLOCATION:', 0), ('RIR_NAME: APNIC', 1), ('COUNTRY_CODE: JP', 1), ('DATE_ALLOCATED: 2011-04-12 00:00:00', 1), ('ALLOCATION_STATUS: assigned', 1)]"


@pytest.mark.asyncio
async def testGetAsnData_enterBadBaseAsn_returnErrorData():

  testOption: dict = { 'asn': 1234, 'peers': False, 'datakeys': list() }

  sut: dict = await main(cliOption=CliOption(**testOption), getRequest=initTestRequest(testErrorAsnResponse), writeOutput=outputTest)

  assert sut['status_message'] == 'Malformed input'
