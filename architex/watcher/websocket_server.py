"""
WebSocket server for real-time communication with frontend.
"""

import asyncio
import json
from typing import Dict, List, Optional, Any, Set
from websockets.server import serve, WebSocketServerProtocol
from websockets.exceptions import ConnectionClosed

from .live_analyzer import LiveAnalyzer


class WebSocketServer:
    """WebSocket server for real-time analysis updates."""
    
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.clients: Set[WebSocketServerProtocol] = set()
        self.live_analyzer = LiveAnalyzer()
        
        # Register callback for analysis updates
        self.live_analyzer.add_callback(self._broadcast_update)
    
    async def start(self):
        """Start the WebSocket server."""
        print(f"🌐 Starting WebSocket server on {self.host}:{self.port}")
        
        async with serve(self._handle_client, self.host, self.port):
            await asyncio.Future()  # Run forever
    
    async def _handle_client(self, websocket: WebSocketServerProtocol, path: str):
        """Handle WebSocket client connections."""
        print(f"🔌 New client connected: {websocket.remote_address}")
        self.clients.add(websocket)
        
        try:
            async for message in websocket:
                await self._handle_message(websocket, message)
        except ConnectionClosed:
            print(f"🔌 Client disconnected: {websocket.remote_address}")
        finally:
            self.clients.discard(websocket)
    
    async def _handle_message(self, websocket: WebSocketServerProtocol, message: str):
        """Handle incoming WebSocket messages."""
        try:
            data = json.loads(message)
            command = data.get('command')
            
            if command == 'analyze':
                await self._handle_analyze_command(websocket, data)
            elif command == 'get_summary':
                await self._handle_summary_command(websocket)
            elif command == 'get_element':
                await self._handle_element_command(websocket, data)
            elif command == 'get_boundary':
                await self._handle_boundary_command(websocket, data)
            elif command == 'export_diagram':
                await self._handle_export_command(websocket, data)
            else:
                await self._send_error(websocket, f"Unknown command: {command}")
                
        except json.JSONDecodeError:
            await self._send_error(websocket, "Invalid JSON")
        except Exception as e:
            await self._send_error(websocket, f"Error: {str(e)}")
    
    async def _handle_analyze_command(self, websocket: WebSocketServerProtocol, data: Dict[str, Any]):
        """Handle analyze command."""
        codebase_path = data.get('codebase_path')
        if not codebase_path:
            await self._send_error(websocket, "Missing codebase_path")
            return
        
        try:
            # Send analysis started notification
            await self._send_message(websocket, {
                'type': 'analysis_started',
                'codebase_path': codebase_path
            })
            
            # Perform analysis
            result = await self.live_analyzer.analyze_codebase(codebase_path)
            
            # Send analysis complete notification
            await self._send_message(websocket, {
                'type': 'analysis_complete',
                'result': result
            })
            
        except Exception as e:
            await self._send_error(websocket, f"Analysis failed: {str(e)}")
    
    async def _handle_summary_command(self, websocket: WebSocketServerProtocol):
        """Handle get_summary command."""
        summary = self.live_analyzer.get_analysis_summary()
        await self._send_message(websocket, {
            'type': 'summary',
            'data': summary
        })
    
    async def _handle_element_command(self, websocket: WebSocketServerProtocol, data: Dict[str, Any]):
        """Handle get_element command."""
        element_id = data.get('element_id')
        if not element_id:
            await self._send_error(websocket, "Missing element_id")
            return
        
        details = self.live_analyzer.get_element_details(element_id)
        if details:
            await self._send_message(websocket, {
                'type': 'element_details',
                'data': details
            })
        else:
            await self._send_error(websocket, f"Element not found: {element_id}")
    
    async def _handle_boundary_command(self, websocket: WebSocketServerProtocol, data: Dict[str, Any]):
        """Handle get_boundary command."""
        boundary_name = data.get('boundary_name')
        if not boundary_name:
            await self._send_error(websocket, "Missing boundary_name")
            return
        
        details = self.live_analyzer.get_service_boundary_details(boundary_name)
        if details:
            await self._send_message(websocket, {
                'type': 'boundary_details',
                'data': details
            })
        else:
            await self._send_error(websocket, f"Boundary not found: {boundary_name}")
    
    async def _handle_export_command(self, websocket: WebSocketServerProtocol, data: Dict[str, Any]):
        """Handle export_diagram command."""
        format_name = data.get('format')
        if not format_name:
            await self._send_error(websocket, "Missing format")
            return
        
        try:
            diagram = self.live_analyzer.export_diagram(format_name)
            await self._send_message(websocket, {
                'type': 'diagram_export',
                'format': format_name,
                'diagram': diagram
            })
        except Exception as e:
            await self._send_error(websocket, f"Export failed: {str(e)}")
    
    async def _broadcast_update(self, update_data: Dict[str, Any]):
        """Broadcast analysis updates to all connected clients."""
        message = {
            'type': 'analysis_update',
            'data': update_data
        }
        
        # Send to all connected clients
        disconnected_clients = set()
        for client in self.clients:
            try:
                await self._send_message(client, message)
            except ConnectionClosed:
                disconnected_clients.add(client)
            except Exception as e:
                print(f"Error sending to client: {e}")
                disconnected_clients.add(client)
        
        # Remove disconnected clients
        self.clients -= disconnected_clients
    
    async def _send_message(self, websocket: WebSocketServerProtocol, data: Dict[str, Any]):
        """Send a message to a WebSocket client."""
        try:
            await websocket.send(json.dumps(data))
        except ConnectionClosed:
            raise
    
    async def _send_error(self, websocket: WebSocketServerProtocol, error: str):
        """Send an error message to a WebSocket client."""
        await self._send_message(websocket, {
            'type': 'error',
            'message': error
        })
    
    def get_client_count(self) -> int:
        """Get the number of connected clients."""
        return len(self.clients)
    
    async def broadcast_message(self, message_type: str, data: Any):
        """Broadcast a custom message to all clients."""
        message = {
            'type': message_type,
            'data': data
        }
        
        disconnected_clients = set()
        for client in self.clients:
            try:
                await self._send_message(client, message)
            except ConnectionClosed:
                disconnected_clients.add(client)
            except Exception as e:
                print(f"Error broadcasting to client: {e}")
                disconnected_clients.add(client)
        
        # Remove disconnected clients
        self.clients -= disconnected_clients 