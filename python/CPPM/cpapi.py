from requests import Request, Session
from time import time
from urllib.parse import urljoin, urlparse, urlunparse
import urllib3,logging
urllib3.disable_warnings()

_session = Session()
logging.basicConfig(level=logging.INFO,format='%(message)s')

class Client:

        def __init__(self, host='', timeout=60, insecure=False,
                                 access_token=None, client_id=None, client_secret=None, username=None, password=None):
                self.host = host
                self.timeout = timeout
                self.insecure = insecure
                self.token_type = 'Bearer'
                self.access_token = access_token
                self.access_token_expires = None
                self.client_id = client_id
                self.client_secret = client_secret
                self.username = username
                self.password = password

        def cppm(self, method, uri, query_params=None, body=None, authz=True):
                headers = {}
                if authz:
                        headers['Authorization'] = self.authHeader()
                url = self.getUrl(uri)
                try: 
                        response = _session.request(method, url, params=query_params,
                                headers=headers, json=body, timeout=self.timeout, verify=not self.insecure)
                        return response.json()
                except:
                        return None

        def getUrl(self, url):
                rel = urlparse(url)
                path = rel.path
                if len(path):
                        if path[0] != '/':
                                path = '/' + path
                        if path[0:4] != '/api':
                                path = '/api' + path
                return urljoin('https://' + self.host, urlunparse((rel.scheme, rel.netloc, path, rel.params, rel.query, rel.fragment)))

        def authHeader(self):
                if not self.access_token:
                        data = {'grant_type': 'password', 'client_id': self.client_id, 'username': self.username, 'password': self.password}
                        data['client_secret'] = self.client_secret
                        oauth = self.cppm('POST', '/oauth', None, data, False)                        
                        try:
                                self.token_type = oauth['token_type']
                                self.access_token = oauth['access_token']
                                self.access_token_expires = time() + oauth['expires_in']
                                return (self.token_type + ' ' + self.access_token)
                        except:
                                logging.info("Connection to ClearPass failed")

def main():
        print('Starting connection to ClearPass!')
        cp = Client(host='10.251.1.105',insecure=True,username='admin',password='eTIPS123',client_id='testClient')
        result=cp.cppm(uri='api/endpoint',method='GET')
        if result:
                print(result)

if __name__ == '__main__':
        main()
