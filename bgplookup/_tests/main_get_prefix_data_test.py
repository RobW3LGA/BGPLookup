import asyncio

from typing import List, Tuple

import pytest

from _models import CliOption
from main import main

testValidPrefixResponse: dict = {
  "status": "ok",
  "status_message": "Query was successful",
  "data": {
    "prefix": "192.168.0.0/24",
    "ip": "192.168.0.0",
    "cidr": 12,
    "asns": [
      {
        "asn": 3456,
        "name": "APNIC-AS-X-BLOCK",
        "description": "Asia Pacific Network Information Centre",
        "country_code": "AU",
        "prefix_upstreams": [
          {
            "asn": 7890,
            "name": "NTT-COMMUNICATIONS-2914",
            "description": "NTT America, Inc.",
            "country_code": "US"
          }
        ]
      }
    ],
    "rir_allocation": {
      "rir_name": "APNIC",
      "country_code": "JP",
      "ip": "1.1.64.0",
      "cidr": 18,
      "prefix": "1.1.64.0/18",
      "date_allocated": "2011-04-12 00:00:00",
      "allocation_status": "allocated"
    }
  }
}

testValidPrefixBadDatakeyResponse: dict = {
  "status": "ok",
  "status_message": "Query was successful",
  "data": {
    "prefix": "192.168.0.0/24",
    "ip": "192.168.0.0",
    "cidr": 12,
  }
}

