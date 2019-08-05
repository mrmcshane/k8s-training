# 01 - Simple Application

A brief example of how to deploy a simple docker container with k8s.
Using the `nginx:alpine` build, we add a static HTML site and create a custom image. 

The custom image is then deployed as a single container pod with a number of replicas via a deployment and assigned a service.

## Deployment

Build custom image
```
docker build containers/40k-map -t andrewmcshanevaltech/map.ns1.ovh
```

Push image to dockerhub
```
docker push andrewmcshanevaltech/map.ns1.ovh
```

Apply the deployment file:
```
kubectl apply -f deployment.yml
```
