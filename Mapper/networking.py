import socket
import threading
import select
from Queue import Queue

import sys, traceback

from ui.map_ui import MapDS

RS = chr(30)

HOST = socket.gethostname()
PORT = 11173
ADDR = (HOST,PORT)

MAX_PACKET_LENGTH = 1024
MAX_PLAYERS = 6

class UserSlot(object):
    OPEN = object()  # uses less memory than an integer, actually.
    PLAYER = object()

    def __init__(self, *args):
        self.set_open()

    def parse_buffer(self):
        toR = []
        while RS in self.buffer:
            term, _, self.buffer = self.buffer.partition(RS)
            toR.append(term)
        return toR

    def set_open(self):
        self._status = UserSlot.OPEN
        self.conn = None
        self.buffer = ""

    def set_connection(self, connection, safe_mode=True):
        assert((not safe_mode) or self.is_open())
        self.conn = connection
        self._status = UserSlot.PLAYER

    def is_open(self):
        return self._status == UserSlot.OPEN

    def send(self, *msg):
        message = ' '.join(map(str, msg))
        self.conn.send(message + RS)


class Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(ADDR)
        self.done = False
        self.slots = [UserSlot() for _ in xrange(MAX_PLAYERS)]
        self.input_handlers = {"MSG": self.cmd_msg}

        print "Generating map...",
        self.map = MapDS()
        self.map.expand_room()
        print " done."

    def cmd_restart(self):
        self.broadcast("RESTART")

    def run(self):
        self.sock.listen(MAX_PLAYERS)
        while not self.done:
            inputs = [x.conn for x in self.slots if not x.is_open()] + [self.sock]
            # blocks until someone connects or a client sends a message
            ready, _, _ = select.select(inputs, [], [], 0.5)  # filters ready connections
            for c in ready:
                if c == self.sock:    # new player
                    conn, _ = c.accept()
                    ind = self.get_next_slot()
                    if ind is None:  # out of slots, have to reject
                        print "Rejected a connection"
                        continue
                    self.slots[ind].set_connection(conn)
                    print "Connected"
                else:   # returning player's command
                    sender = self.get_sender(c)
                    message = c.recv(MAX_PACKET_LENGTH)  # am I stupid or is this just as good
                    if not message:  # close connection
                        c.close()
                        self.slots[sender].set_open()
                    else:   # a real command
                        sender = self.get_sender(c)
                        self.slots[sender].buffer += message
                        messages = self.slots[sender].parse_buffer()
                        for msg in messages:
                            self.handle_input(sender, msg)

    def handle_input(self, slot, message):
        msg = message.split(" ")
        if msg[0] not in self.input_handlers:
            print "Unknown or malformed command:", msg[0]
            return
        self.input_handlers[msg[0]](slot, msg)

    def cmd_msg(self, slot, argv):
        if argv[1][:1] == "/":
            command = argv[1][1:]
        self.broadcast(*argv[1:])

    def broadcast(self, *msg):
        for x in self.slots:
            if not x.is_open():
                x.send(*msg)

    def process_received(self, msg):
        pass

    def stop(self):
        self.done = True

    def get_sender(self, c):
        for i, x in enumerate(self.slots):
            if not x.is_open():
                if x.conn == c:
                    return i
        print "Server.get_sender: I couldn't find the guy you're looking for, this is really bad."

    def get_next_slot(self):
        for i, x in enumerate(self.slots):
            if x.is_open():
                return i
        return None


class Client(threading.Thread):
    def __init__(self, main, host=None):
        self.main = main
        if host is None:
            host = HOST
        self.ADDR = (host, PORT)
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.msgs = Queue()
        self.done = False
        self.recv_buf = ''

    def run(self):
        try:
            self.sock.connect(self.ADDR)
        except IOError:
            print "Couldn't connect"
            return
        self.sock.settimeout(0.5)
        self.send("MSG Hi there!")
        while not self.done:
            while (not self.done) and (RS not in self.recv_buf):
                try:
                    message = self.sock.recv(MAX_PACKET_LENGTH)
                except socket.timeout:
                    continue
                if not message:
                    # an empty string indicates that the client has
                    # closed their connection
                    #print "closed connection"
                    self.done = True
                    self.sock.close()
                    break
                else:
                    self.recv_buf += message
            if not self.done:
                term, _, self.recv_buf = self.recv_buf.partition(RS) 
                self.process_received(term)

    def stop(self):
        self.done = True

    def send(self, msg):
        buf = msg + RS
        while buf:
            self.sock.send(buf[:MAX_PACKET_LENGTH])
            buf = buf[MAX_PACKET_LENGTH:]

    def process_received(self, message):
        print "recv:", message

if __name__ == "__main__":
    while 1:
        try:
            exec(raw_input(">"))
        except Exception as e:
            traceback.print_exc(file=sys.stdout)