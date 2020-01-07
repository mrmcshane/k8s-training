# How this works in production

You now have a basic understanding of the kubernetes concepts and how to deploy simple applications using kubernetes, but how would this be applied in a production environment?

## Application Containers

Your microservice applications will likely be segregated into their own git repository. Each of those repositories will have a Dockerfile.

When anything is merged to `master`, your CI pipeline should build the new version of the application as a docker image and push to your registry with the `latest` tag.

## Kubernetes in Source Control

Rather than having everything in a single repository, it is useful to break some components of your deployment out into seperate repos in source control.

### Templates

Any templates used such as Helm charts should be seperated out so they can be updated in isolation of the application code and deployment config.

### Microservice Config

If you want the ability to deploy microservices independently, adding their kubernetes config a seperate repository will allow you to update individual repositories and allow your CI/CD pipeline to detect and publish individual changes to your deployment.

## Hosting

Rather than hosted o yoru local machine, the kubernetes cluster should be a multi-node cluster hosted either on-prem or as a managed service at AWS/Azure/GCP.

