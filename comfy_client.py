import websocket
import uuid
import json
import urllib.request
import urllib.parse
import time
import os
from typing import Dict, Optional

class ComfyUIClient:
    def __init__(self, server_address="127.0.0.1:8188"):
        self.server_address = server_address
        self.client_id = str(uuid.uuid4())
        self.ws = None

    def connect(self):
        """Establish WebSocket connection for real-time updates"""
        try:
            self.ws = websocket.WebSocket()
            self.ws.connect(f"ws://{self.server_address}/ws?clientId={self.client_id}")
            return True
        except Exception as e:
            print(f"❌ ComfyUI Connection Failed: {e}")
            return False

    def queue_prompt(self, prompt: Dict) -> Optional[str]:
        """Submit a workflow to the queue"""
        p = {"prompt": prompt, "client_id": self.client_id}
        data = json.dumps(p).encode("utf-8")
        try:
            req = urllib.request.Request(f"http://{self.server_address}/prompt", data=data)
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read())["prompt_id"]
        except urllib.error.HTTPError as e:
            print(f"❌ Queue Failed: {e.code} {e.reason}")
            try:
                print(f"Server Response: {e.read().decode('utf-8')}")
            except:
                pass
            return None
        except urllib.error.URLError as e:
            print(f"❌ Queue Failed: ComfyUI Connection Refused ({e.reason})")
            print("   👉 check if ComfyUI is running at 127.0.0.1:8188")
            return None
        except Exception as e:
            print(f"❌ Queue Failed: {e}")
            return None

    def get_image(self, filename: str, subfolder: str, folder_type: str):
        """Retrieve generated image data"""
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        with urllib.request.urlopen(f"http://{self.server_address}/view?{url_values}") as response:
            return response.read()

    def get_history(self, prompt_id: str) -> Dict:
        """Get execution history for a specific prompt_id"""
        with urllib.request.urlopen(f"http://{self.server_address}/history/{prompt_id}") as response:
            return json.loads(response.read())

    def get_checkpoints(self) -> list:
        """List available checkpoints"""
        try:
            # It calls this URL: http://127.0.0.1:8188/object_info/CheckpointLoaderSimple
            with urllib.request.urlopen(f"http://{self.server_address}/object_info/CheckpointLoaderSimple") as response:
                data = json.loads(response.read())
                # Then it parses the giant JSON to find the list of filenames
                return data.get('CheckpointLoaderSimple', {}).get('input', {}).get('required', {}).get('ckpt_name', [])[0]
        except Exception as e:
            print(f"❌ Failed to fetch checkpoints: {e}")
            return [] 
           

    def wait_for_completion(self, prompt_id: str) -> Dict:
        """Wait for the workflow to complete and return outputs"""
        while True:
            out = self.ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                if message["type"] == "executing":
                    data = message["data"]
                    if data["node"] is None and data["prompt_id"] == prompt_id:
                        # Execution finished
                        break
        return self.get_history(prompt_id)[prompt_id]

    def generate_image(self, workflow: Dict, output_node_id: str) -> Optional[Dict]:
        """High-level function to generate an image from a workflow"""
        if not self.ws:
            if not self.connect():
                return None

        prompt_id = self.queue_prompt(workflow)
        if not prompt_id:
            return None
        
        # Wait for completion
        history = self.wait_for_completion(prompt_id)
        
        # Extract outputs
        outputs = history.get("outputs", {}).get(output_node_id, {}).get("images", [])
        return outputs[0] if outputs else None
