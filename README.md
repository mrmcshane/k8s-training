This is a basic repo to host the simple k8s projects I work on as I learn the technology.

It will contain the practical work from the notes created at: https://ns1.ovh/k8s/overview/

Current Projects:
- Simple Application
- Multi-Container Pod

## Simple Application

This is a very basic static html website added to the `nginx:alpine` image

## Multi-Container Pod

An example use case of when it's a good idea to have multiple containers in a pod, building on the `nginx:alpine` and `php` images. It's constructed in a way that we don't have to build a seperate nginx image as kubernetes applies a configMap to place the nginx config file in the right place for the default nginx container. 

The web content is placed on to the custom php image at build time, A shared volume is mapped to both containers and the content is copied over to the share at runtime so both containers have access.