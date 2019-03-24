#import sys, os
#path_server = os.path.realpath(__file__)
#sys.path.append(os.path.dirname(path_server)+'/..')
import mysql.connector as sqlcon
# import generic for all
import socket
import json
import time
import remote as re
import _thread
# import for websockets
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

def is_beginning_in_list(_list, testing):
    for begining in _list:
        if len(testing) >= len(begining) and begining == testing[0:len(begining)]:
            return begining
    return None

def cmdParser(msg, prefixCmd):
    resp = is_beginning_in_list(prefixCmd, msg)
    if resp is not None:
        list_cmd = msg[1:].split(' ')

        cmd = list_cmd[0]
        # if there is no element after the 1 element in list_cmd then parameters = ['']
        parameters = list_cmd[1:]

        return cmd, parameters

class Server:
    def __init__(self):
        self.running = True
        self.prefixCmd=[]

    def on_msg(self):
        pass


class Local(Server):
    def __init__(self, port=42001, default_port_server=42002):
        super().__init__()
        self.client_server = None

        self.prefixCmd = ['/']

        self.port = port
        self.default_port_server = default_port_server
        self.ip = '127.0.0.1'
        self.socket = re.create_socket_in(self.ip, self.port)

        self.client_local = self.on_new_connection(re.create_connection(self.socket))
        self.loop_main()


    def on_new_connection(self, connection):
        connection.setblocking(0)
        new_client = SocketClient(connection=connection, server=self)
        _thread.start_new_thread(new_client.wait_msg, ())
        return new_client


    def loop_main(self):
        while self.running:
            pass


    def on_msg(self, msg, client_):

        if msg[0] in self.prefixCmd:
            if client_ == self.client_local:
                print(msg)
            # local command
            self.onCmd(msg, client_)

        elif self.client_server is not None and client != self.client_server:
            # send the input to server
            self.send_msg(msg, self.client_server)

        else:
            print(msg)

    def onCmd(self, msg, sender):
        cmd, parameters = cmdParser(msg, self.prefixCmd)

        if cmd == 'co':
            self.disconnect('/disc')
            # create the connection
            server_ip = parameters[0]

            if len(parameters) == 2:
                port_server = int(parameters[1])
            else:
                port_server = self.default_port_server

            print('trying to connect to %s on port nb %d' % (server_ip, port_server))

            connection = re.connect(server_ip, port_server)
            if connection is not None:
                self.client_server = self.on_new_connection(connection)

        elif cmd == 'disc':
            self.disconnect(msg)

        elif cmd == 'test':
            print('-> reponse of the test')

    def send_msg(self, msg, client):
        if client.connection is not None:
            re.send_msg(msg, client.connection)


    def disconnect(self, msg):
        if self.client_server is not None and self.client_server.connection is not None:
            try:
                self.send_msg(msg, self.client_server)
                # shutdown the socket out server
                self.client_server.connection.shutdown(socket.SHUT_RDWR)
                self.client_server.connection.close()

                self.client_server.connection = None
                self.client_server = None
            except:
                print('! cannot disconnect correctly !')


class MultiClient(Server):
    def __init__(self, ip=None, port=42003, port_ws=18000):
        super().__init__()
        print('init multiclient')
        self.port = port
        self.port_ws = port_ws
        self.clients = []
        self.last_client_id = 0
        self.wait_connection = True

        self.ip = ip

        if self.ip is None:
            self.ip = socket.gethostbyname(socket.gethostname())

    def start(self):
        _thread.start_new_thread(self.loopSocketServer, (self.ip, self.port, ))
        # "bug" can't change the ip or it stop working
        #_thread.start_new_thread(self.loopWebsocketServer, ('', self.port_ws, ))

        self.loop_main()


    def loop_main(self):
        while True:
        #    pass
            time.sleep(5)
    def loopSocketServer(self, ip='', port= 42003):
        classic_sock_server = SocketServer(ip, port, self)
        print("Server Socket ip is %s, and port is %s" % (ip, port))
        while self.running:
            if self.wait_connection:
                classic_sock_server.waitOneConnection()


    def loopWebsocketServer(self, ip='', port=8000):
        web_socket_server = SimpleWebSocketServer(ip, port, WebsocketServer, game_server=self)
        print("Server WebSocket ip is %s, and port is %s" % (ip, port))
        while self.running:
            web_socket_server.serveonce()

    def on_new_client(self, new_client):
        new_client.id = self.last_client_id
        self.last_client_id += 1

        if new_client.server is None:
            new_client.server = self
        self.clients.append(new_client)

        self.send_msg('** You\'re connected on a server which ip is %s, and port is %s **' % (self.ip, self.port), new_client, verbose=True)

        return new_client

    def on_msg(self, msg, sender):
        if msg is not None and len(msg)>0:
            if msg[0] in self.prefixCmd:
                self.onCmd(msg, sender)
            else:
                msg = '>>' + msg
                print(msg)
                # give a response to the any client connected
                self.send_msg(msg, self.clients)

    def onCmd(self, msg, sender):
        cmd, parameters = cmdParser(msg, self.prefixCmd)

    def send_msg(self, msg, dests, blacklist='', verbose=False, onePrint=True):
        if isinstance(dests, Client):
            # Transform the Client object into an iterable
            dests = [dests]

        firstPrint=True
        for dest in dests:
            if blacklist == '' or dest not in blacklist:
                if verbose and ((onePrint and firstPrint) or not onePrint):
                    print('System->%s:%s' % (dest.name, msg))
                    firstPrint=False
                dest.send(msg)


    def shutdown_client(self, client):
        self.clients.remove(client)
        client.shutdown()


