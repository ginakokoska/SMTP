import socket
import struct
import math
from _thread import *
import threading
print_lock = threading.Lock()


def threaded(c):
    while True:
        try:
            unpacker_n = struct.Struct('B')
            n_data = c.recv(unpacker_n.size)
            print("received n:", n_data)
            n = unpacker_n.unpack(n_data)[0]
            print("unpacked n:", n)
            unpacker_str = 'I 7s B'
            for i in range(n):
                unpacker_str += ' i'
            unpacker = struct.Struct(unpacker_str)

            data = c.recv(unpacker.size)
            if not n_data+data:
                print_lock.release()
                break
            print("received:", data)
            unpacked_data = unpacker.unpack(data)
            print("unpacked:", unpacked_data)
            numbers = unpacked_data[-n:]
            print("numbers:", numbers)
            args = unpacked_data[0:len(unpacked_data) - n]
            msg_id = args[0]
            operation = args[1]
            print("operation:", operation)
            result = calculate(operation, numbers)
            print("msg_id:", msg_id)
            print("result:", result)
            response = struct.pack('I i', msg_id, result)
            c.send(response)

        except TimeoutError:
            c.close()
    c.close()


def calculate(op, z):

    match op:
        case b"summe__":
            return summe(z)
        case b"produkt":
            return produkt(z)
        case b"minimum":
            return minimum(z)
        case b"maximum":
            return maximum(z)
        case _:
            return failed()


def summe(z):
    return sum(z)


def produkt(z):
    return math.prod(z)


def minimum(z):
    return min(z)


def maximum(z):
    return max(z)


def failed():
    pass

# alternative: N an den Anfang von den Daten packen, nur 4 bytes lesen, dann n rausholen, dann Rest


if __name__ == '__main__':
    listening_addr = ("127.0.0.1", 6969)
    server_addr = ("127.0.0.1", 6969)
    streamSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    streamSocket.bind(server_addr)
    streamSocket.listen(1)
    streamSocket.settimeout(15)

    while True:
        connection, addr = streamSocket.accept()
        print_lock.acquire()
        print("Connected to:", addr[0], f':{addr[1]}')
        start_new_thread(threaded, (connection,))
