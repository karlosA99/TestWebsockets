from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: list[WebSocket] = []
        
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
            
manager = ConnectionManager()

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            # Aquí, deberías procesar el mensaje recibido y generar una respuesta.
            response = f"Mensaje procesado: {data}"
            await manager.send_message(response, websocket)
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        #await manager.broadcast("CLIENT DISCONNECTED")
        print("Client Disconnected. Closing session...")
    
    except Exception as e:
        print(f"Unexpected error: {e}")