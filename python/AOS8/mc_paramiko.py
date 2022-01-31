import paramiko, logging, time
from pathlib import Path

class ssh_base():
    def __init__(self,host='',port='22',username='admin',password='',timeout=10):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.timeout = timeout

    def login(self):
        try:
            self.ssh.connect(self.host, self.port,username=self.username,password=self.password,timeout=self.timeout)
            self.ssh_conn = self.ssh.invoke_shell()
            return True
        except:            
            print('Failed to connect MC')
            return False

    def logout(self):
        self.ssh_conn.close()
        
    def exec_command(self,command,timeout=0.2):
        if command.startswith('!'):
            time.sleep(1)
        self.ssh_conn.send(command)
        time.sleep(timeout)
        output = self.ssh_conn.recv(5000)
        lines = output.decode("utf-8")
        return lines

class mc_config():
        def __init__(self,mc_ip,mc_pass):
                self.mc_ip = mc_ip
                self.mc_password = mc_pass
                self.config_folder = 'configs'

        def mc_commands(self,config_file):
                print('##### Checking MC configs to send')
                # Building list of config files
                mc_configs = []
                result = []
                mc_configs.append(config_file)
                print('##### Pushing configs to MC with SSH..')
                # Establishing SSH conn and sending commands
                mc = ssh_base(host=self.mc_ip,port='22',password=self.mc_password)
                mc_conn = mc.login()
                if mc_conn:
                        for i in mc_configs:
                                print(f'Pushing configs from: {i}')
                                with open(f'{self.config_folder}/{i}') as f:
                                        for l in f.readlines():
                                                result.append(mc.exec_command(l))
                        mc.logout()
                        print(f'Completed configs load')
                        return result
                else:
                        print(f'Configs load failed')

def main():

        mc1 = mc_config('10.1.149.100','aruba123')
        result = mc1.mc_commands('test.txt')
        print(result)

if __name__ == '__main__':
    main()


