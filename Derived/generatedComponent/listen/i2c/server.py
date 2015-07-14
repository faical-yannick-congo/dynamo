import json
from datetime import datetime, date
import sys


class I2CHandler:
    def __init__(self, config):
        self.config = config

    def schedule(self, message):
        #print "Schedule for i2c not yet implemented. But supposed to write the request into requests"
        pass   

    def process(self):
        pass

    def run(self):
        pass

if __name__ == "__main__":
    CONFIG = "default"
    if len(sys.argv) == 2:
        CONFIG = sys.argv[1]
    server = I2CHandler(CONFIG)
    server.run()