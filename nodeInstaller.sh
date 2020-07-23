#!/bin/bash

## Instalacion
wget -qO - https://research.cs.wisc.edu/htcondor/ubuntu/HTCondor-Release.gpg.key | sudo apt-key add -

echo "deb http://research.cs.wisc.edu/htcondor/ubuntu/8.8/xenial xenial contrib" >> /etc/apt/sources.list
echo "deb-src http://research.cs.wisc.edu/htcondor/ubuntu/8.8/xenial xenial contrib" >> /etc/apt/sources.list

apt-get update

apt-get install -y condor libglobus-gss-assist3 htop members tree
############################################################################################
# FQDN
sed -i '$ d' /etc/hosts
sed -i '$ d' /etc/hosts

cat << EOT >> /etc/hosts
$(/sbin/ifconfig enp0s8 | grep -i mask | awk '{print $2}'| cut -f2 -d:) $(hostname).ciat.cgiar.org $(hostname)
172.22.52.18 master1.ciat.cgiar.org master1
EOT

######################################################################################

#Configuracion HTCondor-Docker

cat << EOT >> /etc/condor/condor_config.local
# Condor Master
CONDOR_HOST = 172.22.52.18

# User ID Domain
UID_DOMAIN = ciat.cgiar.org

# Filesystem Domain
FILESYSTEM_DOMAIN = ciat.cgiar.org

# Deshabilitar uso de Swap / Disable Swap use.
RESERVED_SWAP = 0

# Condor Worker
DAEMON_LIST = MASTER,STARTD

# Allowed computers / Equipos permitidos
ALLOW_WRITE = *.ciat.cgiar.org

# IP to use/IP a usar
NETWORK_INTERFACE = $(hostname -i)

# Create only 1 Slot / Crear solo 1 Slot
NUM_SLOTS = 1

# Slot resources: 100% / Recursos del Slot: 100%
SLOT_TYPE_1 = cpu=100%, ram=100%, swap=100%, disk=95%

# Enable dynamic resources in Slot1 / Habilitar recursos dinamicos en Slot1
SLOT_TYPE_1_PARTITIONABLE = True

# Create Slot / Crear Slot
NUM_SLOTS_TYPE_1 = 1

# Default Memory if none is requiered 1024MB
MODIFY_REQUEST_EXPR_REQUESTMEMORY = quantize(RequestMemory, {200})

# Enable unexistent user jobs / Permitir tareas de usuarios no existentes
SHADOW_RUN_UNKNOWN_USER_JOBS = True
SOFT_UID_DOMAIN = True

# Red LAN
PRIVATE_NETWORK_NAME = ciat.cgiar.org

STARTER_ALLOW_RUNAS_OWNER=False
EOT

######################################################################################

#Grupos y usuarios

usermod -aG condor $(getent passwd "1000" | cut -d: -f1)

######################################################################################

#Reboot services

service condor restart

######################################################################################

# ClusterMonitoring

cat << EOT >> /home/vagrant/mycron
* * * * * python3 /home/vagrant/daemon.py
EOT

crontab -u vagrant /home/vagrant/mycron

rm /home/vagrant/mycron
