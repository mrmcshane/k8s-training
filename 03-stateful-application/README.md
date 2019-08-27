# Stateful Application

The source for this can be found on my [github](https://github.com/mrmcshane/k8s-training/tree/master/03-stateful-application).

Containerization is designed as a stateless technology, however you can still deploy stateful applications such as databases, as long as you keep the stateful data on a seperate volume and take regular backups.

In this project we will be creating a basic python application that will connect to a mariadb database.
We are only using a single database instance as a database cluster will add more layers of complexity.


## Structure

Your directory structure should look something like this:
```
/
|-- containers
|   `-- python
|       |-- code
|       |   |-- requirements.txt
|       |   `-- test.py
|       `-- Dockerfile
|-- deployment-python.yml
`-- deployment-mariadb.yml
```

Both deployments have been seperated out into seperate files so you can update them independently of each other.

## Python Application

I won't paste all of the application code as the codeitself doesn't matter, if you want to use it, it's hosted [here](https://github.com/mrmcshane/k8s-training/blob/master/03-stateful-application/containers/python/code/test.py).

The main part of the application that matters is the database connection string:
```
host="mariadb-clusterip.default.svc.cluster.local"
```
This uses the internal DNS of the k8s cluster. Nothing needs to be configured as it's automatically created from the service assigned to the mariadb application.

k8s dns is in in the format:
```
service.namespace.svc.cluster.local
```
If you haven't specified a namespace (and I haven't), it's `default`.

## Python Deployment

This is a very simple deployment based on the default python image.
A new image is created to add our small program and deployed via k8s.

### Dockerfile

This is the basic docker config, it copies over the code, installs the python dependencies, and then runs the application.
```
FROM python:3

WORKDIR /usr/src/app

COPY code/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY code/test.py .
EXPOSE 80

CMD [ "python", "./test.py" ]
```

### Deployment

The most simple of deployments, it creates a single pod with a single container running the custom python image:
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: python
spec:
  replicas: 1
  selector:
    matchLabels:
      component: python-label
  template:
    metadata:
      labels:
        component: python-label
    spec:
      containers:
        - name: python
          image: mrmcshane/python
          ports:
          - containerPort: 80
```

### Service

Very simple service, mapping port `30005` externally to port `80` in the deployment:
```
apiVersion: v1
kind: Service
metadata:
  name: python-node-port
spec:
  type: NodePort
  ports:
    - port: 80
      targetPort: 80
      nodePort: 30005
  selector:
    component: python-label
```


## Mariadb Deployment

We will deploy the default mariadb image and configure it by passing it a ConfigMap.

### Config Map

This is how we will configure our default database.
```
apiVersion: v1
kind: ConfigMap
metadata:
  name: mariadb-config
  namespace: default
data:
  MYSQL_DATABASE: test_db
  MYSQL_USER: test_user
  MYSQL_PASSWORD: test_pass
  MYSQL_RANDOM_ROOT_PASSWORD: 'yes'
```
Note the single quotes around `'yes'`, this ensures it is read as a string correctly.

### Deployment

This deployment will create a volume and a single container with that volume assigned:
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mariadb
spec:
  replicas: 1
  selector:
    matchLabels:
      component: mariadb-label
  template:
    metadata:
      labels:
        component: mariadb-label
    spec:
      volumes:
        - name: mariadb-volume
          emptyDir: {}
      containers:
        - name: mariadb
          image: mariadb
          volumeMounts:
          - mountPath: "/var/lib/mysql"
            name: mariadb-volume
          envFrom:
          - configMapRef:
              name: mariadb-config
```

### Service

We will be using a ClusterIP service type rather than the NodePort service assigned to the python application. 

The ClusterIP is the most restrictive service, which is best for a database. Nothing outside the cluster will be given access:

```
apiVersion: v1
kind: Service
metadata:  
  name: mariadb-clusterip
spec:
  selector:    
    component: mariadb-label
  type: ClusterIP
  ports:  
  - name: mariadb
    port: 3306
    targetPort: 3306
    protocol: TCP
```

## Deploying the application

It's a simple `apply` to deploy the applications:
```
kubectl apply -f deployment-mariadb.yml
kubectl apply -f deployment-python.yml
```

## Deploying on GCP

First, we need to create a static IP so we can configure a DNS record to point to our loadbalancer:
```
gcloud compute addresses create [name] --region europe-north1
```

To get the external IP address, we can use:
```
gcloud compute addresses describe [name] --region europe-north1 --format='value(address)'
```

As we are deploying this on a cloud platform, replace the `NodePort` service in the `deployment-python.yml` config with a `Loadbalancer` service containing the Static IP:
```
apiVersion: v1
kind: Service
metadata:
  name: python-lb
spec:
  type: LoadBalancer
  loadBalancerIP: [Static IP]
  ports:
    - port: 80
      targetPort: 80
  selector:
    component: python-label
```

As before, it's a simple `apply` to deploy the applications:
```
kubectl apply -f deployment-mariadb.yml
kubectl apply -f deployment-python.yml
```


## Note

These links helped me:

- create a basic web application: [pythonspot](https://pythonspot.com/flask-web-app-with-python/)

- connecting python to mysql: [stackoverflow](https://stackoverflow.com/questions/51191563/connecting-python-and-mysql-in-docker-docker-compose)

- [Google Docs - Deploying a containerized web application](https://cloud.google.com/kubernetes-engine/docs/tutorials/hello-app)

- [Google Docs - Configuring Domain Names with Static IP Addresses](https://cloud.google.com/kubernetes-engine/docs/tutorials/configuring-domain-name-static-ip)

