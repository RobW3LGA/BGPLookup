import os, sys, json

import asyncclick as click
from asyncclick.core import Context, Option

import ipaddress
from ipaddress import IPv4Network, IPv6Network

from typing import List, Tuple, Union

from _models import AppState, CliOption
from _settings import appState
from _utilities import initDataParser, initGetRequest, outputConsole
from _actions import getAsnData, getExchangeData, getPrefixData

state: AppState = AppState(**appState)


def validateAsn(ctx: Context, option: Option, asnValue: int) -> int:

  if asnValue is not None and ((type(asnValue) != int) or (asnValue not in range(state.asnLowValue, (state.asnHighValue + 1)))):

    raise click.BadParameter(f"{asnValue} - must be an integer between {state.asnLowValue} and {state.asnHighValue}.")
    sys.exit(1)

  return asnValue


def validateExchange(ctx: Context, option: Option, ixValue: int) -> int:

  if ixValue is not None and ((type(ixValue) != int) or (ixValue not in range(state.ixLowValue, (state.ixHighValue + 1)))):

    raise click.BadParameter(f"{ixValue} - must be an integer between {state.ixLowValue} and {state.ixHighValue}.")
    sys.exit(1)

  return ixValue


def validatePrefix(ctx: Context, option: Option, prefixValue: Union[IPv4Network, IPv6Network]) -> Union[IPv4Network, IPv6Network]:

  validPrefix: Union[IPv4Network, IPv6Network] = None
  if prefixValue is not None:

    try:

      validPrefix = ipaddress.ip_network(prefixValue)

    except Exception:

      raise click.BadParameter(f"{prefixValue} is an invalid network/mask.")
      sys.exit(1)

  return validPrefix


def validateVersion(ctx: Context, option: Option, switchValue: bool) -> None:

  if not switchValue or ctx.resilient_parsing:

    return

  click.echo(f"{state.appName} {state.appVersion}")
  ctx.exit()


async def main(cliOption: CliOption, getRequest: callable, writeOutput: callable) -> dict:

  if (cliOption.asn is not None):

    return await getAsnData(getRequest=getRequest, parseDataItem=initDataParser(writeOutput=writeOutput), asn=cliOption.asn, peers=cliOption.peers, dataKeys=cliOption.datakeys)

  elif (cliOption.exchange is not None):

    return await getExchangeData(getRequest=getRequest, parseDataItem=initDataParser(writeOutput=writeOutput), exchange=cliOption.exchange, dataKeys=cliOption.datakeys)

  elif (cliOption.prefix is not None):

    return await getPrefixData(getRequest=getRequest, parseDataItem=initDataParser(writeOutput=writeOutput), prefix=cliOption.prefix, dataKeys=cliOption.datakeys)

  else:

    print(f"Error: No options selected. Try '{state.appName} --help' for help.")
    sys.exit()


@click.command()
@click.option('--asn', type=int, callback=validateAsn, help=f"Target host is '{state.protocol}{state.hostname}'.\tProvide details for given ASN ({state.asnLowValue}-{state.asnHighValue}).\tFollow with optional datakeys (space separated).")
@click.option('--peers', is_flag=True, default=False, help=f"Provide peer details for given ASN.")
@click.option('--exchange', '-ix', type=int, callback=validateExchange, help=f"Provide details for given Inet Exchange ({state.ixLowValue}-{state.ixHighValue}).\tFollow with optional datakeys (space separated).")
@click.option('--prefix', type=str, callback=validatePrefix, help="The base IP address/Length of the announced prefix.\tFollow with optional datakeys (space separated).")
@click.argument('datakeys', type=str, nargs=-1)
@click.option('--debug', is_flag=True, help="Output the raw JSON response, if received.")
@click.option('--version', '-v', is_flag=True, callback=validateVersion, expose_value=False, is_eager=True, help="Show version and exit.")
async def parseCli(asn: int, peers: bool, exchange: int, prefix: IPv4Network, datakeys: Tuple, debug: bool) -> None:

  datakeyList: List[str] = list(datakeys)

  cliOption: dict = {

    'asn': asn,
    'peers': peers,
    'exchange': exchange,
    'prefix': prefix,
    'datakeys': datakeyList
  }

  result: dict = await main(cliOption=CliOption(**cliOption), getRequest=initGetRequest(protocol=state.protocol, hostname=state.hostname), writeOutput=outputConsole)

  if debug and (result is not None) and (len(result) != 0):

    print(f"\nDEBUG OUTPUT: {result}")

  sys.exit()


if __name__ == '__main__':

  parseCli(_anyio_backend="asyncio")
