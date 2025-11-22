import asyncio
import websockets
import os
import time

SAVE_DIR = "captured_images"

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

connected_clients = set()

async def handler(websocket):
    print("Client connected")
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            # Broadcast to other clients
            # We iterate over a copy to avoid modification during iteration issues.
            for client in list(connected_clients):
                if client != websocket:
                    try:
                        await client.send(message)
                    except websockets.exceptions.ConnectionClosed:
                        pass
                    except Exception as e:
                        print(f"Broadcast error: {e}")
                        
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connected_clients.remove(websocket)

async def main():
    print("Server starting on localhost:8765...")
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped.")
