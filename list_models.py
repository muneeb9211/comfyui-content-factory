import urllib.request
import json
import sys
import os

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

SERVER_ADDRESS = "127.0.0.1:8188"
URL = f"http://{SERVER_ADDRESS}/object_info/CheckpointLoaderSimple"

print(f"Fetching checkpoints from {URL} ...")

try:
    with urllib.request.urlopen(URL) as response:
        data = json.loads(response.read())
        # The structure is usually data['CheckpointLoaderSimple']['input']['required']['ckpt_name'][0]
        checkpoints = data.get('CheckpointLoaderSimple', {}).get('input', {}).get('required', {}).get('ckpt_name', [])
        
        if isinstance(checkpoints, list) and len(checkpoints) > 0:
            if isinstance(checkpoints[0], list):
                # Sometimes it's a list within a list
                checkpoints = checkpoints[0]
            
            print(f"\nFound {len(checkpoints)} available checkpoints:")
            for i, ckpt in enumerate(checkpoints):
                print(f"  {i+1}. {ckpt}")
        else:
            print("\nWARNING: No checkpoints found! Your ComfyUI 'models/checkpoints' folder might be empty.")
            
except Exception as e:
    print(f"❌ Failed to fetch checkpoints: {e}")
    sys.exit(1)
