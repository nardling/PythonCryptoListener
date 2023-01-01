import asyncio
import websockets

async def handler(websocket, path):
    data = await websocket.recv()
    reply = f"Data recv'd {data}"
    await websocket.send(reply)

start_server = websockets.serve(handler, "", 5001)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
