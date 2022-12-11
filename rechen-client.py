import socket
import struct


def formatForClient(msg_id, operation, z):

    n = len(z)
    operation = operation.encode('utf-8')
    values = (msg_id, operation, n)
    n_value = (n,)
    print("n_value", n_value)
    for num in z:
        values += (num,)
    print("values", values)
    packer_str = 'I 7s B'
    for i in range(n):
        packer_str += ' i'
    print("packer_str", packer_str)
    packer = struct.Struct(packer_str)
    print("packer", packer)
    packer_n = struct.Struct('B')
    print("packer_n", packer_n)
    return [packer_n.pack(*n_value), packer.pack(*values)]


def interpret_response(data):
    unpacker_str = 'I i'
    unpacker = struct.Struct(unpacker_str)
    return unpacker.unpack(data)


if __name__ == '__main__':

    calc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    calc_socket.settimeout(15)
    server_address = ('127.0.0.1', 6969)
    calc_socket.connect(server_address)
    i = 0

    while True:
        try:
            query = formatForClient(i, "summe__", [1, 2, 3])
            i += 1
            print(query)
            calc_socket.sendall(query[0])
            calc_socket.sendall(query[1])
            data = calc_socket.recv(8)
            print("received", data)
            unpacked_data = interpret_response(data)

            print("unpacked:", unpacked_data)
            hostname = socket.gethostname()
            IPAddr, port = calc_socket.getpeername()
            print("Your computer name is:", hostname)
            print("Your ip address is:", IPAddr)
            print("Your socket port is:", port)
            ans = input('\nDo you want to continue? (y/n):')
            if ans == 'y':
                continue
            else:
                break
        except TimeoutError:
            calc_socket.close()
    calc_socket.close()
