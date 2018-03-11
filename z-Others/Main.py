import os
import time
import datetime

def create_file():

    now_time = datetime.datetime.now()

    with open('{}-{}-{}.txt'.format(now_time.hour,
                                    now_time.minute,
                                    now_time.second), 'w') as sf:

        sf.write(str(time.time()))
    sf.close()


if __name__ == '__main__':

    create_file()

















































