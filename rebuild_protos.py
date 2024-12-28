from pathlib import Path
import shutil
import re
import os
import sys
import sh

# Get directories from environment variables
lnd_dir = Path(os.getenv("APP_DIR", ""))
grpc_client_dir = Path(os.getenv("CLIENT_DIR", ""))

if not lnd_dir or not grpc_client_dir:
    print("Error: APP_DIR or CLIENT_DIR environment variables not set.")
    sys.exit(1)

if not lnd_dir.exists() or not grpc_client_dir.exists():
    print("Error: Double-check that the paths exist!")
    sys.exit(1)

compiled_dir = grpc_client_dir.joinpath("lndgrpc/compiled/")
compiled_dir.mkdir(parents=True, exist_ok=True)

# Copy .proto files
for proto in lnd_dir.rglob("*.proto"):
    print(f"Copying: {proto}")
    shutil.copy(proto, compiled_dir)

# Modify .proto files
for proto in compiled_dir.rglob("*.proto"):
    with open(proto, 'r+') as f:
        text = f.read()
        for pattern, replacement in [
            ('lightning.proto', 'lndgrpc/compiled/lightning.proto'),
            ('verrpc/verrpc.proto', 'lndgrpc/compiled/verrpc.proto'),
            ('signrpc/signer.proto', 'lndgrpc/compiled/signer.proto'),
        ]:
            if re.search(pattern, text):
                print(f" - Replacing '{pattern}' with '{replacement}' in {proto.name}")
                text = re.sub(pattern, replacement, text)
        f.seek(0)
