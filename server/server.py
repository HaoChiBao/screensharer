import asyncio
import websockets
import os
import time
import http

SAVE_DIR = "captured_images"

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

connected_clients = set()

async def health_check(path, request_headers):
    if path == "/health":
        return http.HTTPStatus.OK, [], b"OK"

async def handler(websocket):
    client_type = "Unknown"
    try:
        # Wait for identification message
        init_msg = await websocket.recv()
        if isinstance(init_msg, str):
            if init_msg == "REGISTER_RECORDER":
                client_type = "Recorder"
            elif init_msg == "REGISTER_VIEWER":
                client_type = "Viewer"
            else:
                print(f"Unknown client type: {init_msg}")
        
        print(f"Client connected: {client_type}")
        connected_clients.add(websocket)
        
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
        print(f"Client disconnected: {client_type}")
    except Exception as e:
        print(f"Error ({client_type}): {e}")
    finally:
        if websocket in connected_clients:
            connected_clients.remove(websocket)

async def main():
    print("Server starting on localhost:8080...")
    async with websockets.serve(handler, "0.0.0.0", 8080, process_request=health_check):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped.")
