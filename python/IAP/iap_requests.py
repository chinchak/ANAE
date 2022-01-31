import requests,urllib3,json
urllib3.disable_warnings()

class api_base:
    
        def __init__(self,host,username,password):
            self.host = host
            self.username = username
            self.password = password
            self.sid = ''
            self.session = ''
            self.headers = {"Content-Type":"application/json"}
            
        def login(self):
                try:
                    login_url = f"https://{self.host}:4343/rest/login"
                    querystring = json.dumps({"user":self.username,"passwd":self.password})
                    self.session = requests.session()
                    login = self.session.post(login_url, data=querystring, headers=self.headers, verify=False, timeout=5)
                    self.sid = login.json()['sid']
                    print(f"Login status: {login.json()}")
                    return True
                except:
                    print('Login failed')
                    return False

        def show(self,command):
            url = f"https://{self.host}:4343/rest/show-cmd?iap_ip_addr={self.host}&cmd={command}"
            full_url=url+"&sid="+self.sid
            result = self.session.get(full_url, headers=self.headers)
            return result

        def logout(self):
            logout_url = f"https://{self.host}:4343/rest/logout"
            querystring = json.dumps({"sid":self.sid})
            logout = self.session.post(logout_url, verify=False, data=querystring, headers=self.headers)
            print(f'\nLogout status: {logout.json()}')

if __name__ == '__main__':
    iap1 = api_base(host='10.1.145.150',username='admin',password='admin1')
    iap1_conn = iap1.login()
    if iap1_conn:
            result = iap1.show('show%20ap%20bss-table')
            print(f"\n{result.json()}")
            iap1.logout()
