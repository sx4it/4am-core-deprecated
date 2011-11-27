#!/usr/bin/env python

import logging
import Server
 
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    Server.run()
