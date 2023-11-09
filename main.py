import logging

from utils import *
from myAllTask import my_AllTask

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', encoding='utf-8')

def main():
    connect_to_device()
    my_AllTask.run()

if __name__ == "__main__":
    main()