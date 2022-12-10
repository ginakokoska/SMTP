from socket import *
import base64


# decodeeverythingreceivedfrom server
# encodeeverythingsendtoserver


def ascii_to_base64(ascii_string):  # encode
    #return ascii_string.decode()
    return (base64.b64encode(ascii_string.encode('utf-8'))).decode('utf-8')


def base64_to_ascii(base64_string):  # decode
    #return
    return (base64.b64decode(base64_string)).decode('utf-8')


def check_message(msg):
    if msg.endswith("\r\n"):
        return msg
    else:
        return msg + "\r\n"


def client_socket(sock, msg, mailFrom, rcpt):
    sock.send(mailFrom.encode())
    received_from = ascii_to_base64(sock.recv(1024))
    print(received_from)

    sock.send(rcpt.encode())
    received_rcpt = ascii_to_base64(sock.recv(1024))
    print(received_rcpt)

    data = "DATA\r\n"
    sock.send(data.encode())
    received_data = ascii_to_base64(sock.recv(1024))
    print(received_data)

    msg = check_message(msg)
    sock.send(msg.encode())
    received_msg = ascii_to_base64(sock.recv(1024))
    print(received_msg)

    dot = "."
    sock.send(dot.encode())
    received_dot = ascii_to_base64(sock.recv(1024))
    print(received_dot)

    quit = "QUIT\r\n"
    sock.send(quit.encode())
    received_quit = ascii_to_base64(sock.recv(1024))
    print(received_quit)

    sock.close()
    print("mail sent via socket. closed client")


def login(sock, username, password, mail_server):
    sock.connect(mail_server)
    recv_mail_server = base64_to_ascii(sock.recv(1024))


    username = ascii_to_base64(username)  # ascii_to_base64("\x00{username}")
    password = ascii_to_base64(password)  # ascii_to_base64("\x00{password}")
    authPlain = ascii_to_base64("AUTH PLAIN ")
    authMsg = authPlain + username + password
    sock.send(authMsg)
    received_auth = base64_to_ascii(sock.recv(1024))
    print("send login details to server: " + authMsg)



if __name__ == '__main__':
    username = "yannickrechnernetze@gmx.de"
    password = "GinaYannick"
    msg = "helloo future"
    mailFrom = "<MAIL FROM:<yannickrechnernetze@gmx.de>"
    rcpt = "<RCPT TO:<gi161kok@htwg-konstanz.de>"
    authPlain = "AUTH PLAIN "
    mail_server = ("smtp.gmx.com", 25)
    clientSocket = socket(AF_INET, SOCK_STREAM)

    login(clientSocket, username, password, mail_server)
    client_socket(clientSocket, msg, mailFrom, rcpt)


    # Press the green button in the gutter to run the script.


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
