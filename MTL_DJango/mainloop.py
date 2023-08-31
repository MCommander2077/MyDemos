import time

import requests


def mainloop():
    while True:
        try:
            data = requests.get('https://be.t21c.kro.kr/levels').text
            # data = data['results']
        except Exception as error:
            print(f'data got failed,reason:{error}\nReacquiring...')
        else:
            with open('data.txt', 'w+', encoding='utf-8') as f:
                f.write(data)
                f.close()
            print('data has been gotten')
            time.sleep(3600)
