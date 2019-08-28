# Kubernetes Basics

**NOTE:** this is a work in progress


This is a basic repo to host the simple k8s projects I work on as I learn the technology.

It will contain the practical work from the notes created at: https://ns1.ovh/k8s/overview/.

## What is kubernetes

Kubernetes is an orchestration tool for container technologies, mainly docker.

## Why use Kubernetes

Docker allows a process to run in an isolated container, bundles with its dependencies. However with docker, these containers need to be managed individually.

Kubernetes manages these containers at scale, assigning them to orchestration groups to manage their replication and availability. With these orchestration groups in place, the groups of containers become highly available and fault tolerant.

## How is kubernetes used

Like most orchestration tools, kubernetes 

## Kubernetes overview

![overview](img/k8s_overview.png "overview")

### Pods

### Deployments

![deployments](img/k8s_deployment.png "deployments")

### Networking

#### Services



#### Ingress

Ingress is the network entrypoint to your internal cluster network.
It contains routing rules to ensure network traffic is routed to the correct locations.

![networking](img/k8s_networking.png "networking")

### Namespaces

A namespace is essentially a virtual cluster

## Tasks

- [00 - k8s cluster setup](https://github.com/mrmcshane/k8s-training/tree/master/00-k8s-cluster-setup)
- [01 - simple application](https://github.com/mrmcshane/k8s-training/tree/master/01-simple-application)
- [02 - multi container pod](https://github.com/mrmcshane/k8s-training/tree/master/02-multi-container-pod)
- [03 - stateful application](https://github.com/mrmcshane/k8s-training/tree/master/03-stateful-application)
- [04 - namespaces](https://github.com/mrmcshane/k8s-training/tree/master/04-namespaces)
- [05 - helm](https://github.com/mrmcshane/k8s-training/tree/master/05-helm)
- [0x - database cluster](https://github.com/mrmcshane/k8s-training/tree/master/0x-database-cluster)
- [0x - ingress](https://github.com/mrmcshane/k8s-training/tree/master/0x-ingress)
- [0x - istio](https://github.com/mrmcshane/k8s-training/tree/master/0x-istio)

This is not complete and will be changed/updated as I go.
The `0x` headers are for planned work, may or may not happen. 
