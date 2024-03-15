
import websocket

# WebSocket connection URL
socket_url = "ws://localhost:8000/ws/tableData/"

def on_message(ws, message):
    print("Received message:", message)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws):
    print("WebSocket connection closed.")

def on_open(ws):
    print("WebSocket connection established.")
    # Send "hi" message to the server
    ws.send("hi")

if __name__ == "__main__":
    # Create a WebSocket connection
    ws = websocket.WebSocketApp(socket_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

