from ipaddress import IPv4Network
from typing import List


async def getExchangeData(getRequest: callable, parseDataItem: callable, exchange: int, dataKeys: List[str]) -> dict:

  response: dict = await getRequest(uri=f"ix/{exchange}")

  if (len(dataKeys) != 0):

    for dataKey in dataKeys:

      try:

        parseDataItem(dataItem=response[dataKey.lower()], dataKey=dataKey)

      except:

        print(f"\nError: Data key '{dataKey}' not found.")

  else:

    parseDataItem(dataItem=response, dataKey='ix')

  return response
