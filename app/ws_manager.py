from fastapi import WebSocket
import json

class WSManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room: str):
        await websocket.accept()
        if room not in self.active_connections:
            self.active_connections[room] = []
        self.active_connections[room].append(websocket)

    def disconnect(self, websocket: WebSocket, room: str):
        if room in self.active_connections and websocket in self.active_connections[room]:
            self.active_connections[room].remove(websocket)
            if not self.active_connections[room]:
                del self.active_connections[room]

    async def broadcast(self, data: dict, room: str):
        if room in self.active_connections:
            message_json = json.dumps(data, default=str)
            for connection in self.active_connections[room]:
                await connection.send_text(message_json)

manager = WSManager()