import os, sys
import httpx
from httpx._exceptions import ConnectTimeout
import socket


def initGetRequest(protocol: str, hostname: str) -> callable:

  async def httpGetRequest(uri: str) -> list:

    try:

      async with httpx.AsyncClient(verify=False) as client:

        response: dict = (await client.get(url=f"{protocol}{hostname}/{uri}")).json()

        if (response['status'] != 'ok'):

          print(f"Error: Response for '{protocol}{hostname}/{uri}' returned with '{response['status_message']}'. Check the request via Postman.")
          os._exit(1)

        else:

          return response['data']

    except socket.gaierror as ex:

      print(f"Error: Request to '{protocol}{hostname}/{uri}' failed with '{ex}'. Check the request via Postman.")
      sys.exit(1)

    except ConnectTimeout:

      print(f"Error: Request to '{protocol}{hostname}/{uri}' timed out. Check the request via Postman.")
      sys.exit(1)

    except:

      print(f"Error: Request to '{protocol}{hostname}/{uri}' failed in some unspectacular (and poorly handled) fashion.")
      raise
      sys.exit(1)

  return httpGetRequest
