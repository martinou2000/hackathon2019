import getsensor as sensor
import remote as re
import _thread
import time

def on_new_connection(self, connection):
	connection.setblocking(0)
	new_client = SocketClient(connection=connection, server=self)
	_thread.start_new_thread(new_client.wait_msg, ())
	return new_client

def loop_send(msg, connection):

	while 1:
		msg = "# Info to send to server"
		if connection is not None:
			msg = input()
			re.send_msg(msg, connection)
		time.sleep(1)


# create connection out
server_ip = '192.168.10.104'
port_server = 42000
connected = False
while not connected:
	try:
		connection_out = re.connect(server_ip, port_server)
		connected = True
	except ConnectionRefusedError:
		#print("can't connect bro")
		time.sleep(1)
_thread.start_new_thread(loop_send, ("rasp_send", connection_out))

#if connection is not None:
#client = on_new_connection(connection)
""" 
while 1:
	msg = "# Info to send to server"
	if connection is not None:
		re.send_msg(msg, connection)
"""

# create connection in
"""port = 42005
ip = '192.168.10.105'
socket = re.create_socket_in(ip, port)

connection = re.create_connection(socket)
connection.setblocking(0)


while 1:
	msg = re.get_remote_msg(connection)
	print(msg)
	input()
	time.sleep(1)
"""
while connection_out is not None:
	msg = sensor.getSensor()
	print("send"+msg)
	re.send_msg(msg, connection_out)
	time.sleep(1)
