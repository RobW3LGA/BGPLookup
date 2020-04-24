def outputConsole(lineItem: str, depth: int = 0) -> None:

  tabs: str = ''
  level: int = 0
  if (depth != 0):

    while level != depth:

      tabs = f"{tabs}\t"
      level = level + 1

  print(f"{tabs}{lineItem}")