testErrorPrefixResponse: dict = {
  "status": "error",
  "status_message": "Prefix not found in BGP table or malformed",
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
async def testGetPrefixData_enterBasePrefix_returnRootPrefixData():

  testOption: dict = { 'prefix': '192.168.0.0/24', 'datakeys': list() }

  sut: dict = await main(cliOption=CliOption(**testOption), getRequest=initTestRequest(testValidPrefixResponse), writeOutput=outputTest)

  assert sut['ip'] == '192.168.0.0'
  assert str(testOutput) == "[('PREFIX:', 0), ('PREFIX: 192.168.0.0/24', 1), ('IP: 192.168.0.0', 1), ('CIDR: 12', 1), ('ASNS:', 1), ('ASN: 3456', 2), ('NAME: APNIC-AS-X-BLOCK', 2), ('DESCRIPTION: Asia Pacific Network Information Centre', 2), ('COUNTRY_CODE: AU', 2), ('PREFIX_UPSTREAMS:', 2), ('ASN: 7890', 3), ('NAME: NTT-COMMUNICATIONS-2914', 3), ('DESCRIPTION: NTT America, Inc.', 3), ('COUNTRY_CODE: US', 3), ('RIR_ALLOCATION:', 1), ('RIR_NAME: APNIC', 2), ('COUNTRY_CODE: JP', 2), ('IP: 1.1.64.0', 2), ('CIDR: 18', 2), ('PREFIX: 1.1.64.0/18', 2), ('DATE_ALLOCATED: 2011-04-12 00:00:00', 2), ('ALLOCATION_STATUS: allocated', 2)]"


@pytest.mark.asyncio
async def testGetPrefixData_enterBasePrefixWithDatakey_returnRootPrefixDatakeyData():

  testOption: dict = { 'prefix': '192.168.0.0/24', 'datakeys': ['ASNS', 'rir_allocation'] }

  sut: dict = await main(cliOption=CliOption(**testOption), getRequest=initTestRequest(testValidPrefixResponse), writeOutput=outputTest)

  assert sut['ip'] == '192.168.0.0'
  assert str(testOutput) == "[('PREFIX:', 0), ('PREFIX: 192.168.0.0/24', 1), ('IP: 192.168.0.0', 1), ('CIDR: 12', 1), ('ASNS:', 1), ('ASN: 3456', 2), ('NAME: APNIC-AS-X-BLOCK', 2), ('DESCRIPTION: Asia Pacific Network Information Centre', 2), ('COUNTRY_CODE: AU', 2), ('PREFIX_UPSTREAMS:', 2), ('ASN: 7890', 3), ('NAME: NTT-COMMUNICATIONS-2914', 3), ('DESCRIPTION: NTT America, Inc.', 3), ('COUNTRY_CODE: US', 3), ('RIR_ALLOCATION:', 1), ('RIR_NAME: APNIC', 2), ('COUNTRY_CODE: JP', 2), ('IP: 1.1.64.0', 2), ('CIDR: 18', 2), ('PREFIX: 1.1.64.0/18', 2), ('DATE_ALLOCATED: 2011-04-12 00:00:00', 2), ('ALLOCATION_STATUS: allocated', 2), ('ASNS:', 0), ('ASN: 3456', 1), ('NAME: APNIC-AS-X-BLOCK', 1), ('DESCRIPTION: Asia Pacific Network Information Centre', 1), ('COUNTRY_CODE: AU', 1), ('PREFIX_UPSTREAMS:', 1), ('ASN: 7890', 2), ('NAME: NTT-COMMUNICATIONS-2914', 2), ('DESCRIPTION: NTT America, Inc.', 2), ('COUNTRY_CODE: US', 2), ('RIR_ALLOCATION:', 0), ('RIR_NAME: APNIC', 1), ('COUNTRY_CODE: JP', 1), ('IP: 1.1.64.0', 1), ('CIDR: 18', 1), ('PREFIX: 1.1.64.0/18', 1), ('DATE_ALLOCATED: 2011-04-12 00:00:00', 1), ('ALLOCATION_STATUS: allocated', 1)]"


@pytest.mark.asyncio
async def testGetPrefixData_enterBasePrefix_returnRootPrefixBadDatakeyError():

  testOption: dict = { 'prefix': '192.168.0.0/24', 'datakeys': ['ASNS', 'rir_allocation'] }

  sut: dict = await main(cliOption=CliOption(**testOption), getRequest=initTestRequest(testValidPrefixBadDatakeyResponse), writeOutput=outputTest)

  assert sut['ip'] == '192.168.0.0'
  assert str(testOutput) == "[('PREFIX:', 0), ('PREFIX: 192.168.0.0/24', 1), ('IP: 192.168.0.0', 1), ('CIDR: 12', 1), ('ASNS:', 1), ('ASN: 3456', 2), ('NAME: APNIC-AS-X-BLOCK', 2), ('DESCRIPTION: Asia Pacific Network Information Centre', 2), ('COUNTRY_CODE: AU', 2), ('PREFIX_UPSTREAMS:', 2), ('ASN: 7890', 3), ('NAME: NTT-COMMUNICATIONS-2914', 3), ('DESCRIPTION: NTT America, Inc.', 3), ('COUNTRY_CODE: US', 3), ('RIR_ALLOCATION:', 1), ('RIR_NAME: APNIC', 2), ('COUNTRY_CODE: JP', 2), ('IP: 1.1.64.0', 2), ('CIDR: 18', 2), ('PREFIX: 1.1.64.0/18', 2), ('DATE_ALLOCATED: 2011-04-12 00:00:00', 2), ('ALLOCATION_STATUS: allocated', 2), ('ASNS:', 0), ('ASN: 3456', 1), ('NAME: APNIC-AS-X-BLOCK', 1), ('DESCRIPTION: Asia Pacific Network Information Centre', 1), ('COUNTRY_CODE: AU', 1), ('PREFIX_UPSTREAMS:', 1), ('ASN: 7890', 2), ('NAME: NTT-COMMUNICATIONS-2914', 2), ('DESCRIPTION: NTT America, Inc.', 2), ('COUNTRY_CODE: US', 2), ('RIR_ALLOCATION:', 0), ('RIR_NAME: APNIC', 1), ('COUNTRY_CODE: JP', 1), ('IP: 1.1.64.0', 1), ('CIDR: 18', 1), ('PREFIX: 1.1.64.0/18', 1), ('DATE_ALLOCATED: 2011-04-12 00:00:00', 1), ('ALLOCATION_STATUS: allocated', 1)]"
