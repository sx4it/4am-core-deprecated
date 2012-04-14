# TODO before launching the server

* Before running client.py, push your user public key with addUserAndKey.py.


# Deployment

## Usage

```
#!/bin/sh
 
set -e
 
echo "Updating the system."
apt-get update && apt-get dist-upgrade
 
echo "Installing some interesting package."
apt-get install git python-crypto python-support python build-essential \
python-pip python-paramiko uuid-dev python-dev libmysqlclient-dev mysql-server -y
 
echo "Downloading and compiling zeromq."
wget http://download.zeromq.org/zeromq-2.1.10.tar.gz
tar xzvf zeromq-2.1.10.tar.gz
cd zeromq-2.1.10
./configure 
make
make install
cd -
rm -rf zeromq-2.1.10
rm zeromq-2.1.10.tar.gz
echo "Installed zeromq."
 
echo "Installing some python packages."
pip install pyzmq sqlalchemy MySQL-python
 
git clone git://github.com/sx4it/4am-core.git
cd 4am-core/
git checkout experimental
ssh-keygen -b 2048 -t rsa -f ${HOME}/.ssh/id_rsa -N ""
```
