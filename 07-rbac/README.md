# RBAC - Role Based Access Control

The source for this can be found on my [github](https://github.com/mrmcshane/k8s-training/tree/master/07-rbac).

Role Based Access Control (RBAC) is how we lock down access to resources/functionality in kubernetes. It can get reasonably complicated, but in this example, we will be creating one read/write user for each of the namespaces and one read-only user with access to the whole cluster.


## Structure

Your directory structure should look something like this:
```
07-rbac
|-- containers
|   `-- python
|       |-- code
|       |   |-- requirements.txt
|       |   `-- test.py
|       `-- Dockerfile
|-- deployment-blue.yml
|-- deployment-green.yml
|-- rbac-blue.yml
|-- rbac-green.yml
`-- rbac-cluster.yml
```
This builds on [04-namespaces](https://github.com/mrmcshane/k8s-training/tree/master/04-namespaces)



## Namespace Users

We will be doing this for two users, `usr-blue` and `usr-green`. We will use `usr-blue` in this example.

### Create User

```yaml
code: snippet
```
Explain what this is and why.

### Create Policy

```yaml
code: snippet
```
Explain what this is and why.

### Create Binding

```yaml
code: snippet
```
Explain what this is and why.




## Cluster User

### Create User

```yaml
code: snippet
```
Explain what this is and why.

### Create Policy

```yaml
code: snippet
```
Explain what this is and why.

### Create Binding

```yaml
code: snippet
```
Explain what this is and why.


## Testing

How to test each user's access.

### usr-blue

namespace: blue
- list pods
- update pods

namespace: green
- list pods
- update pods

namespace: all
- list pods
- update pods

### usr-green

namespace: blue
- list pods
- update pods

namespace: green
- list pods
- update pods

namespace: all
- list pods
- update pods

### usr-all

namespace: blue
- list pods
- update pods

namespace: green
- list pods
- update pods

namespace: all
- list pods
- update pods





## Note

This link helped me:

- [Kubernetes best practices: Organizing with Namespaces](https://cloud.google.com/blog/products/gcp/kubernetes-best-practices-organizing-with-namespaces)
