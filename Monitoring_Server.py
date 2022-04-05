import json
import logging.config
import socket
from datetime import datetime
from _thread import *
from basic_config.util_function import Util

with open('./basic_config/TMS_logger.json') as f:
    logger_config = json.load(f)

logging.config.dictConfig(logger_config)



pcid_list = {}
dateformat = "%Y-%m-%d %H:%M:%S"
failist = set([])


class Server():
    def __init__(self):
        self.util = Util()
        self.util.create_folder('c:/TMS/')
        self.logger = logging.getLogger('Server')

    def threaded(self, client_socket, addr):
        print('connected by {0} : {1} '.format(addr[0], addr[1]))

        while True:
            try:
                data = client_socket.recv(1024)
                data = data.decode()

                print(data, type(data))

                if data == 'None' or ' ' or not data:
                    self.logger.warning('Receive Data is Nore or Empty Data :{}'.format(data))
                    self.logger.info('Disconnected by {0} : {1}'.format(addr[0], addr[1]))
                    break

                currenttime = datetime.now()
                timestamp = currenttime.strftime(dateformat)
                pcid_list[data] = timestamp
                print(pcid_list)
                self.check_timestamp()



                self.logger.info('Received by {0} : {1} PCID : {2}'.format(addr[0], addr[1], data))


            except ConnectionResetError as e:

                self.logger.error('ConnectionResetError occurs :: {}'.format(e))

                self.logger.error('Disconnected by {0} : {1} '.format(addr[0], addr[1]))
                break

        client_socket.close()


    def make_pc_checking_dict(self):
        number_of_pc = int(input('How many PCs are you planning to monitor?'))
        self.logger.info('PCID{0} ~ PCID{1} Monitoring Start'.format(0, number_of_pc))
        for i in range(0, number_of_pc):
            pcid_list['{}'.format(i)] = 'None'

    def check_timestamp(self):
        current_time = datetime.now()
        for i in pcid_list:
            if pcid_list[i] == 'None':
                pass

            else:
                timestamp = datetime.strptime(pcid_list[i], dateformat)
                diff = current_time - timestamp
                diff_h = diff.seconds/3600
                if diff_h >= 2:
                    self.logger.info('PCID:{} is error occurs'.format(i))
                    failist.add(i)
                else:
                    if i in failist:
                        failist.discard(i)

    def write_failist_log(self):
        self.logger.info('faillist::{0}'.format(failist))
        pass


if __name__ == '__main__':

    server = Server()
    server.make_pc_checking_dict()



    HOST =
    PORT =

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    server.logger.info('Server start')

    while True:
        server.logger.info('Socket is waiting')
        client_socket, addr = server_socket.accept()
        start_new_thread(server.threaded, (client_socket, addr))
        server.write_failist_log()
    server_socket.close()