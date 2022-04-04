import logging.config
import socket
from datetime import datetime
from _thread import *
import json
import os

with open("TMS_logger.json") as f:
    logger_config = json.load(f)

logging.config.dictConfig(logger_config)
logger = logging.getLogger("Server")


pcid_list = {}
dateformat = "%Y-%m-%d %H:%M:%S"
failist = set([])

def create_folder(dir_path):
    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            logger.info("[TOOL] FOLDER CREATE : {}".format(dir_path))
        else:
            logger.info("[TOOL] FOLDER IS ALREADY EXIST : {}".format(dir_path))
    except OSError as e:
        logger.error('OS Error Occur :{} '.format(e) + dir_path)




def threaded(client_socket, addr):
    print('connected by {0} : {1} '.format(addr[0], addr[1]))

    while True:
        try:
            data = client_socket.recv(1024)

            if data == 'None' or '':
                logger.warning('Receive Data is Nore or Empty Data :{}'.format(data.decode()))

            pcid = data.decode()
            currenttime = datetime.now()
            timestamp = currenttime.strftime(dateformat)
            pcid_list[pcid] = timestamp
            print(pcid_list)
            check_timestamp()

            if not data:
                logger.info('Disconnected by {0} : {1}'.format(addr[0], addr[1]))
                break

            logger.info('Received by {0} : {1} PCID : {2}'.format(addr[0], addr[1], pcid))


        except ConnectionResetError as e:

            logger.error('ConnectionResetError occurs :: {}'.format(e))

            logger.error('Disconnected by {0} : {1} '.format(addr[0], addr[1]))
            break

    client_socket.close()


def make_pc_checking_dict():
    number_of_pc = int(input('How many PCs are you planning to monitor?'))
    logger.info('PCID{0} ~ PCID{1} Monitoring Start'.format(0,number_of_pc))
    for i in range(0, number_of_pc):
        pcid_list['{}'.format(i)] = 'None'

def check_timestamp():
    current_time = datetime.now()
    for i in pcid_list:
        if pcid_list[i] == 'None':
            pass

        else:
            timestamp = datetime.strptime(pcid_list[i], dateformat)
            diff = current_time - timestamp
            diff_h = diff.seconds/3600
            if diff_h >= 2:
                logger.info('PCID:{} is error occurs'.format(i))
                failist.add(i)
            else:
                if i in failist:
                    failist.discard(i)

def write_failist_log():
    logger.info('faillist::{0}'.format(failist))
    pass


if __name__ == '__main__':
    create_folder('c:/TMS/log/')
    create_folder('c:/TMS/failist/')

    make_pc_checking_dict()



    HOST = ''
    PORT =

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    logger.info('Server start')

    while True:
        logger.info('Socket is waiting')
        client_socket, addr = server_socket.accept()
        start_new_thread(threaded, (client_socket, addr))
        write_failist_log()


    server_socket.close()