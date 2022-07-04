import socket


def TMS_run_client_bat(data):
    try:
        workingDir = ('C:\TEST_Monitoring')
        os.chdir(workingDir)
        for i in range(0,int(data)):
            os.system('C:\TEST_Monitoring\client_runner.bat')
            print('run TMS bat file COUNT : {}'.format(i))
            time.sleep(1)
    except Exception as e:
        print('TMS_run_client_bat fun : EXCEPTION OCCURS : {}'.format(e))