#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import threading
import time

import requests

def mainloop():
    while True:
        try:
            data = requests.get('https://be.t21c.kro.kr/levels').text
            #data = data['results']
        except Exception as error:
            print(f'data got failed,reason:{error}\nReacquiring...')
        else:
            with open('data.txt','w+') as f:
                f.write(data)
                f.close()
            print('data has been gotten')
            time.sleep(3600)

def main():
    mainloop_thread = threading.Thread(target=mainloop)
    mainloop_thread.daemon = True
    mainloop_thread.start()
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MTL_DJango.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
