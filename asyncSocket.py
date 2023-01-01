from tradesServer import tradesServer
import threading

s = tradesServer(5001)
serveinst = threading.Thread(target=s.start, daemon=True)
serveinst.start()

while True:
    pass