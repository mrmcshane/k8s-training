This is a basic repo to host the simple k8s projects I work on as I learn the technology.

It will contain the practical work from the notes created at: https://ns1.ovh/k8s/overview/ covering the following areas:

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


### 00 - k8s cluster setup

Using https://github.com/ecomm-integration-ballerina/kubernetes-cluster, we build a 3 node cluster using virtualbox.

### 01 - simple application

Deploy a static HTML website in a custom container.

### 02 - multi container pod

Deploy a PHP application, an example of how to deploy two very closely linked containers within the same pod (nginx/php).

### 03 - stateful application

Small python application that connects to a database.

Note - still needs work to make the database volume persistent.

### 04 - namespaces

Working with namespaces to segregate applications.

### 05 - helm

Helm is a way of templating kubernetes deployments, this allows us to cut down on the amount of duplicated code from the deployments in task 04 by creating the same application using helm templates.

### 0x - database cluster

How to deploy a fully scalable database cluster using k8s that supports automated recovery in the event of failure.

Note - This is going to be a bit harder, as it also needs to incorporate some kind of backup system in the event the whole thing goes down.

### 0x - ingress

Creating ingress points for your application.

### 0x - istio

Deploying istio into your environment.