### This is a fork with minor changes from
https://github.com/kornpow/lnd-grpc-client

-------------------------------------------------------------
# lndgrpclib
A Python GRPC Client Library for LND (Lightning Network Daemon) ⚡⚡⚡

This is a wrapper around the default grpc interface that handles setting up credentials (including macaroons). An async client is also available to do fun async stuff like listening for invoices in the background. 

## Dependencies
- Python 3.8+
- Working LND lightning node, take note of its ip address.
- Copy your admin.macaroon and tls.cert files from your node to a directory on your machine. 


## Installation
```bash
pip install lndgrpclib
```

### CLI Usage
This package adds a CLI command to your PATH once installed:

```bash
lndgrpcclient_cli
```

### Setup

```
$ lndgrpcclient_cli environment

Saving credentials!
Enter your node's IP Address [127.0.0.1]: 86.75.309.69
86.75.309.69
Enter your node's Port [10009]: 
10009
Enter your node's Alias [default-node-alias]: mintblok
mintblok
Where do you want keep your node credentials? Macaroons and tls.cert? [$HOME/lnd]: 
Enter your macaroon filename [admin.macaroon]: 
Build directory structure and save `node-env` file at location: $HOME/.lnd [True]: 1
This environment file must be loaded to access your node!

export LND_CRED_PATH=$HOME/.lnd
export LND_NODE_IP=86.75.309.69
export LND_NODE_PORT=10009
export LND_MACAROON=admin.macaroon
Writing file....
Wrote environment file to location: /home/kevin/.lnd/mintblok/node-env
Enable it by running: source /home/kevin/.lnd/mintblok/node-env
```

```
$ lndgrpcclient_cli credentials --input_format hex --credential_type macaroon

Saving credentials to: $HOME/.lnd/mintblok
Enter your node's macaroon []: abcdef123456
Enter your macaroon name: [admin]:
Enable this macaroon by running:
 export LND_MACAROON=admin.macaroon
Wrote file: $HOME/.lnd/mintblok/admin.macaroon
```

```
$ lndgrpcclient_cli credentials --input_format hex --credential_type tls

Saving credentials to: /home/kevin/.lnd/mintblok
Enter your node's tls []: abcdef1234
Wrote file: /home/kevin/.lnd/mintblok/tls.cert
```


### Usage
```
$ lndgrpcclient_cli shell

>>> lnd.get_info().block_hash
'0000000000000000000873876975b2443cfcb93cd9b66c58ed6da922fe5f40b3'

>>> lnd.get_node_info("0360a41eb8c3fe09782ef6c984acbb003b0e1ebc4fe10ae01bab0e80d76618c8f4").node.alias
'mintblok'

>>> lnd.get_network_info()
graph_diameter: 13
avg_out_degree: 5.528722661077973
max_out_degree: 417
num_nodes: 18609
num_channels: 51442
total_network_capacity: 2873600
avg_channel_size: 55.86096963570623
max_channel_size: 1000000
num_zombie_chans: 165176
```

## Advanced Usage
Go in the `examples` folder for some advanced examples including:
- Open channel using PSBT: `openchannel-external.py`
- Open Batch of Channels using PSBT: `batchopenchannel-external.py`
- Keysend Payments: `send-keysend.py`
- Reconnect to your peers: `reconnect-peers.py`
- Channel Acceptor API w/ a custom failure message: `channel-acceptor.py`

### Async

```python
import asyncio
from lndgrpc import AsyncLNDClient

async_lnd = AsyncLNDClient()

async def subscribe_invoices():
    print('Listening for invoices...')
    async for invoice in async_lnd.subscribe_invoices():
        print(invoice)

async def get_info():
    while True:
        info = await async_lnd.get_info()
        print(info)
        await asyncio.sleep(5)

async def run():
    coros = [subscribe_invoices(), get_info()]
    await asyncio.gather(*coros)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
```

### Specifying Macaroon/Cert files
By default the client will attempt to lookup the `readonly.macaron` and `tls.cert` files in the mainnet directory. 
However if you want to specify a different macaroon or different path you can pass in the filepath explicitly.

```python
lnd = LNDClient(
    macaroon_filepath='$HOME/.lnd/invoice.macaroon', 
    cert_filepath='$HOME/.lnd/tls.cert'
)
```

## Generating LND Proto Files
```
mkvirtualenv gen_rpc_protos
# or 
workon gen_rpc_protos
# then

pip install grpcio grpcio-tools googleapis-common-protos sh

cd lndgrpc
git clone --depth 1 https://github.com/googleapis/googleapis.git
cd ..
```


Set environment
```
cd ~
python3 -m venv lndpython
source lndpython/bin/activate

export APP_DIR=$HOME/.lnd
export CLIENT_DIR=$HOME/lndgrpclib
python3 rebuild_protos.py
pip install -e .
```

## Deploy to Test-PyPi
```bash
poetry build
twine check dist/*
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```howdy
