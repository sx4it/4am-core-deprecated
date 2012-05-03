#!/usr/bin/env python

import fabric.api import run, env, get as fabrun, fabenv, fabget

def getAuthorizedKeys():
    fabget('~/.ssh/authorized_keys')



if __name__ == "__main__":
    fabenv.host_string = '192.168.0.112'
    fabenv.no_agent = True
    fabenv.reject_unknown_hosts = True
    fabenv.user = 'root'
    fabenv.key_filename = '/root/ct2'
    fabenv.abort_on_prompts = True
    getAuthorizedKeys()
    fabric.network.disconnect_all()
