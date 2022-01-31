import requests,urllib3
urllib3.disable_warnings()

class api_base:
    
        def __init__(self,host,username,password):
            self.host = host
            self.username = username
            self.password = password
            self.UIDARUBA = ''
            self.session = ''
            self.headers = {"Accept": "application/json"}
            
        def login(self):
                try:
                    login_url = f"https://{self.host}:4343/v1/api/login"
                    querystring = {"username":f"{self.username}","password":f"{self.password}"}            
                    self.session = requests.session()
                    login = self.session.post(login_url,data=querystring,verify=False)
                    self.UIDARUBA = login.json()['_global_result']['UIDARUBA']
                    print(f"Login successful: {login.status_code}")
                    return True
                except:
                    print('Login failed')
                    return False

        def command(self,endpoint,path='/mm'):
            url = f"https://{self.host}:4343/{endpoint}"
            full_url=url+"&UIDARUBA="+self.UIDARUBA
            querystring = {"config_path":{path}}
            result = self.session.get(full_url, headers=self.headers, params=querystring)
            return result

        def logout(self):
            logout_url = f"https://{self.host}:4343/v1/api/logout"
            logout = self.session.post(logout_url, verify=False)
            print(f'Logout successful: {logout.status_code}')

if __name__ == '__main__':
    mc1 = api_base(host='10.1.149.100',username='admin',password='aruba123')
    mc1_conn=mc1.login()
    if mc1_conn:
            result=mc1.command(endpoint="v1/configuration/object/vlan_id")
            print(result.json())
            mc1.logout()
