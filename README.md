# Screen Share App

This project allows you to select an area on your screen and stream it to a local server which saves the latest frame.

## Prerequisites

You need Python installed (3.7+ recommended).

## Installation

1.  **Navigate to the project directory**:
    ```bash
    cd /Users/jamesyang/Documents/projects/screensharer
    ```

2.  **Install dependencies**:
    It is recommended to use a virtual environment.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install websockets mss
    ```
    *Note: `tkinter` is usually included with Python. If you get an error about it, you may need to install `python-tk` (Linux) or ensure your Python install includes it.*

## Running the App

### 1. Start the Server
Open a terminal and run:
```bash
source venv/bin/activate
python server/server.py
```
You should see: `Server starting on localhost:8765...`

### 2. Start the Client
Open a **new** terminal window and run:
```bash
source venv/bin/activate
python client/main.py
```

### 3. Usage
1.  When the client starts, your screen will dim slightly.
2.  Click and drag to draw a red rectangle around the area you want to share.
3.  Release the mouse to confirm.
4.  The streaming will begin immediately.
5.  Check the `server/captured_images/latest.png` file to see the real-time updates.
6.  Press `Ctrl+C` in the terminal windows to stop.

## Project Structure
- `server/`: Contains the websocket server (`server.py`) and saved images.
- `client/`: Contains the client application (`main.py`, `overlay.py`, `streamer.py`).
