#!/usr/bin/env bash

# get some env variables
user=$1
namespace=$2
cluster=$3

# create linux user and create home/cert directories
useradd ${user}
mkdir /home/${user}/
mkdir /home/${user}/.certs/
mkdir /home/${user}/.kube/

# generate certs and sign with kubernetes ca
openssl genrsa -out ${user}.key 2048
openssl req -new -key ${user}.key -out ${user}.csr -subj "/CN=${user}/O=07-rbac"
openssl x509 -req -in ${user}.csr -CA /etc/kubernetes/pki/ca.crt -CAkey /etc/kubernetes/pki/ca.key -CAcreateserial -out ${user}.crt -days 365

# copy certs to user dir
cp ${user}.* /home/${user}/.certs/

# create user config
rm -f /home/${user}/.kube/config
sudo cat /etc/kubernetes/admin.conf | head -n -12 >> /home/${user}/.kube/config
cat >> /home/${user}/.kube/config <<- EOM
- context:
    cluster: kubernetes
    namespace: ${namespace}
    user: ${user}
  name: ${user}@kubernetes
current-context: ${user}@kubernetes
kind: Config
preferences: {}
users:
- name: ${user}
  user:
    client-certificate-data: $(cat usr-blue.crt | base64 -i | paste -sd "" -)
    client-key-data: $(cat usr-blue.key | base64 -i | paste -sd "" -)
EOM

sudo chown -R $(id -u ${user}):$(id -g ${user}) /home/${user}/.kube/