# 01 - Simple Application

A brief example of how to deploy a simple docker container with k8s.

The application we are deploying is a simple python website.

The custom image is then deployed as a single container pod with a number of replicas via a deployment and assigned a service.

## Structure

Create a directory structure like below, feel free to clone the repo to get the containers or even create your own:
```
01-simple-application
|-- containers
|   `-- web
|       |-- app
|       |   `-- ...
|       `-- Dockerfile
|-- web.yml
`-- README.md
```

## Application

We will build the application into a docker image, although this could be any image in a remote registry.

It's a simple python application to display a webpage on `http/80`.


## web.yml

### Deployment

There are two parts to this simple application, the `deployment` and the `service`.

Using docker, we deploy containers. This changes in k8s as we never deploy a container directly, but we deploy a pod. A pod is the smallest unit that can be deployed in k8s, a pod usually contains a single continer.

Our pods will be part of a `deployment` and specified in a `template`.

This is also where we specify the number of replicas of a pod that will be deployed as part of the deployment.

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      component: web-label
  template:
    metadata:
      labels:
        component: web-label
    spec:
      containers:
        - name: web-container
          image: mrmcshane/web
          ports:
            - containerPort: 80
```


### Service

A `service` assigns networking to a set of pods.

#### Service Types

We will be using `type: NodePort`, as it allows direct access to the service from outside the cluster.

##### Selectors

```
selector:
  component: web-label
```

`Selectors` are used to specify which pods traffic is routed to. These select the `labels` assigned to a pod.

#### Port Mapping

```
ports:
- port: 80
    targetPort: 80
    nodePort: 30001
```
Services also control the port mapping from outside the pod to inside the pod through 3 settings:

- **port:** access within the cluster
- **targetPort:** access within the pod
- **nodePort:** access from external


## Deploying the application

Build web image:
```
docker build containers/web -t mrmcshane/web
```

Push custom image to dockerhub:
```
docker push mrmcshane/web
```

Apply the deployment file:
```
kubectl apply -f web.yml
```
