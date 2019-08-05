# 02 - Multi Container Pod

This is an example of when it's useful to place two containers in the same pod.

The application is a simple PHP site that returns your IP address. As it's PHP, it will require both nginx and php. These could be placed in one container, but that defeats the "one container one job" philosophy. Instead they will be seperate containers but within a single pod. 

A pod is meant to be the smallest unit of your application that can run independently. This is why with an application that requires both nginx/php, as neither of them can work independently of each other, you would add them both to a pod.


## Deployment

Build custom php image
```
docker build containers/php -t andrewmcshanevaltech/ip.ns1.ovh-php
```

Push custom php image to dockerhub
```
docker push andrewmcshanevaltech/ip.ns1.ovh-php
```

Apply the deployment file:
```
kubectl apply -f deployment.yml
```