class WebsocketServer(WebSocket):
    """ 
    Object from this class will create connection throught the web.
    And then create a WebsocketClient object, and bind it to his chat server. 
    """
    def __init__(self, server, sock, adress, game_server=None):
        super().__init__(server, sock, adress)
        self.game_server = game_server
        self.game_client = None

    def handleMessage(self):
        if self.game_client is not None:
            self.game_client.receive(self.data)

    def handleConnected(self):
        new_client = WebsocketClient(self)
        self.game_client = self.game_server.on_new_client(new_client)

    def send(self, msg):
        self.sendMessage(msg)


class SocketServer:
    def __init__(self, ip, port, game_server):
        self.ip = ip
        self.port = port
        self.running = True
        self.game_server = game_server
        self.socket_in = self.createSocketIn(ip, port)

    def createSocketIn(self, ip, port):
        socket_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_in.bind((ip, port))
        socket_in.listen(1)
        return socket_in


    def waitOneConnection(self):
        connection, remote_adress = self.socket_in.accept()
        peername = connection.getpeername()
        print('# New classic socket connection established with ip %s, and port %s' % (peername[0], peername[1]))
        self.onConnection(connection)


    def onConnection(self, connection):
        connection.setblocking(0)
        client = SocketClient(connection=connection, server=self.game_server)
        client = self.game_server.on_new_client(client)
        _thread.start_new_thread(client.wait_msg, ())


class Client:
    def __init__(self, name='Unnamed', server=None):
        self.running = True
        self.name = name
        self.server = server

    def shutdown(self):
        del self

    def receive(self, msg):
        self.server.on_msg(msg, self)


class SocketClient(Client):
    def __init__(self, connection=None, name='Unnamed', server=None):
        super().__init__(name, server)
        self.db = sqlcon.connect(host="127.0.0.1", user="greencube_user", passwd="123")
        self.connection = connection

    def wait_msg(self):
        while self.server is not None and self.server.running and self.running:
            msg = None

            if self.connection is not None:
                msg = re.get_remote_msg(self.connection)

            if msg is not None:
                #db = sqlcon.connect(host="127.0.0.1", user="greencube_user", passwd="123")
                print(msg)
                cur = self.db.cursor()
                cur.execute("USE greencube")
                add_entries = ("INSERT INTO Measurement "
                              "(type, value, id_sensor, `date`) "
                              "VALUES (%s, %s, %d, NOW())")
                data = json.loads(msg)
                for id_sensor in data:
                    for type in data[id_sensor]:
                        #print("INSERT INTO M%(type, str(data[id_sensor][type]), int(id_sensor))
                        data_measure = (type, str(data[id_sensor][type]), int(id_sensor))
                        #print(data_measure)
                        print("INSERT INTO Measurement (type, value, id_sensor, `date`) VALUES (\"" + type + "\", \"" + str(data[id_sensor][type]) + "\", " + id_sensor+ ", NOW())")
                        cur.execute("INSERT INTO Measurement (type, value, id_sensor, `date`) VALUES (\"" + type + "\", \"" + str(data[id_sensor][type]) + "\", " + id_sensor+ ", NOW())")
                self.db.commit()
                cur.close()
                #self.receive(msg)
                #print(db)
                #db = sqlcon.connect(host="127.0.0.1", user="greencube_user", passwd="123")
                print(msg)

    def send(self, msg):
        if self.connection is not None:
            re.send_msg(msg, self.connection)


class WebsocketClient(Client):
    def __init__(self, websocket,  name='Unnamed', server=None):
        super().__init__(name, server)
        self.websocket = websocket

    def send(self, msg):
        self.websocket.send(msg)

if __name__ == '__main__':
    MultiClient(ip='192.168.10.104', port=42001).start()
