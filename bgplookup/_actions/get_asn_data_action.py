from typing import List


async def getAsnData(getRequest: callable, parseDataItem: callable, asn: int, peers: bool, dataKeys: List[str]) -> dict:

  if (peers):

    response: dict = await getRequest(uri=f"asn/{asn}/peers")

    for peer in response['ipv4_peers']:

      parseDataItem(dataItem=peer, dataKey='IPv4')

    for peer in response['ipv6_peers']:

      parseDataItem(dataItem=peer, dataKey='IPv6')

  else:

    response: dict = await getRequest(uri=f"asn/{asn}")

    if (len(dataKeys) != 0):

      for dataKey in dataKeys:

        try:

          parseDataItem(dataItem=response[dataKey.lower()], dataKey=dataKey)

        except:

          print(f"\nError: Data key '{dataKey}' not found.")

    else:

      parseDataItem(dataItem=response, dataKey='asn')

  return response
