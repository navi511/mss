import socket

from msslogger import MSSLogger

host = ""  # Address of the socket
port = 9999  # Port of the socket

"""Server class"""

MSSLogger.intializelogger()
class Server:
    logger = MSSLogger.getlogger("serverlogger")
    def __init__(self):
        """Socket Creation"""
        try:
            self.logger.info("creating a socket connection")
            self.ss = socket.socket()
        except socket.error as msg:  # IN case connection timed out and socket craetion is failed.
            print("Socket Creation error: " + str(msg))

    def bind_socket(self):
        """Binding the socket and listening for connection"""
        try:
            print("Binding the port " + str(port))
            self.ss.bind((host, port))
            self.ss.listen(5)

        except socket.error as msg:
            self.logger.error("socket binding error: " + str(msg) + "\n" + "Retrying ....")
            print("socket binding error: " + str(msg) + "\n" + "Retrying ....")
            self.bind_socket()

    def accept_socket(self):
        """Connection establishment with client"""
        conn, (IPAddr, Port) = self.ss.accept()
        self.logger.info("connection has been established " + "with IP " + IPAddr + " and port " + str(Port))
        print("connection has been established.\nServer listening at " + IPAddr + ":" + str(Port)+" ...")
        select_service = "Select any Service:\nType 1 for 'Echo'\nType 2 for 'File Transfer'"
        self.recv_data(conn, select_service)
        conn.close()

    def recv_data(self, conn, select_service):
        """Receiving data for choices"""
        conn.send(select_service.encode('utf-8'))
        try:
            client_res = conn.recv(1024)
            conn.send(client_res)
            self.logger.info("######## Client Requested for '" + self.selected_service(client_res) + "' Service ########")
            print("######## Client Requested for '" + self.selected_service(client_res) + "' Service ########")
            self.select_choice(conn, client_res)
        except socket.error as msg:
            self.logger.info("Socket error: " + str(msg))

    def selected_service(self, select_service):
        try:
            serv_name = select_service.decode('utf-8')
            if serv_name == '1':
                selected_service = "Echo"
            elif serv_name == '2':
                selected_service = "File Transfer"
            else:
                selected_service = "Invalid"
            return selected_service
        except socket.error as msg:
            self.logger.info("error while fetching service name: " + str(msg))

    def select_choice(self, conn, choice):
        """Choice selected """
        if choice.decode('utf-8') == "1":
            echo_str = "======You have choosed ECHO service !!!====== \n======Press Quit/Exit to Terminate service======"
            conn.send(echo_str.encode('utf-8'))
            self.server_echo(conn)
        if choice.decode('utf-8') == "2":
            self.server_fts()

    def server_echo(self, conn):
        """Echo Server """
        flag = True
        while True:
            client_res = conn.recv(1024)
            plain_text = client_res.decode('utf-8')
            self.logger.info("Input received from client: " + plain_text)
            if flag:
                print("Messages received from client:\n", plain_text)
                flag = False
            else:
                print(plain_text)
            if plain_text.lower() == "quit" or plain_text.upper() == "QUIT" or plain_text.lower() == "exit" or plain_text.upper() == "EXIT":
                conn.send("Disconnecting from server ...\a".encode('utf-8'))
                break
            conn.sendall(client_res)
        conn.close()

    def server_fts(self):
        pass  # function fot FTS code will come


def main():
    """Main Function"""
    server_obj = Server()
    server_obj.bind_socket()
    server_obj.accept_socket()


if __name__ == "__main__":
    main()
