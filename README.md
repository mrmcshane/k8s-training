# Kubernetes Basics


## What is kubernetes

Kubernetes is an orchestration tool for container technologies, mainly docker.


## Why is Kubernetes used

Docker allows a process to run in an isolated container, bundled with its dependencies. However with docker, these containers need to be managed individually.

Kubernetes manages these containers at scale, assigning them to groups to manage their replication and availability. 


## Kubernetes Components

Here's a brief oiverview of the main components that make up a Kubernetes system, we will then go into a more detailed description of each component.

Here is an overview:

![overview](img/k8s_blue_overview.png "pods")

- A group of containers is called a **pod**. We always manage the pod, never the container.

- A a pod is created in the environment via a **deployment**. These are usually configured in a **replica set**, this determines how many copies of the pod will be deployed.

- A deployment is created in the **cluster**, or in larger environments a **namespace**, which is a virtual cluster.


### Clusters and Namespaces

A Kubernetes Cluster encompasses every component, from pods and deployments to nodes and networking. It's synonymous with your kubernetes environment.

A Namespace is a virtual cluster used for seperating different applications or application versions.


### Pods

Pods are the smallest component that Kubernetes manages.

![pods](img/k8s_blue_pod.png "pods")

These can be comprised of one or more containers, usually one.

You will usually find more containers in a pod if you have a custom logging or monitoring system.


### Deployments

![deployments](img/k8s_blue_deployment.png "deployments")

A deployment is how we manage groups of pods. 

Pods are usually configured as a template and assigned to a `Replica Set`, then the replica set is deployed using a deployment. 

This allows us to deploy multiple copies of a pod for high availability.


### Physical overview

This is the physical heirarchy of a kubernetes cluster.

![overview](img/k8s_overview_physical.png "overview")

Here we see how a deployment similar to the logical view fits into the physical world.

This cluster uses two nodes which aren’t shown on the logical diagram.

You can see two deployments of two pods. Kubernetes will attempt to schedule the pods in any given deployment on different nodes, this is to ensure that a failure in a node doesn’t result in a failure in the application. 


### Services

Services are how we assign networking to a pod.

![service labels](img/k8s_service.gif "service labels")

This is done by assigning a label to the pod in the format `key:value`: 
```yaml
template:
  metadata:
    labels:
      key: value
```

The service then attached itself to those pods by using a selector:
```yaml
spec:
  selector:
    key: value
```

There are several types of services that can be deployed the descriptions below are taken from the [Kubernetes Documentation](https://kubernetes.io/docs/concepts/services-networking/service/).
The diagrams are inspired by [this Medium post from Google](https://medium.com/google-cloud/kubernetes-nodeport-vs-loadbalancer-vs-ingress-when-should-i-use-what-922f010849e0).


#### ClusterIP

![ClusterIP](img/k8s_service_clusterip.png "ClusterIP")

Exposes the Service on a cluster-internal IP. Choosing this value makes the Service only reachable from within the cluster. This is the default ServiceType.


#### NodePort

![NodePort](img/k8s_service_nodeport.png "NodePort")

Exposes the Service on each Node’s IP at a static port (the NodePort). A ClusterIP Service, to which the NodePort Service routes, is automatically created. You’ll be able to contact the NodePort Service, from outside the cluster, by requesting <NodeIP>:<NodePort>.


#### LoadBalancer

![Loadbalancer](img/k8s_service_loadbalancer.png "Loadbalancer")

Exposes the Service externally using a cloud provider’s load balancer. NodePort and ClusterIP Services, to which the external load balancer routes, are automatically created.


#### Ingress

![Ingress](img/k8s_service_ingress.png "Ingress")

Ingress is the network entry point to your internal cluster network.

It contains routing rules to ensure network traffic is routed to the correct locations.

Public Cloud platforms will usually have their own Ingress controller that integrate effectively with their underlying infrastructure. Most Ingress controllers run nginx.


#### ExternalName

Maps the Service to the contents of the externalName field (e.g. foo.bar.example.com), by returning a CNAME record with its value. No proxying of any kind is set up.


## How is kubernetes used

Like most orchestration tools, a kubernetes deployment is defined in a number of manifests. These manifests describe the desired state of a kubernetes application.

These desired states are given to the control plane, which manages the cluster. The desired state of the cluster is applied with what's known as a **control loop**:

![control loop](img/control_loop.png "control loop")

This takes the desired state of the cluster and observes the current state, if there is a difference, it acts to apply the changes. Once the changes are applied it restarts the loop, observing the current state comparing it against the desired state, ensuring it's constantly staying up to date and that no configuration drift has occurred.


## kubectl

Command line tool for Kubernetes

This is what we will use to manage our cluster

For details or help with commands:

```
kubectl --help
kubectl --options
```

![kubectl help](img/kubectl_help.png "kubectl help")


### kubectl get

Display one or many resources

Commonly used for:

- pod(s)
- deployment(s)
- svc (services)

```
kubectl get [resource]
```

![kubectl get](img/kubectl_get.png "kubectl get")


### kubectl describe

Describes the details of a resource.

This is used to get more information than is presented by the get command.

```
kubectl describe [resource]
```

![kubectl describe](img/kubectl_describe.png "kubectl describe")


### kubectl apply

Apply a configuration to a resource

Usually done with the -f flag to specify a manifest file

```
kubectl apply -f [file.yml]
```

![kubectl apply](img/kubectl_apply.png "kubectl apply")


### kubectl delete

Delete resources by:

- file
- name
- selector

```
kubectl delete -f [file.yml]
```

![kubectl delete](img/kubectl_delete.png "kubectl delete")


### kubectl exec

Execute a command in a container

```
kubectl exec -it [pod] -- [command]
```

![kubectl exec](img/kubectl_exec.png "kubectl exec")


## Tasks

- [00 - k8s cluster setup](https://github.com/valtech-uk/kubernetes-training/tree/master/00-k8s-cluster-setup)
- [01 - simple application](https://github.com/valtech-uk/kubernetes-training/tree/master/01-simple-application)
- [02 - multi container pod](https://github.com/valtech-uk/kubernetes-training/tree/master/02-multi-container-pod)
- [03 - stateful application](https://github.com/valtech-uk/kubernetes-training/tree/master/03-stateful-application)
- [04 - namespaces](https://github.com/valtech-uk/kubernetes-training/tree/master/04-namespaces)
- [05 - helm template](https://github.com/valtech-uk/kubernetes-training/tree/master/05-helm-template)

