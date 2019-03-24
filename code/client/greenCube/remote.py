import socket
import time
import json

def get_remote_msg(socket_in):
    """Returns msg from a remote player.

    Parameters
    ----------
    socket_in: socket to receive msg (socket)
        
    Returns
    ----------
    msg: just a message (str)

    Raises
    ------
    IOError: if remote player cannot be reached
            
    """

    msg = None
    # receive msg    
    try:
        msg = socket_in.recv(65536).decode()
    except:
        pass

    if msg == '':
        msg = None

    return msg


def send_msg(msg, socket_out):
    """Notifies msg of the local player to a remote player.
    
    Parameters
    ----------
    socket_out: socket to send msg (socket)
    msg: msg of the local player (str)
        
    Raises
    ------
    IOError: if remote player cannot be reached
    
    """

    if msg != '':
        # send msg
        try:
            socket_out.sendall(msg.encode())
        except:
            pass


def create_socket_in(ip, port_in):
    socket_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_in.bind((ip, port_in))
    socket_in.listen(1)

    return socket_in


def create_connection(socket_in):
    # remote_adress = (ip, port)
    connection, remote_address = socket_in.accept()
    peername = connection.getpeername()
    print('# New connection established with ip %s, and port %s' % (peername[0], peername[1]))
    return connection

def connect(ip, port, timeout=True, timeouttime=5):
    print("Trying to connect")
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if timeout:
        connection.settimeout(timeouttime)

    try:
        connection.connect((ip, port))
    except TimeoutError:
        print('Wasn\'t able to create the connection. Time out.')
        connection = None

    return connection

