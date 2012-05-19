# Installation

The script deploy.sh at the root of the repository takes care of the installation of the server.
The server is installed under a new user called 4am and a specific version of Python is installed and compiled.

```
wget --no-check-certificate https://raw.github.com/sx4it/4am-core/experimental/deploy.sh
bash deploy.sh
```

# Creation of the database
The preferred database server is MySQL.

```
CREATE DATABASE `4am_experimental` CHARACTER SET utf8;
```

# Configuring the server

* Take the role of the 4am user
```
su - 4am
```

* Copy the sample confirmation file and customize it if needed
```
cp 4am-core/4am.conf.sample ~/.4am.conf
```

* Push your user public key with 4am-init
```
4am-init --key-path id-mykey.pub
```

# Launching the server
* Take the role of the 4am user
```
su - 4am
```

* Launch the controller
```
4am-controller
```

* Launch the ssh handler
```
4am-sshd
```

# Errors

If you encounter path problems, source the setenv.sh script at the root of the repo.
If you have installed the software with the deployment script, it should have been added to the .bashrc file of the 4am user.
