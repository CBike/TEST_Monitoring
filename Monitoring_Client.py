import socket
import json
import logging.config
import os



with open("TMS_logger.json") as f:
    logger_config = json.load(f)

logging.config.dictConfig(logger_config)
logger = logging.getLogger("Client")


def create_folder(dir_path):
    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            logger.info("[TOOL] FOLDER CREATE : {}".format(dir_path))
        else:
            logger.info("[TOOL] FOLDER IS ALREADY EXIST : {}".format(dir_path))
    except OSError as e:
        logger.error('OS Error Occur :{} '.format(e) + dir_path)




def connect_server(HOST, PORT, PCID):
    PCID = str(PCID)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    logger.info('Client Connect to {} {} Server '.format(HOST,PORT))
    client_socket.send(PCID.encode())
    logger.info('Client Send Message({}) to Server'.format(PCID))
    client_socket.close()


if __name__ == '__main__':
    create_folder('c:/TMS/log/')

    HOST = ''
    PORT =
    connect_server(HOST, PORT, 4)
