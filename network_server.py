"""
network_server.py

Implements a simple WebSocket server for the DM App using websockets 15.x.
Handles inbound connections from Player App clients and broadcasts messages.
"""

import asyncio
import websockets
import threading
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NetworkServer")

class NetworkServer:
    def __init__(self, host='localhost', port=8765):
        self.clients = set()
        self.host = host
        self.port = port
        self.loop = asyncio.new_event_loop()

    async def handle_connection(self, websocket):
        self.clients.add(websocket)
        logger.info("New client connected.")
        try:
            async for message in websocket:
                logger.info(f"Received message from client: {message}")
        except websockets.exceptions.ConnectionClosed:
            logger.info("Client disconnected.")
        finally:
            self.clients.remove(websocket)

    def broadcast(self, event_type, payload):
        message = json.dumps({"event": event_type, "data": payload})
        logger.debug(f"Broadcasting message: {message}")
        asyncio.run_coroutine_threadsafe(self._broadcast(message), self.loop)

    async def _broadcast(self, message):
        if self.clients:
            await asyncio.gather(*[client.send(message) for client in self.clients], return_exceptions=True)

    def start_in_thread(self):
        def run():
            asyncio.set_event_loop(self.loop)
            try:
                self.loop.run_until_complete(self._start_server())
            except Exception as e:
                logger.error(f"Network server error: {e}")
            self.loop.run_forever()

        threading.Thread(target=run, daemon=True).start()
        logger.info("Network server thread started.")

    async def _start_server(self):
        server = await websockets.serve(self.handle_connection, self.host, self.port)
        logger.info(f"NetworkServer initialized on port {self.port}")
        return server
