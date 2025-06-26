"""
WebSocket handler for real-time dashboard communication.
"""

import asyncio
import json
from typing import Dict, List, Optional, Any, Callable
from websockets import WebSocketServerProtocol, serve
from websockets.exceptions import ConnectionClosed


class WebSocketHandler:
    """Handles WebSocket connections for real-time dashboard updates."""
    
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.clients: List[WebSocketServerProtocol] = []
        self.message_handlers: Dict[str, Callable] = {}
        self.analysis_callbacks: List[Callable] = []
        
        # Register default message handlers
        self._register_default_handlers()
    
    def _register_default_handlers(self):
        """Register default message handlers."""
        self.register_handler("ping", self._handle_ping)
        self.register_handler("analyze", self._handle_analyze_request)
        self.register_handler("get_status", self._handle_status_request)
    
    def register_handler(self, message_type: str, handler: Callable):
        """Register a message handler for a specific message type."""
        self.message_handlers[message_type] = handler
    
    def register_analysis_callback(self, callback: Callable):
        """Register a callback for analysis updates."""
        self.analysis_callbacks.append(callback)
    
    async def _handle_ping(self, websocket: WebSocketServerProtocol, data: Dict[str, Any]):
        """Handle ping messages."""
        await websocket.send(json.dumps({
            "type": "pong",
            "timestamp": asyncio.get_event_loop().time()
        }))
    
    async def _handle_analyze_request(self, websocket: WebSocketServerProtocol, data: Dict[str, Any]):
        """Handle analysis requests."""
        codebase_path = data.get("codebase_path")
        if not codebase_path:
            await websocket.send(json.dumps({
                "type": "error",
                "message": "Missing codebase_path"
            }))
            return
        
        # Trigger analysis callbacks
        for callback in self.analysis_callbacks:
            try:
                await callback(codebase_path)
            except Exception as e:
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": f"Analysis failed: {str(e)}"
                }))
    
    async def _handle_status_request(self, websocket: WebSocketServerProtocol, data: Dict[str, Any]):
        """Handle status requests."""
        await websocket.send(json.dumps({
            "type": "status",
            "data": {
                "connected_clients": len(self.clients),
                "server_time": asyncio.get_event_loop().time()
            }
        }))
    
    async def handle_client(self, websocket: WebSocketServerProtocol, path: str):
        """Handle individual WebSocket client connections."""
        # Add client to list
        self.clients.append(websocket)
        
        try:
            # Send welcome message
            await websocket.send(json.dumps({
                "type": "welcome",
                "message": "Connected to Architex WebSocket Server",
                "server_time": asyncio.get_event_loop().time()
            }))
            
            # Handle incoming messages
            async for message in websocket:
                try:
                    data = json.loads(message)
                    message_type = data.get("type")
                    
                    if message_type in self.message_handlers:
                        await self.message_handlers[message_type](websocket, data)
                    else:
                        await websocket.send(json.dumps({
                            "type": "error",
                            "message": f"Unknown message type: {message_type}"
                        }))
                        
                except json.JSONDecodeError:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": "Invalid JSON format"
                    }))
                except Exception as e:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": f"Error processing message: {str(e)}"
                    }))
                    
        except ConnectionClosed:
            pass
        finally:
            # Remove client from list
            if websocket in self.clients:
                self.clients.remove(websocket)
    
    async def broadcast(self, message: Dict[str, Any]):
        """Broadcast a message to all connected clients."""
        if not self.clients:
            return
        
        message_json = json.dumps(message)
        disconnected_clients = []
        
        for client in self.clients:
            try:
                await client.send(message_json)
            except ConnectionClosed:
                disconnected_clients.append(client)
            except Exception as e:
                print(f"Error broadcasting to client: {e}")
                disconnected_clients.append(client)
        
        # Remove disconnected clients
        for client in disconnected_clients:
            if client in self.clients:
                self.clients.remove(client)
    
    async def broadcast_analysis_update(self, analysis_data: Dict[str, Any]):
        """Broadcast analysis update to all clients."""
        await self.broadcast({
            "type": "analysis_update",
            "data": analysis_data,
            "timestamp": asyncio.get_event_loop().time()
        })
    
    async def broadcast_metrics_update(self, metrics_data: Dict[str, Any]):
        """Broadcast metrics update to all clients."""
        await self.broadcast({
            "type": "metrics_update",
            "data": metrics_data,
            "timestamp": asyncio.get_event_loop().time()
        })
    
    async def broadcast_recommendations_update(self, recommendations_data: Dict[str, Any]):
        """Broadcast recommendations update to all clients."""
        await self.broadcast({
            "type": "recommendations_update",
            "data": recommendations_data,
            "timestamp": asyncio.get_event_loop().time()
        })
    
    async def start_server(self):
        """Start the WebSocket server."""
        async with serve(self.handle_client, self.host, self.port):
            print(f"WebSocket server started on ws://{self.host}:{self.port}")
            await asyncio.Future()  # Run forever
    
    def start_server_sync(self):
        """Start the WebSocket server synchronously."""
        asyncio.run(self.start_server()) 