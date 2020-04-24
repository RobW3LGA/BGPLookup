from pydantic import BaseModel
from ipaddress import IPv4Network, IPv6Network
from typing import List, Union


class CliOption(BaseModel):

  asn: int = None
  peers: bool = False
  exchange: int = None
  prefix: Union[IPv4Network, IPv6Network] = None
  datakeys: List[str] = None
