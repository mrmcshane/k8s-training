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

The deployment config is similar to the previous task with two main additions; a shared volume, and how to apply the config map.
  

#### Shared Volume

We could have put a copy of the application code on both containers diretly, but that require a second 

The `php` image is built with the application code baked in. Once the container starts, the first task it performs will be to copy the application code to the shared volume, allowing access to the code form the `nginx` image.

First we create a blank volume under the deployment tamplate:
```
spec:
  volumes:
    - name: shared-files
      emptyDir: {}
```

Then we map the volume to each container:
```
- image: nginx:alpine
  name: nginx
  volumeMounts:
    - name: shared-files
      mountPath: /var/www/html
```

For the `php` container, we add an extra step to run a command to copy the app code over on startup:
```
- image: mrmcshane/php
  name: php
  volumeMounts:
    - name: shared-files
      mountPath: /var/www/html
  lifecycle:
    postStart:
      exec:
        command: ["/bin/sh", "-c", "cp -r /app/. /var/www/html"]
```

#### Apply Config Map

An additional volume is created containing the config map:

```
spec:
    volumes:
    - name: shared-files
        emptyDir: {}
    - name: nginx-config-volume
        configMap:
        name: nginx-config
```

To apply a config map as a file, we add an additional volume mount to the nginx container.

- **name:** Name of the volume the config map is assigned to.
- **mountPath:** Config file you wish to create.
- **subPath:** The key of your config within the configmap (as it can contain multiple keys).

```
- image: nginx:alpine
  name: nginx
  volumeMounts:
    - name: shared-files
      mountPath: /var/www/html
    - name: nginx-config-volume
      mountPath: /etc/nginx/nginx.conf
      subPath: nginx.conf
```

### Service

The service is pretty straightforward:
```
apiVersion: v1
kind: Service
metadata:
  name: php-nodeport
spec:
  type: NodePort
  ports:
    - port: 80
      targetPort: 80
      nodePort: 31111
  selector:
    component: php-label
```



## Deploy the application

Build custom php image
```
docker build containers/php -t mrmcshane/php
```

Push custom php image to dockerhub
```
docker push mrmcshane/php
```

Apply the deployment file:
```
kubectl apply -f php.yml
```
