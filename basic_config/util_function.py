import os


class Util():

    def __init__(self):
        pass



    def create_folder(self, dir_path):
        try:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                print("[TOOL] FOLDER CREATE : {}".format(dir_path))
            else:
                print("[TOOL] FOLDER IS ALREADY EXIST : {}".format(dir_path))
        except OSError as e:
            print('OS Error Occur :{} '.format(e) + dir_path)


