import asyncio
import websockets
import mss
import mss.tools
import io
import time

class ScreenStreamer:
    def __init__(self, region):
        self.region = region
        self.running = False

    async def stream(self):
        uri = "ws://localhost:8765"
        self.running = True
        
        print(f"Connecting to {uri}...")
        try:
            async with websockets.connect(uri) as websocket:
                print("Connected to server.")
                with mss.mss() as sct:
                    while self.running:
                        # Capture the screen
                        img = sct.grab(self.region)
                        
                        # Convert to PNG
                        # mss.tools.to_png(img.rgb, img.size, output="debug.png") # Debug
                        
                        # We need to convert raw pixels to PNG bytes efficiently
                        # Using mss built-in to_png is easiest but writes to file usually.
                        # Let's use PIL for in-memory conversion if needed, but mss has a way.
                        # Actually, sct.grab returns a ScreenShot object.
                        # We can get bytes directly.
                        
                        # Efficient conversion to PNG bytes
                        png_bytes = mss.tools.to_png(img.rgb, img.size)
                        
                        await websocket.send(png_bytes)
                        
                        # Cap at ~30 FPS
                        await asyncio.sleep(0.033)
                        
        except Exception as e:
            print(f"Streaming error: {e}")
        finally:
            print("Streaming stopped.")

    def stop(self):
        self.running = False
