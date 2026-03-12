import urllib.request
import urllib.error
import socket
import sys

SERVER_ADDRESS = "127.0.0.1:8188"
URL = f"http://{SERVER_ADDRESS}"

print(f"📡 Checking ComfyUI connection at {URL} ...")

# 1. Check TCP Port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.settimeout(2)
    s.connect(("127.0.0.1", 8188))
    print("✅ TCP Port 8188 is OPEN")
    s.close()
except Exception as e:
    print(f"❌ TCP Port 8188 is CLOSED: {e}")
    print("   👉 ACTION: Start ComfyUI (run_nvidia_gpu.bat or python main.py)")
    sys.exit(1)

# 2. Check HTTP API
try:
    with urllib.request.urlopen(f"{URL}/history") as response:
        if response.status == 200:
            print("✅ ComfyUI API is RESPONDING")
        else:
            print(f"⚠️ ComfyUI API returned status: {response.status}")
except urllib.error.URLError as e:
    print(f"❌ ComfyUI API Unreachable: {e}")
    sys.exit(1)

print("\n🎉 ComfyUI is RUNNING and READY!")
