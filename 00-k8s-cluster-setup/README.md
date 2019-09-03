# 00 - K8s Cluster Setup

Rough guide on creating a local k8s cluster on a mac.

Install several things before starting:

- virtualbox
  ```
  brew cask install virtualbox
  ```

- git
  ```
  brew install git
  ```

- docker
  ```
  brew install docker
  ```

- kubernetes
  ```
  brew install kubernetes
  ```

- vagrant
  ```
  brew cask install vagrant
  ```


I used this repo for setting up my cluster config:
https://github.com/ecomm-integration-ballerina/kubernetes-cluster

It will create a 3 node k8s cluster on virtualbox.

Instead of creating addidtional kubectl config files and configuring port forwarding to the vitrualbox VMs, we will be running all of the kubernetes commands in this example on the `k8s-head` instance. As this was configured with vagrant, this can be done by running:
```
vagrant ssh k8s-head
```

Once there, you can clone and enter the repo containing the tasks:
```
git clone https://github.com/mrmcshane/k8s-training.git
cd k8s-training
```
