import asyncio
import threading
from overlay import SelectionOverlay
from streamer import ScreenStreamer

def start_streaming(selection):
    streamer = ScreenStreamer(selection)
    try:
        asyncio.run(streamer.stream())
    except KeyboardInterrupt:
        streamer.stop()

def main():
    # 1. Show overlay to get selection
    selection = None
    
    def on_selected(rect):
        nonlocal selection
        selection = rect
    
    overlay = SelectionOverlay(on_selected)
    overlay.start()
    
    if selection:
        print(f"Starting stream for region: {selection}")
        start_streaming(selection)
    else:
        print("No selection made. Exiting.")

if __name__ == "__main__":
    main()
