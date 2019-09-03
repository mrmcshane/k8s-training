# Ingress

The source for this can be found on my [github](https://github.com/mrmcshane/k8s-training/tree/master/05-ingress).

An Ingress is essentially a layer 7 (application) loadbalancer, it allows external access to the cluster and the applications within.

**Note:** This is being configured on GKE on GCP, not a local cluster.

## Structure

We will be deploying multiple versions of the python/mariadb application, with access to each of them configured as seperate subdomains all accessed through the ingress service.
```
05-ingress
|-- containers
|   |-- blue-python
|   |   `-- ...
|   |-- green-python
|   |   `-- ...
|   `-- pink-python
|       `-- ...
|-- deployment-blue.yml
|-- deployment-green.yml
|-- deployment-pink.yml
`-- ingress.yml
```


## Python Application

The main difference in this application is the connection string in each of the applications only specifies its own database:
```
MySQLdb.connect(host="blue-mariadb-clusterip")
```

Three different versions of the container will be deployed as the css has been updated to differentiate each application.


## ingress.yml

To create an ingress resource, we need the following:
```
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: ingress-resource
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
    ingress.kubernetes.io/add-base-url: "true"
```

Then to specify the routing rules to access the backends:
```
spec:
  rules:
  - host: pink.domain.com
    http:
      paths:
      - backend:
          serviceName: pink-service
          servicePort: 80
  - host: blue.domain.com
    http:
      paths:
      - backend:
          serviceName: blue-service
          servicePort: 80
  - host: green.domain.com
    http:
      paths:
      - backend:
          serviceName: green-service
          servicePort: 80
```
 

## Deploying the application

It's a simple `apply` to deploy the applications:
```
kubectl apply -f deployment-blue.yml
kubectl apply -f deployment-green.yml
kubectl apply -f deployment-pink.yml
kubectl apply -f ingress.yml
```

Alternatively, to apply all manifest files within te directory:
```
kubectl apply -f .
```


## Testing

To test this is working, add dns records for your subdomains to point to the external IP of the ingress controller. Once the new DNS records have propogated, visit the URLs to test your application. 

Please note that DNS propogation can take up to 24 hours.