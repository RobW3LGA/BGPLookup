from pydantic import BaseModel


class AppState(BaseModel):

  appName: str = None
  appVersion: str = None
  asnLowValue: int = 0
  asnHighValue: int = 0
  ixLowValue: int = 0
  ixHighValue: int = 0
  protocol: str = None
  hostname: str = None
