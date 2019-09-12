# RBAC - Role Based Access Control

The source for this can be found on my [github](https://github.com/mrmcshane/k8s-training/tree/master/07-rbac).

Role Based Access Control (RBAC) is how we lock down access to resources/functionality in kubernetes. It can get reasonably complicated, but in this example, we will be creating one read/write user for each of the namespaces and one read-only user with access to the whole cluster.



## RBAC Overview

Go into a little detail how RBAC is condigured with a couple of diagrams.



## Structure

Your directory structure should look something like this:
```
07-rbac
|-- deployment-blue.yml
|-- deployment-green.yml
|-- rbac-blue.yml
|-- rbac-green.yml
`-- rbac-cluster.yml
```
This builds on and uses the containers from [04-namespaces](https://github.com/mrmcshane/k8s-training/tree/master/04-namespaces), so build the containers from that task if you haven't already.

The RBAC manifests don't need to be in seperate files, but it's easier to structure it this way for the task.


## Pre-req - Create Users

We will need to create local users and kubernetes signed certs for these users.
This will be done with `create_k8s_user.sh` below:
```
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
```

This can be called with the command (ensure it's given a nice `chmod +x`):
```
sudo ./create_k8s_user.sh usr-blue blue kubernetes
```

There is a more manual method of doing this which requires you to run commands as the user to create the config by passing arguments, but it's easier and more reproducable if you can auto-generate the conifg file based on the admin config with the generated certificates. Automation is better and the less user interaction the better.

Once this has been run as the `vagrant` user, you can switch users `sudo su usr-blue` and run `kubectl get all` to see what you have access to.


## Namespace Users

We will be doing this for two users, `usr-blue` and `usr-green`. We will use `usr-blue` in this example.

### Create User

```yaml
code: snippet
```
Explain what this is and why.

### Create Policy

```yaml
code: snippet
```
Explain what this is and why.

### Create Binding

```yaml
code: snippet
```
Explain what this is and why.




## Cluster User

### Create User

```yaml
code: snippet
```
Explain what this is and why.

### Create Policy

```yaml
code: snippet
```
Explain what this is and why.

### Create Binding

```yaml
code: snippet
```
Explain what this is and why.


## Testing

How to test each user's access.

### usr-blue

namespace: blue
- list pods
- update pods

namespace: green
- list pods
- update pods

namespace: all
- list pods
- update pods

### usr-green

namespace: blue
- list pods
- update pods

namespace: green
- list pods
- update pods

namespace: all
- list pods
- update pods

### usr-all

namespace: blue
- list pods
- update pods

namespace: green
- list pods
- update pods

namespace: all
- list pods
- update pods





## Note

This link helped me:

- [Kubernetes best practices: Organizing with Namespaces](https://cloud.google.com/blog/products/gcp/kubernetes-best-practices-organizing-with-namespaces)
