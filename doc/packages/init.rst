Init Script
==============

The ``init.py`` script is used to upload a new key to the sql server, it use the *server.conf* file. It connect remotly to the database and upload the desired key for your account.

**Usage: init.py [options]**
  Options:
    -h, --help                          show this help message and exit
    -p PATH, --key-path=PATH            key path
    --database-port=PORT_NB             database port
    --database-ip=IP                    database ip
    --database-user=USER                database user
    --database-pass=PASS                database pass
    --database-name=NAME                database name
    --database-controller=controller    database controller

