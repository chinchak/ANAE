from pyaoscx.session import Session
from pyaoscx.configuration import Configuration
import urllib3
urllib3.disable_warnings()

version = '10.04'
switch_ip = '10.251.14.103'
s = Session(switch_ip, version)

try:
    s.open('admin', 'aruba123')

    config = Configuration(s)
    test = config.get_full_config()
    for i in test['Port']:
        if 'ip4_address' in test['Port'][i].keys():
            print(f"Interface: {test['Port'][i]['interfaces']}, IP Address: {test['Port'][i]['ip4_address']}")
    print('Completed')

except Exception as error:
    print('Ran into exception: {}. Closing session.'.format(error))

finally:
    s.close()
