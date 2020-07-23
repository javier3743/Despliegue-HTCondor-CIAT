# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.define "master" do |master|

# Box que utilizaremos
      master.vm.box = "ubuntu/xenial64"

# Hostname
      master.vm.hostname = "master1"

# Aprovisionamiento
      master.vm.provision "shell", path: "masterInstaller.sh", privileged: true
      master.vm.provision "file", source: "ClusterMonitoring", destination: "$HOME/ClusterMonitoring"


# Red privada
      master.vm.network "private_network", ip: "172.22.52.18"
      master.vm.network "forwarded_port", guest: 8000, host: 8000
      master.vm.provider :virtualbox do |vb|
        vb.customize ["modifyvm", :id, "--memory", 512]
      end

  end

# Nodo de procesamiento 1
  config.vm.define "node1" do |node1|

# Box que utilizaremos
      node1.vm.box = "ubuntu/xenial64"

# Hostname
      node1.vm.hostname = "node1"

# Script de aprovisionamiento
      node1.vm.provision "file", source: "ClusterMonitoring/Server/daemon.py", destination: "$HOME/daemon.py"
      node1.vm.provision "shell", path: "nodeInstaller.sh", privileged: true

# Red privada
      node1.vm.network "private_network", ip: "172.22.52.19"
      node1.vm.provider :virtualbox do |vb|
        vb.customize ["modifyvm", :id, "--memory", 512]
      end

  end

# Nodo de procesamiento 2
  config.vm.define "node2" do |node2|

      node2.vm.box = "ubuntu/xenial64"
      # Box que utilizaremos

# Hostname
      node2.vm.hostname = "node2"

# Script de aprovisionamiento
      node2.vm.provision "file", source: "ClusterMonitoring/Server/daemon.py", destination: "$HOME/daemon.py"
      node2.vm.provision "shell", path: "nodeInstaller.sh", privileged: true

# Red privada
      node2.vm.network "private_network", ip: "172.22.52.20"
      node2.vm.provider :virtualbox do |vb|
        vb.customize ["modifyvm", :id, "--memory", 512]
      end

  end
end
