from getsensor import getSensor
import json
import remote as re
import time
import _thread

file = open('config.txt', 'r')
config = json.load(file)
file.close()

def wait_msg(connection):
	while connection is not None:
		msg = re.get_remote_msg(connection)
		if msg is not None:
			print(msg)

server_ip = "192.168.10.104"
server_port = 42001

connection = re.connect(server_ip, server_port)


connection.setblocking(0)

_thread.start_new_thread(wait_msg, (connection, ))

while 1:
	data = {}
	data[1] = getSensor()
	#data = json.loads(msg)
	#data['cube_id'] = config['cube_id']
	msg = json.dumps(data)
	#msg = getSensor() + str(config['cube_id'])
	print(msg)
	re.send_msg(msg, connection)
	time.sleep(1)
