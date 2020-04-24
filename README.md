# BGPLookup
A sandcastle built with a bulldozer.

# Project: Build a CLI tool using Python

This started out as a simple project to build a Python utility library and explore WebAPI and RESTConf. The result was an experiment into async calls using [Click/AsyncClick][github_asyncclick], [HTTPX][github_httpx], [pydantic][github_pydantic] for strong typing and [pytest][github_pytest] as an intro to dependency injection and [Functional Python][pythondocs_functional]

All API calls are provided by [BGPView][bgpview_docs]. For valid data, try [Postman][postman_docs] to view https://api.bgpview.io/search

## Installation

### Python version check (minimum) from a virtual environment session:
```
(0.1.0) C:\[Projects Folder]\bgplookup-project\0.1.0>python --version
Python 3.6.10
```

### Install into virtual environment session after download/clone:
```
(0.1.0) C:\[Projects Folder]\bgplookup-project\0.1.0>pip install -e ./BGPLookup-master
...
```

## Examples
### Example One (and a good starting point):
```
(0.1.0) C:\[Projects Folder]\bgplookup-project\0.1.0>bgplookup --help
Usage: bgplookup [OPTIONS] [DATAKEYS]...

Options:
  --asn INTEGER            Target host is 'https://api.bgpview.io'.
                           Provide details for given ASN (1-64496).
                           Follow with optional datakeys (space separated).
  --peers                  Provide peer details for given ASN.
  -ix, --exchange INTEGER  Provide details for given Inet Exchange (1-853).
                           Follow with optional datakeys (space separated).
  --prefix TEXT            The base IP address/Length of the announced prefix.
                           Follow with optional datakeys (space separated).
  --debug                  Output the raw JSON response, if received.
  -v, --version            Show version and exit.
  --help                   Show this message and exit.
```

### Example Two:
```
(0.1.0) C:\[Projects Folder]\bgplookup-project\0.1.0>bgplookup --asn 61138
```

This command is the equivalent to the API call: https://api.bgpview.io/asn/61138

### Example Three:
```
(0.1.0) C:\[Projects Folder]\bgplookup-project\0.1.0>bgplookup --asn 61138 --peers
```

This command is the equivalent to the API call: https://api.bgpview.io/asn/61138/peers

### Example Four:
```
(0.1.0) C:\[Projects Folder]\bgplookup-project\0.1.0>bgplookup --prefix 192.209.63.0/24 ASNS RIR_ALLOCATION IANA_ASSIGNMENT
```

For a bit of fun, the challenge was to isolate and display selected first-level data groups

### Special thank you to the fine folks at [World Wide Technology][wwt_website] for the guidance and inspiration

[github_asyncclick]: https://github.com/click-contrib/asyncclick
[github_httpx]: https://github.com/encode/httpx
[github_pydantic]: https://github.com/samuelcolvin/pydantic
[github_pytest]: https://github.com/pytest-dev/pytest
[pythondocs_functional]: https://docs.python.org/3/howto/functional.html
[bgpview_docs]: https://bgpview.docs.apiary.io
[bgpview_search]: https://api.bgpview.io/search
[postman_docs]: https://learning.postman.com/docs/postman/launching-postman/introduction
[wwt_website]: https://www.wwt.com
