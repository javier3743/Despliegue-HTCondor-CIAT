#!/bin/bash

## Instalacion
apt-get update

apt-get  install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

wget -qO - https://research.cs.wisc.edu/htcondor/ubuntu/HTCondor-Release.gpg.key | sudo apt-key add -

echo "deb http://research.cs.wisc.edu/htcondor/ubuntu/8.8/xenial xenial contrib" >> /etc/apt/sources.list
echo "deb-src http://research.cs.wisc.edu/htcondor/ubuntu/8.8/xenial xenial contrib" >> /etc/apt/sources.list

apt-get update

apt-get install -y condor libglobus-gss-assist3 docker-ce docker-ce-cli containerd.io cifs-utils htop members tree

curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
############################################################################################
# FQDN
sed -i '$ d' /etc/hosts
sed -i '$ d' /etc/hosts
cat << EOT >> /etc/hosts
$(/sbin/ifconfig enp0s8 | grep -i mask | awk '{print $2}'| cut -f2 -d:) $(hostname).ciat.cgiar.org $(hostname)
172.22.52.19 node1.ciat.cgiar.org node1
172.22.52.20 node2.ciat.cgiar.org node2
EOT

##############################################################################################################################
#Configuracion HTCondor-Docker

cat << EOT >> /etc/condor/condor_config.local
# Condor Master
CONDOR_HOST = 172.22.52.18

##  Mail parameters:
MAIL = /usr/bin/mail

##  Network domain parameters:
UID_DOMAIN = ciat.cgiar.org

FILESYSTEM_DOMAIN = ciat.cgiar.org

DAEMON_LIST = COLLECTOR, MASTER, NEGOTIATOR,SCHEDD,SHARED_PORT

# Equipos que pueden enviar tareas
ALLOW_WRITE= *.ciat.cgiar.org
ALLOW_READ= *.ciat.cgiar.org
NETWORK_INTERFACE=$(hostname -i)

PRIVATE_NETWORK_NAME = ciat.cgiar.org
COLLECTOR.MAX_FILE_DESCRIPTORS = 20000

# History parameters:
ENABLE_HISTORY_ROTATION = True
MAX_HISTORY_LOG = 20000000
MAX_HISTORY_ROTATIONS=100

# Containers start parameters
STARTER_ALLOW_RUNAS_OWNER=False

EOT

######################################################################################

#Grupos y usuarios

usermod -aG docker condor
usermod -aG docker $(getent passwd "1000" | cut -d: -f1)
usermod -aG condor $(getent passwd "1000" | cut -d: -f1)

######################################################################################

#Reboot services

service docker restart
service condor restart

######################################################################################

# ClusterMonitoring

docker-compose -f /home/vagrant/ClusterMonitoring/docker-compose.yml up -d
