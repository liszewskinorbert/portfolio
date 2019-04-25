import os, paramiko
#paramiko.util.log_to_file('paramiko.log')
import warnings
warnings.filterwarnings(action='ignore',module='.*paramiko.*')




class Server:

    def __init__(self, port=22):
        self.port=port
        self.name = ""
        self.user=""
        self.passw=""

    def ssh_client(self, ip, port, user, passwd ,key, command):
        client=paramiko.SSHClient()
        if key:
            client.load_host_keys(key)
        else:
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip, port=port, username=user, password=passwd)
            ssh_session=client.get_transport().open_session()
            if ssh_session.active:
                ssh_session.exec_command(command)
                print(ssh_session.recv(4096).decode(encoding="utf-8"))

            client.close()


if __name__ == '__main__':

    myServer = Server()
    os.system('cls')
    print("Asystent rosetty, jakie masz polecenie ?")
    myServer.name = input("Podaj mi adres IP: ")
    myServer.user = input("Podaj mi nazwę usera: ")
    myServer.passw = input("Podaj mi haslo do zalogowania: ")
    print("Podałes {} :)".format(myServer.name))
    while True:
        print(" ")
        print("-------------------- ")
        print("[H] Hosty            ")
        print("[P] pingi            ")
        print("[L] logi             ")
        print("[F] users            ")
        print("[S] uslugi           ")
        print("[D] Disks            ")
        print("[X] Exit             ")
        print("---------------------")
        action = input("Twój wybór: ").upper()
        if action not in "HPLFSDX" or len(action) != 1:
            os.system('cls')
            print("Nie wiem jak mam to wykonać")
            continue
        if action == 'H':
            os.system('cls')
            myServer.ssh_client(myServer.name, myServer.port, myServer.user, myServer.passw, '', 'cat /etc/hosts')
        elif action == 'P':
            os.system('cls')
            myServer.ssh_client(myServer.name, myServer.port, myServer.user, myServer.passw, '', 'ping 8.8.8.8')
        elif action == 'F':
            os.system('cls')
            myServer.ssh_client(myServer.name, myServer.port, myServer.user, myServer.passw, '', 'cat /etc/passwd')
        elif action == 'S':
            os.system('cls')
            myServer.ssh_client(myServer.name, myServer.port, myServer.user, myServer.passw, '', 'ps -auxw |grep java')
        elif action == 'L':
            os.system('cls')
            myServer.ssh_client(myServer.name, myServer.port, myServer.user, myServer.passw, '', 'tail -n 100 /var/log/syslog')
        elif action == 'D':
            os.system('cls')
            myServer.ssh_client(myServer.name, myServer.port, myServer.user, myServer.passw, '', 'mount')
        elif action == 'X':
            os.system('cls')
            print(" ... astalavista baby ....")
            exit()


