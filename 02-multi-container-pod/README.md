# 02 - Multi Container Pod

This is an example of when it's useful to place two containers in the same pod.

The application is a simple PHP site. As it's PHP, it will require a frontend webserver and a php backend. These could be placed in one container, but that defeats the "one container one job" philosophy. Instead they will be seperate containers but within a single pod. 

A pod is meant to be the smallest unit of your application that can run independently. This is why with an application that requires both nginx/php, as neither of them can work independently of each other, you would add them both to a pod.



## Structure

Create a directory structure like below, feel free to clone the repo to get the containers or even create your own:
```
02-multi-container-pod
|-- containers
|   `-- php
|       |-- app
|       |   `-- ...
|       `-- Dockerfile
|-- php.yml
`-- README.md
```

## Application

### Config Map

Config Maps are a way of injecting configuration into a container.

This allows us to inject a custom configuration into an off the shelf nginx webserver image.

The main parts to this are:
```
kind: ConfigMap
apiVersion: v1
metadata:
  name: config-map-name
data:
  configfile.name: |
    config
    file
    contents
    here
```

Here is the full block with a basic `nginx.conf` to redirect php filetypes to port 9000:
```
kind: ConfigMap
apiVersion: v1
metadata:
  name: nginx-config
data:
  nginx.conf: |
    events {
    }
    http {
      server {
        listen 80 default_server;
        listen [::]:80 default_server;
        index index.php;
        
        root /var/www/html;
        server_name _;
        location / {
          try_files $uri $uri/ =404;
        }
        location ~ \.php$ {
          include fastcgi_params;
          fastcgi_param REQUEST_METHOD $request_method;
          fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
          fastcgi_pass 127.0.0.1:9000;
        }
      }
    }
```

### Deployment

__needs reviewing__

The general deployment config is much the same as a simple application, but with two differences:

- Shared Volume
- Apply config Map
  

#### Shared Volume



#### Apply Config Map

















## Deploy the application

Build custom php image
```
docker build containers/php -t mrmcshane/ip.ns1.ovh-php
```

Push custom php image to dockerhub
```
docker push mrmcshane/ip.ns1.ovh-php
```

Apply the deployment file:
```
kubectl apply -f deployment.yml
```
