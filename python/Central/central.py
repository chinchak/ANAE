from pycentral.base import ArubaCentralBase
from pycentral.monitoring import Sites
from pprint import pprint

class central:
    def __init__(self,token):
        self.token = token
        self.base_url = "https://apigw-prod2.central.arubanetworks.com"
        self.central_info = {
        "base_url": "https://apigw-prod2.central.arubanetworks.com",
        "token": {
            "access_token": self.token
            }
        }
        self.ssl_verify = True
        self.sites = Sites()
        
    def login(self):
        self.central = ArubaCentralBase(central_info=self.central_info,ssl_verify=self.ssl_verify)

    def central_req(self):
        apiPath = "/monitoring/v1/aps"
        apiMethod = "GET"
        apiParams = {
            "limit": 20,
            "offset": 0
        }
        base_resp = self.central.command(apiMethod=apiMethod,
                            apiPath=apiPath,
                            apiParams=apiParams)
        return(base_resp)

    def get_sites(self):        
        base_resp = self.sites.get_sites(conn=self.central)
        return(base_resp)

    def create_site(self,site_name,addr):        
        base_resp = self.sites.create_site(conn=self.central,site_name=site_name,site_address=addr)
        return(base_resp)

def main():
    cent = central(token="bL21laZ8v6rsylW7SeoHylwhmZ05NX9n")
    cent.login()
    
    base_resp=cent.central_req()
    
    for i in base_resp['msg']['aps']:
        print(f"AP model: {i['model']}, AP status: {i['status']}, AP IP addr: {i['ip_address']}")

    resp1=cent.get_sites()
    print(resp1)

    addr={'address':'Main street','city':'Detroit','country':'US'}
    resp2=cent.create_site('Site2',addr)
    print(resp2)


if __name__ == '__main__':
    main()
