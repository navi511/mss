import socket
from msslogger import MSSLogger

MSSLogger.intializelogger()
logger = MSSLogger.getlogger("clientlogger")
cs = socket.socket()
host = "127.0.0.1"
port = 9999

cs.connect((host, port))


def f_input():
    choice_msg = cs.recv(1024)
    logger.info("********* Services Provided by Server: *********\n " + choice_msg.decode())
    print("********* Services Provided by Server: *********\n ", choice_msg.decode('utf-8'))
    # User will provide the input as he wants to use the service
    choice_in = input("Please choose the Service option: ")
    logger.info("Please choose the Service option: " + choice_in)
    cs.send(choice_in.encode('utf-8'))

    choice_rec = cs.recv(1024)  # According to selected choice, look for the service
    logger.info(choice_rec.decode('utf-8'))

    if choice_rec.decode('utf-8') == '1':
        echo_rcv = cs.recv(1024).decode('utf-8')
        print(echo_rcv)
        logger.info(echo_rcv)
        client_echo()

    elif choice_rec.decode('utf-8') == '2':
        file_transfer()
    else:
        invalid_service()


def invalid_service():
    print("Oops !!! you have selected wrong service option\nDisconnecting from server \a...")
    logger.error("Oops !!! you have selected wrong service option\nDisconnecting from server \a...")


def client_echo():
    while True:
        msg = input("Type your Message: ")
        logger.info("Enter the string: " + msg)
        # send msg to server
        cs.sendall(msg.encode('utf-8'))

        # echo reply from server
        data = cs.recv(1024)
        print("Response from Server: ", data.decode('utf-8'))
        logger.info("Received echo message from server: " + data.decode('utf-8'))
        if data.decode('utf-8') == "Disconnecting from server ...\a":
            break
    cs.close()


def file_transfer():
    print("Currently the code is under development ")
    pass  # here FTS code will come


def main():
    f_input()


if __name__ == "__main__":
    main()
