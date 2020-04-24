from ipaddress import IPv4Network, IPv6Network
from typing import List, Union


async def getPrefixData(getRequest: callable, parseDataItem: callable, prefix: Union[IPv4Network, IPv6Network], dataKeys: List[str]) -> dict:

  response: dict = await getRequest(uri=f"prefix/{prefix}")

  if (len(dataKeys) != 0):

    for dataKey in dataKeys:

      try:

        parseDataItem(dataItem=response[dataKey.lower()], dataKey=dataKey)

      except:

        print(f"\nError: Data key '{dataKey}' not found.")

  else:

    parseDataItem(dataItem=response, dataKey='prefix')

  return response
