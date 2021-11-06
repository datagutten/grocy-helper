from time import sleep

import requests

count = 0
while True:
    try:
        response = requests.get('http://localhost:9283', timeout=2)
        if response.status_code == 200:
            print('Success')
            break
    except requests.exceptions.ConnectionError:
        print('Wait %d\r' % count)
        count += 1
        sleep(1)
