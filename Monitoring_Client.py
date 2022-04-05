import json
import logging.config
import socket
from basic_config.util_function import Util


with open('./basic_config/TMS_logger.json') as f:
    logger_config = json.load(f)

logging.config.dictConfig(logger_config)



class Client():

    def __init__(self):
        self.util = Util()
        self.logger = logging.getLogger('Client')

    def connect_server(self, HOST, PORT, PCID):
        try:
            PCID = str(PCID)
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((HOST, PORT))
            self.logger.info('Client Connect to {} {} Server '.format(HOST,PORT))
            client_socket.send(PCID.encode())
            self.logger.info('Client Send Message({}) to Server'.format(PCID))
            client_socket.close()

            return client_socket
        except Exception as e:
            self.logger.info('Connect Server Exception :{}'.format(e))

if __name__ == '__main__':

    client = Client()

    HOST = ''
    PORT =
    client.connect_server(HOST, PORT, '0')
