#!/bin/bash
 
set -e
 
if [ $(id -u) -ne 0 ]
then
	echo "Must be run as root"
	exit 1
fi

function debian_dependencies
{
    echo "Updating the system."
    apt-get update && apt-get dist-upgrade -y
    
    echo "Installing some interesting package."
    apt-get install -y \
    curl python build-essential \
    'libbz2-dev' 'libsqlite3-dev' 'zlib1g-dev' 'libxml2-dev' 'libxslt1-dev' 'libgdbm-dev' 'libgdb-dev' 'libxml2' 'libssl-dev' 'tk-dev' 'libgdbm-dev' 'libexpat1-dev' 'libncursesw5-dev' \
    uuid-dev libmysqlclient-dev mysql-server git
}

function debian_dependencies
{
    echo "Updating the system."
    yum update -y

    echo "Installing package needed to build things."
    yum -y install gcc gcc-c++ make
    echo "Installing package needed to build python."
    yum -y install openssl-devel* zlib*.x86_64
    echo "Installing package needed to build zmq."
    yum -y install libuuid-devel
    echo "Installing git."
    yum -y install git
}
 
function install_zmq
{
    if [ -f /usr/local/lib/libzmq.so ]
    then
        echo "ZeroMQ seems to be already installed, skipping."
        return 0
    fi
	if [ -z "$1" ]                           # Is parameter #1 zero length?
	then
		echo "Need the version number !"  # Or no parameter passed.
		return 1
	fi
	ZMQVERS=$1
	echo "Downloading and compiling zeromq version $ZMQVERS."
	wget http://download.zeromq.org/zeromq-$ZMQVERS.tar.gz
	tar xzvf zeromq-$ZMQVERS.tar.gz
	cd zeromq-$ZMQVERS
	./configure
	make
	make install
	cd -
	rm -rf zeromq-$ZMQVERS zeromq-$ZMQVERS.tar.gz
    echo /usr/local/lib >> /etc/ld.so.conf.d/zmq.conf
	ldconfig
	echo "Installed zeromq."
}

if [ -f /etc/debian_version ]
then
    debian_dependencies
    adduser --system --force-badname --home /opt/4am/ --shell /bin/bash --disabled-password 4am
else if [ -f /etc/centos-release ]
then
    centos_dependencies
    adduser --system --home /opt/4am/ --shell /bin/bash  --create-home 4am
else
    echo "Unsupported system, sorry."
fi

install_zmq 2.1.11
 
 
cat > /opt/4am/4am-deploy.sh <<EOF
#!/bin/bash

set -e 

echo "Installating of python through pythonbrew."
curl -kL http://xrl.us/pythonbrewinstall | bash
echo source /opt/4am/.pythonbrew/etc/bashrc >> ~/.bashrc
source /opt/4am/.pythonbrew/etc/bashrc
pythonbrew install --configure="--with-threads --enable-shared" \
                   --force \
                   --no-setuptools \
                   --jobs=2 \
                   --verbose 2.7.2
# Tricks cause it's not returning 0 on sucess
set +e
pythonbrew switch 2.7.2
set -e
echo export LD_LIBRARY_PATH=~/.pythonbrew/pythons/Python-2.7.2/lib >> ~/.bashrc
export LD_LIBRARY_PATH=~/.pythonbrew/pythons/Python-2.7.2/lib
echo "Installation of python completed."

echo "Installing pip."
curl -O http://python-distribute.org/distribute_setup.py
python distribute_setup.py && easy_install pip

echo "Installing some python packages."
pip-2.7 install pyzmq sqlalchemy MySQL-python paramiko

git clone git://github.com/sx4it/4am-core.git
cd 4am-core/
git checkout experimental
ssh-keygen -b 2048 -t rsa -f ~/.ssh/id_rsa -N ""
EOF

chmod +x /opt/4am/4am-deploy.sh
su -l -c /opt/4am/4am-deploy.sh 4am
rm /opt/4am/4am-deploy.sh
 
