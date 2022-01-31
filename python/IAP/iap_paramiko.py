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
            print('Failed to connect sw')
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

class sw_config():
	def __init__(self,sw_ip,sw_pass):
		self.sw_ip = sw_ip
		self.sw_password = sw_pass
		self.config_folder = 'configs'

	def sw_commands(self,config_file):
		print('##### Checking sw configs to send')
		# Building list of config files
		sw_configs = []
		result = []
		sw_configs.append(config_file)
		print('##### Pushing configs to sw with SSH..')
		# Establishing SSH conn and sending commands
		sw = ssh_base(host=self.sw_ip,port='22',password=self.sw_password)
		sw_conn = sw.login()
		if sw_conn:
			for i in sw_configs:
				print(f'Pushing configs from: {i}')
				with open(f'{self.config_folder}/{i}') as f:
					for l in f.readlines():
						result.append(sw.exec_command(l))
			sw.logout()
			print(f'Completed configs load')
			return result
		else:
			print(f'Configs load failed')

def main():

	sw1 = sw_config('10.1.145.150','admin1')
	result=sw1.sw_commands('show.txt')
	print(result)

if __name__ == '__main__':
    main()


