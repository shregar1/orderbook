import json
import asyncio
import websockets

async def hello():
    async with websockets.connect('ws://127.0.0.1:8000/connect') as websocket:
        try:
            while True:
                await asyncio.sleep(1)  # Send a ping every 10 seconds
                await websocket.ping("connection")
                message = await websocket.recv()
                event_payload: dict = json.loads(message)
                event = event_payload.get("event")
                data = event_payload.get("data")
                print(f"Received {event} event data: {data}")
                print("Ping sent")
        except websockets.exceptions.ConnectionClosedError:
            pass
asyncio.run(hello())
