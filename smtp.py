from socket import *
import base64


# decodeeverythingreceivedfrom server
# encodeeverythingsendtoserver


def client_socket(sock, msg, mailFrom, rcpt):
    sock.send(mailFrom.encode())
    received_from = sock.recv(1024).decode("utf-8")
    print(received_from)

    sock.send(rcpt.encode())
    received_rcpt = sock.recv(1024).decode("utf-8")
    print(received_rcpt)

    data = "DATA\r\n"
    sock.send(data.encode())
    received_data = sock.recv(1024).decode("utf-8")
    print(received_data)
    print("data--")

    sock.send(msg.encode())
    received_msg = sock.recv(1024).decode("utf-8")
    print(received_msg)
    print("msg--")

    # end = "<CR><LF>.<CR><LF>\r\n"
    # sock.send(end.encode())
    # received_end = sock.recv(1024).decode("utf-8")
    # print(received_end)
    # print("crlf--")

    # dot = ".\r\n"
    # sock.send(dot.encode())
    # received_dot = sock.recv(1024).decode("utf-8")
    # print(received_dot)
    # print("dot--")

    quit = "QUIT\r\n"
    sock.send(quit.encode())
    received_quit = sock.recv(1024).decode("utf-8")
    print(received_quit)

    sock.close()
    print("mail sent via socket. closed client")


def login(sock, username, password, mail_server):
    sock.connect(mail_server)
    recv_mail_server = (sock.recv(1024)).decode("utf-8")
    print("received mail server:", recv_mail_server)

    ehlo = "HELO lb\r\n"
    sock.send(ehlo.encode())
    received_ehlo = sock.recv(1024).decode("utf-8")
    print("HELO/EHLO return:", received_ehlo)
    if received_ehlo.startswith('250'):
        print('250 reply not received from server.')

    authPlain = "AUTH PLAIN "
    cred = base64.b64encode(("\x00"+username + "\x00"+password).encode())
    authMsg = authPlain.encode() + cred + "\r\n".encode()
    sock.send(authMsg)
    received_auth = sock.recv(1024).decode("utf-8")
    print("send login details to server: ", received_auth)


if __name__ == '__main__':
    print("started")
    username = "rnetin"
    password = "Ueben8fuer8RN"
    msg = "Subject: helloo future\r\n.\r\n"
    mailFrom = "MAIL FROM:<rnetin@htwg-konstanz.de>\r\n"
    rcpt = "RCPT TO:<gi161kok@htwg-konstanz.de>\r\n"
    mail_server = ("asmtp.htwg-konstanz.de", 587)
    clientSocket = socket(AF_INET, SOCK_STREAM)
    print("2")
    login(clientSocket, username, password, mail_server)
    client_socket(clientSocket, msg, mailFrom, rcpt)

    # Press the green button in the gutter to run the script.

