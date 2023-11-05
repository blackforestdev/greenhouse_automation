import websocket
import json
import time

# Define the WebSocket URL
ws_url = "ws://localhost:5000/socket.io/?EIO=4&transport=websocket"

# Define a function to handle incoming messages
def on_message(ws, message):
    print(f"Received: {message}")
    # Check if the message is a response to your custom event
    if "current_times" in message:
        print("Received current times data")

# Define a function to handle errors
def on_error(ws, error):
    print(f"Error: {error}")

# Define a function to handle WebSocket close
def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

# Define a function to handle WebSocket open
def on_open(ws):
    print("Websocket connected")
    # Send a custom event
    event_data = json.dumps({"event": "request_current_times"})
    ws.send(event_data)

# Create a WebSocketApp object and define the callbacks
ws = websocket.WebSocketApp(ws_url,
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

# Start the WebSocket connection and run forever
ws.run_forever()
