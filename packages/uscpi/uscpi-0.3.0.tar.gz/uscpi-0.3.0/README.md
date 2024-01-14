# &mu;SCPI

An asynchronous SCPI instrumentation library.

## Install

### PyPI

Installing the latest release from [PyPI](https://pypi.org).

```console
pip install -U uscpi
```

### Repository

When using [git](https://git-scm.com), clone the repository and 
change your present working directory.

```console
git clone http://github.com/mcpcpc/uscpi
cd uscpi/
```

Create and activate a virtual environment.

```console
python3 -m venv venv
source venv/bin/activate
```

Install &mu;SCPI to the virtual environment.

```console
pip install -e .
```

## Usage

### Asynchronous

A basic example using the *asyncio* library.

```python
from asyncio import run
from uscpi import TCP
from uscpi import Instrument

client = TCP(host="127.0.0.1", port=5025)
instrument = Instrument(client=client)

async def main():
    response = await instrument.idn()
    print(response)

if __name__ == "__main__":
     run(main())
```

### Connection Timeout

By default, &mu;SCPI will wait indefinitely for a connection to 
be established. If the `timeout` property is defined, an 
*asyncio.TimeoutError* will be raised after the specified 
connection time period (in seconds) is exceeded.

```python
TCP(host="127.0.0.1", port=5025, timeout=0.1)
```

### Automatic Connection Management

To ensure proper connection cleanup, the built-in asynchronous
context manager can be used. 

```python
async def main():
    async with TCP("127.0.0.1", 8080) as client:
        instrument = Instrument(client=client)
        response = await instrument.idn()
        print(response)
```

### Event Callbacks

There are four user callback functions that can be implemented 
and executed when a corresponding event is triggered:
`connection_made_cb`, `connection_lost_cb`, `data_received_cb`, 
and `eof_received_cb`. Each callable object must be passed to 
the client method during instantiation. 

```python
def user_cb():
    print("Connection made!")

TCP(host="127.0.0.1", port=5025, connection_made_cb=user_cb)
```

## Features

&mu;SCPI is fairly lightweight and leaves a majority of 
instrument function commands to be implemented by the user. 
Nonetheless, the following IEEE-488.2 commands have been 
implemented:

- Clear Status Command
- Event Status Enable Command and Query
- Standard Event Status Register Query
- Identification Query
- Reset Command
- Service Request Enable Command and Query
- Read Status Byte Query
- Trigger Command
- Self-Test Query
- Wait-to-Continue Command

You can learn more about each of these commands by using the 
built-in `help` method.

```pycon
>>> from uscpi import Instrument
>>> help(Instrument)
```

## Credits

- [sockio](https://github.com/tiagocoutinho/sockio)
- [IEEE 488.2-1978 Protocol](https://ieeexplore.ieee.org/document/19528)
- [IEEE 488.2 Common Commands](https://rfmw.em.keysight.com/spdhelpfiles/truevolt/webhelp/US/Content/__I_SCPI/IEEE-488_Common_Commands.htm)
