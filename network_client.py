"""
network_client.py

Handles WebSocket client logic for the Player App.
Connects to the DM App, listens for broadcast events like 'gandor_chat'.
"""

import asyncio
import json
import threading
import websockets
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NetworkClient")


class NetworkClient:
    def __init__(self, uri="ws://localhost:8765", token="default_token"):
        self.uri = uri
        self.token = token
        self.hooks = {}  # Hook registry for incoming events
        self.thread = threading.Thread(target=self._run, daemon=True)

    def register_hook(self, hook_name, callback):
        """
        Register a function to be triggered on a specific event.

        Args:
            hook_name (str): Name of the event (e.g., 'gandor_chat')
            callback (function): Function to call when event is received
        """
        self.hooks[hook_name] = callback
        logger.info(f"Hook registered for: {hook_name}")

    def start(self):
        self.thread.start()

    def _run(self):
        asyncio.run(self._listen())

    async def _listen(self):
        try:
            async with websockets.connect(self.uri) as websocket:
                await websocket.send(json.dumps({"token": self.token}))
                logger.info("Connected to DM server via WebSocket.")

                while True:
                    raw_msg = await websocket.recv()
                    msg = json.loads(raw_msg)
                    event = msg.get("event")
                    payload = msg.get("payload", {})

                    logger.debug(f"Received event: {event} with payload: {payload}")

                    if event in self.hooks:
                        self.hooks[event](payload)
                    else:
                        logger.warning(f"No hook registered for event: {event}")
        except Exception as e:
            logger.error(f"NetworkClient error: {e}")
