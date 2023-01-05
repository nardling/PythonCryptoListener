import asyncio
import websockets

class tradesServer:
    def __init__(self, port):
        self.running = False
        self.server = None
        self.port = port
        self.sockets = set()
        self.sendLoop = asyncio.new_event_loop()

    def sendSynch(self, msg):
        self.send(msg)

    def sendFunc(self, msg):
        for s in self.sockets:
            self.sendLoop.run_until_complete(s.send(msg))

    async def msgRecv(self, socket, path):
        while True:
            msg = await socket.recv()
            if msg == "subscribe":
                self.sockets.add(socket)
            print ("****************CLIENT SUBSCRIBED***************")

    def start(self):
        if (self.running):
            return
        self.running = True
        loop = asyncio.new_event_loop()
        loop.set_debug(True)
        asyncio.set_event_loop(loop)
        self.server = websockets.serve(self.msgRecv, "", self.port)
        # asyncio.get_event_loop().run_until_complete(self.server)
        # asyncio.get_event_loop().run_forever()
        loop.run_until_complete(self.server)
        loop.run_forever()
        loop.close()
        print("Server Exiting")
