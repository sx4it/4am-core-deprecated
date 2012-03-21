Client Script
=============

You can use a simple prompt to query the server::

    ./client.py [cmd]

    Usage: client.py [options]
      Options:
        -h, --help                          show this help message and exit
        -p PATH, --key-path=PATH            key path
        --database-port=PORT_NB             database port
        --database-ip=IP                    database ip
        --database-user=USER                database user
        --database-pass=PASS                database pass
        --database-name=NAME                database name
        --database-controller=controller    database controller

Example::

    ./client.py help

    ./client.py User.add name=foo firstname=bar

    ./client.py User.list

You can find more example by reading the user documentation or looking into the `api` module.
