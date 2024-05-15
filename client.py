import asyncio
import websockets

async def chat():
    uri = "ws://localhost:8000/ws/chat"  # Asegúrate de que el puerto es correcto.
    async with websockets.connect(uri) as websocket:
        while True:
            # Enviar un mensaje
            message = input("Escribe un mensaje (o 'salir' para terminar): ")
            if message == "salir":
                print("Finalizando sesión de chat.")
                break
            await websocket.send(message)
            print(f"> {message}")
            
            # Recibir y mostrar la respuesta
            response = await websocket.recv()
            print(f"< {response}")

# Ejecutar la función de chat dentro de un bucle de eventos asincrónicos
asyncio.run(chat())