from getsensor import getSensor
from websocket import create_connection
import time

connected = False
while not connected:
	try:
		ws = create_connection("ws://192.168.10.104:1000")
		connected = True
	except ConnectionRefusedError:
		print("Connection failed, retrying,...")
		time.sleep(1)

while 1:
	msg = getSensor()
	print(msg)
	ws.send(msg)
	time.sleep(1)
