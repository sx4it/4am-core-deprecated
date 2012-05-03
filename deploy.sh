#!/bin/bash
 
set -e

## Default values
DEPLOYHOME=/opt/4am/
PYTHONVERS="2.7.3"
## End default values
 
if [ $(id -u) -ne 0 ]
then
	echo "Must be run as root"
	exit 1
fi

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

function usage
{
    cat <<EOF
Usage: $0 [options]

Options:
  -h, --help            show this help message and exit
  --database mysql|postgresql
                        install and configure mysql or postgresql
  --home PATH
                        full path to the users home directory (default $DEPLOYHOME)
EOF
}

while :
do
    case "$1" in
        -h | --help)
        usage
        exit 0
        ;;
        --database)
        #if [ "$2" != 'mysql' ] && [ "$2" != 'postgresql' ]
        if [ "$2" != 'mysql' ]
        then
            echo "Error: Unknown/unsupported engine: '$2'" >&2
            usage
            exit 1
        fi
        DATABASE=$2
        shift 2
        ;;
        --home)
        DEPLOYHOME=$2
        shift 2
        ;;
        -*)
        echo "Error: Unknown option: $1" >&2
        usage
        exit 1
        ;;
        *)  # No more options
        break
        ;;
    esac
done


# Define different functions depending on the operating system
if [ -f /etc/debian_version ]
then
    # DEBIAN
    function dependencies
    {
        echo "Updating the system."
        apt-get update && apt-get dist-upgrade -y
        
        echo "Installing some interesting package."
        apt-get install -y \
        curl python build-essential \
        'libbz2-dev' 'libsqlite3-dev' 'zlib1g-dev' 'libxml2-dev' 'libxslt1-dev' 'libgdbm-dev' 'libgdb-dev' 'libxml2' 'libssl-dev' 'tk-dev' 'libgdbm-dev' 'libexpat1-dev' 'libncursesw5-dev' \
        uuid-dev libmysqlclient-dev git
    }

    function mysql_install
    {
        #INSTALLER_LOG=/var/log/non-interactive-installer.log
        DEBIAN_FRONTEND=noninteractive apt-get install -q -y mysql-server pwgen
    
        # Alternatively you can set the mysql password with debconf-set-selections
        MYSQL_PASS=$(pwgen -s 12 1)
        mysql -uroot -e "UPDATE mysql.user SET password=PASSWORD('${MYSQL_PASS}') WHERE user='root'; FLUSH PRIVILEGES;"
        echo "MySQL Password set to '${MYSQL_PASS}'. Remember to delete ~/.mysql.passwd" | tee ~/.mysql.passwd
    }

    function addDedicatedUser
    {
        echo "Adding user..."
        adduser --system --force-badname --home $DEPLOYHOME --shell /bin/bash --disabled-password 4am
    }

elif [ -f /etc/centos-release ]
then
    function dependencies
    {
        echo "Updating the system."
        yum update -y
    
        echo "Installing package needed to build python, zmq and some python packages."
        yum -y install gcc gcc-c++ make \
        openssl-devel* zlib*.x86_64 \
        libuuid-devel mysql-devel \
        git
    }
 
    function addDedicatedUser
    {
        echo "Adding user..."
        adduser --system --home $DEPLOYHOME --shell /bin/bash  --create-home 4am
    }
else
    echo "Unsupported operating system, sorry."
    exit 1
fi

dependencies

if [ "$DATABASE" = "mysql" ]
then
    echo "Configuring $DATABASE"
    mysql_install
elif [ "$DATABASE" = "postgresql" ]
then
    postgresql_install
fi

addDedicatedUser

install_zmq 2.1.11
 
 
cat > ${DEPLOYHOME}4am-deploy.sh <<EOF
#!/bin/bash

set -e 

echo "Installating of pythonbrew."
if [ "\$(pythonbrew --version)" != "1.3" ]
then
        curl -kL http://xrl.us/pythonbrewinstall | bash
        source ~/.pythonbrew/etc/bashrc
        echo source ~/.pythonbrew/etc/bashrc >> ~/.bashrc
        cat > ~/.profile <<DOTPROFILE
# ~/.profile: executed by Bourne-compatible login shells.

if [ "\\\$BASH" ]; then
  if [ -f ~/.bashrc ]; then
    . ~/.bashrc
  fi
fi

mesg n
DOTPROFILE
fi

## Could be replaced by a direct install of python without pythonbrew
echo "Installating of python through pythonbrew."

# Was for python 2.7.2 (or because pythonbrew was broken)
if [ "$PYTHONVERS" = "2.7.2" ]
then
    pythonbrew install --configure="--with-threads --enable-shared" \
                       --force \
                       --no-setuptools \
                       --jobs=2 \
                       --verbose $PYTHONVERS
    # Tricks cause it's not returning 0 on sucess
    set +e
    pythonbrew switch $PYTHONVERS
    set -e
    export LD_LIBRARY_PATH=~/.pythonbrew/pythons/Python-${PYTHONVERS}/lib
    echo export LD_LIBRARY_PATH=~/.pythonbrew/pythons/Python-${PYTHONVERS}/lib >> ~/.bashrc
    echo "Installing pip."
    curl -O http://python-distribute.org/distribute_setup.py
    python distribute_setup.py && easy_install pip
else
    pythonbrew install ${PYTHONVERS}
    # Tricks cause it's not returning 0 on sucess
    set +e
    pythonbrew switch $PYTHONVERS
    set -e
fi

echo "Installation of python completed."

echo "Installing some python packages."
pip-2.7 install pyzmq sqlalchemy MySQL-python paramiko

git clone git://github.com/sx4it/4am-core.git
cd 4am-core/
git checkout experimental
ssh-keygen -b 2048 -t rsa -f ~/.ssh/id_rsa -N ""

echo source ~/4am-core/setenv.sh >> ~/.bashrc
EOF

chmod +x ${DEPLOYHOME}4am-deploy.sh
su -l -c ${DEPLOYHOME}4am-deploy.sh 4am
# Could be removed but not mandatory
#rm /opt/4am/4am-deploy.sh

cat <<EOF
Your installation is finished you now need to init the database.
Blabla 4am-init
EOF
 
exit 0
