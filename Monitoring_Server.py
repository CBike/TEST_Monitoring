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
fail_list = set([])


class Server():
    def __init__(self):
        self.util = Util()
        self.util.create_folder('c:/TMS/')
        self.logger = logging.getLogger('Server')

    def threaded(self, client_socket, addr):
        self.logger.info('connected by {0} : {1} '.format(addr[0], addr[1]))

        while True:
            try:
                recv_data = client_socket.recv(1024)
                decode_data = recv_data.decode()

                if decode_data in pcid_list:
                    current_time = datetime.now()
                    timestamp = current_time.strftime(dateformat)
                    pcid_list[decode_data] = timestamp
                else:
                    self.logger.info('Wrong PCID DATA Received:{0}'.format(decode_data))

                self.logger.info('Monitoring Data : {}'.format(pcid_list))

                self.check_timestamp()

                if not recv_data:
                    self.logger.info('Disconnected by {0} : {1}'.format(addr[0], addr[1]))
                    break

                self.logger.info('Received by {0} : {1} PCID : {2}'.format(addr[0], addr[1], decode_data))


            except ConnectionResetError as e:
                self.logger.error('ConnectionResetError occurs :: {}'.format(e))
                self.logger.error('Disconnected by {0} : {1} '.format(addr[0], addr[1]))
                break

        client_socket.close()


    def make_pc_checking_dict(self):
        number_of_pc = int(input('How many PCs are you planning to monitor?'))
        self.logger.info('PCID: {0} ~ PCID: {1} Monitoring Start'.format(0, number_of_pc - 1))
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
                if diff_h >= 0.1:
                    self.logger.info('PCID:{} is error occurs'.format(i))
                    fail_list.add(i)
                else:
                    if i in fail_list:
                        fail_list.discard(i)

    def write_fail_log(self):
        f = open('c:/TMS/fail_list.txt', 'w')
        f.write('{}'.format(fail_list))


        self.logger.info('Monitoring FAIL LIST :: {0}'.format(fail_list))


if __name__ == '__main__':

    server = Server()
    server.make_pc_checking_dict()



    HOST = ''
    PORT =

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    server.logger.info('Server start')

    while True:
        server.logger.info('Socket is waiting')
        server.write_fail_log()
        client_socket, addr = server_socket.accept()
        start_new_thread(server.threaded, (client_socket, addr))


    server_socket.close()