from typing import Union


def initDataParser(writeOutput: callable) -> callable:

  def dataParser(dataItem: Union[dict, list, str], dataKey: str = None, depth: int = 0) -> None:

    if (type(dataItem) == list):

      for listItem in dataItem:

        dataParser(dataItem=listItem, dataKey=dataKey, depth=depth)

    elif (type(dataItem) == dict):

      writeOutput(lineItem=f"{dataKey.upper()}:", depth=depth)
      primaryKey: str = list(dataItem.keys())[0]
      depth = (depth + 1)

      for key, value in dataItem.items():

        dataParser(dataItem=value, dataKey=key, depth=depth)

    else:

      writeOutput(lineItem=f"{dataKey.upper()}: {dataItem}", depth=depth)

  return dataParser
