# 00 - K8s Cluster Setup

Rough guide on creating a local k8s cluster on a mac.

Install several things before starting:
- virtualbox
- git
- docker
- kubernetes


I used this repo for setting up my cluster config:
https://github.com/ecomm-integration-ballerina/kubernetes-cluster

It will create a 3 node k8s cluster on virtualbox.

When this is created, add a port forwarding rule to the `k8s-head` vm to forward 2222 on your local machine to port 22 on the vm.

I use this `~/.ssh/config` to allow easy access:
```
Host k8
  HostName 127.0.0.1
  Port 2222
  User vagrant
  IdentityFile ~/.ssh/k-cluster
```


