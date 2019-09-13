# RBAC - Role Based Access Control

The source for this can be found on my [github](https://github.com/mrmcshane/k8s-training/tree/master/07-rbac).

Role Based Access Control (RBAC) is how we lock down access to resources/functionality in kubernetes. It can get reasonably complicated, but in this example, we will be creating one read/write user for each of the namespaces and one read-only user with access to the whole cluster.



## RBAC Overview

Go into a little detail how RBAC is configured with a couple of diagrams.



## Structure

Your directory structure should look something like this:
```
07-rbac
|-- deployment-blue.yml
|-- deployment-green.yml
|-- rbac-blue.yml
|-- rbac-green.yml
`-- rbac-cluster.yml
```
This builds on and uses the containers from [04-namespaces](https://github.com/mrmcshane/k8s-training/tree/master/04-namespaces), so build the containers from that task if you haven't already.

The RBAC manifests don't need to be in seperate files, but it's easier to structure it this way for the task.


## Pre-req - Create Users

We will need to create local users and kubernetes signed certs for these users.
This will be done with `create_k8s_user.sh` below:
```
#!/usr/bin/env bash

# get some env variables
user=$1
namespace=$2
cluster=$3

# create linux user and create home/cert directories
useradd ${user}
mkdir /home/${user}/
mkdir /home/${user}/.certs/
mkdir /home/${user}/.kube/

# generate certs and sign with kubernetes ca
openssl genrsa -out ${user}.key 2048
openssl req -new -key ${user}.key -out ${user}.csr -subj "/CN=${user}/O=07-rbac"
openssl x509 -req -in ${user}.csr -CA /etc/kubernetes/pki/ca.crt -CAkey /etc/kubernetes/pki/ca.key -CAcreateserial -out ${user}.crt -days 365

# copy certs to user dir
cp ${user}.* /home/${user}/.certs/

# create user config
rm -f /home/${user}/.kube/config
sudo cat /etc/kubernetes/admin.conf | head -n -12 >> /home/${user}/.kube/config
cat >> /home/${user}/.kube/config <<- EOM
- context:
    cluster: kubernetes
    namespace: ${namespace}
    user: ${user}
  name: ${user}@kubernetes
current-context: ${user}@kubernetes
kind: Config
preferences: {}
users:
- name: ${user}
  user:
    client-certificate-data: $(cat ${user}.crt | base64 -i | paste -sd "" -)
    client-key-data: $(cat ${user}.key | base64 -i | paste -sd "" -)
EOM

sudo chown -R $(id -u ${user}):$(id -g ${user}) /home/${user}/.kube/
```

This can be called with the command (ensure it's given a nice `chmod +x`):
```
sudo ./create_k8s_user.sh usr-blue blue kubernetes
```

The official method for doing this involves running several commands manually as the individual users, but this is more reproducable for the excersize.

The [Bitnami Docs](https://docs.bitnami.com/kubernetes/how-to/configure-rbac-in-your-kubernetes-cluster/) have a great example of how to perform these steps manually.

Once this has been run as the `vagrant` user, you can switch users `sudo su usr-blue` and run `kubectl get all` to see what you have access to.


## Namespace Users

We will be doing this for two users, `usr-blue` and `usr-green`. We will use `usr-blue` in this example.


### Create Policy

```yaml
kind: Role
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  namespace: blue
  name: blue-role
rules:
- apiGroups: 
  - ""
  - apps
  - extensions
  resources: 
  - deployments
  - pods
  - replicasets
  - services
  verbs:
  - get
  - list
  - watch
  - create
  - update
  - patch
  - delete
```
Permissions are specified by `Roles`, it determines the api groups, resources, and verbs that you are allowed to run. `Roles` are Namespace level controls.

### Create Binding

```yaml
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: blue-role-binding
  namespace: blue
subjects:
- kind: User
  name: usr-blue
  apiGroup: ""
roleRef:
  kind: Role
  name: blue-role
  apiGroup: ""
```
Once a policy is created, we assign it to a user with a `RoleBinding`. These are namespace level bindings that bind a role to a user or group.


## Cluster User

### Create Policy

```yaml
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: cluster-ro-role
rules:
- apiGroups: 
  - ""
  - apps
  - extensions
  resources: 
  - deployments
  - pods
  - replicasets
  - services
  verbs:
  - get
  - list
  - watch
```
A `ClusterRole` is as the name suggests, a role, but at the cluster level.

### Create Binding

```yaml
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: cluster-ro-role-clusterrolebinding
subjects:
- kind: User
  name: usr-cluster
  namespace: "*"
roleRef:
  kind: ClusterRole
  name: cluster-ro-role
  apiGroup: ""
```
Again with the ClusterRole, a `ClusterRoleBinding` is a binding but on a cluster level.


## Testing

### Namespace User

Switch user to `usr-blue`:
```
sudo sh usr-blue
```

To test the access that is given to a single namespace user, run:
```
kubectl get all
```

This will request all resources in your default namespace (blue):
```
NAME                          READY   STATUS    RESTARTS   AGE
pod/mariadb-7f86669b9-9htwk   1/1     Running   0          19h
pod/python-6844b4f794-gs7r7   1/1     Running   0          19h

NAME                        TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
service/mariadb-clusterip   ClusterIP      10.98.145.230    <none>        3306/TCP       19h
service/python-lb           LoadBalancer   10.101.140.132   <pending>     80:32221/TCP   10s

NAME                      READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/mariadb   1/1     1            1           19h
deployment.apps/python    1/1     1            1           19h

NAME                                DESIRED   CURRENT   READY   AGE
replicaset.apps/mariadb-7f86669b9   1         1         1       19h
replicaset.apps/python-6844b4f794   1         1         1       19h
Error from server (Forbidden): replicationcontrollers is forbidden: User "usr-blue" cannot list resource "replicationcontrollers" in API group "" in the namespace "blue"
Error from server (Forbidden): daemonsets.apps is forbidden: User "usr-blue" cannot list resource "daemonsets" in API group "apps" in the namespace "blue"
Error from server (Forbidden): statefulsets.apps is forbidden: User "usr-blue" cannot list resource "statefulsets" in API group "apps" in the namespace "blue"
Error from server (Forbidden): horizontalpodautoscalers.autoscaling is forbidden: User "usr-blue" cannot list resource "horizontalpodautoscalers" in API group "autoscaling" in the namespace "blue"
Error from server (Forbidden): jobs.batch is forbidden: User "usr-blue" cannot list resource "jobs" in API group "batch" in the namespace "blue"
Error from server (Forbidden): cronjobs.batch is forbidden: User "usr-blue" cannot list resource "cronjobs" in API group "batch" in the namespace "blue"
```

To check your cluster level permissions:
```
kubectl get all --all-namespaces
```

This user will have no permissions to see anything at the cluster level:
```
Error from server (Forbidden): pods is forbidden: User "usr-blue" cannot list resource "pods" in API group "" at the cluster scope
Error from server (Forbidden): replicationcontrollers is forbidden: User "usr-blue" cannot list resource "replicationcontrollers" in API group "" at the cluster scope
Error from server (Forbidden): services is forbidden: User "usr-blue" cannot list resource "services" in API group "" at the cluster scope
Error from server (Forbidden): daemonsets.apps is forbidden: User "usr-blue" cannot list resource "daemonsets" in API group "apps" at the cluster scope
Error from server (Forbidden): deployments.apps is forbidden: User "usr-blue" cannot list resource "deployments" in API group "apps" at the cluster scope
Error from server (Forbidden): replicasets.apps is forbidden: User "usr-blue" cannot list resource "replicasets" in API group "apps" at the cluster scope
Error from server (Forbidden): statefulsets.apps is forbidden: User "usr-blue" cannot list resource "statefulsets" in API group "apps" at the cluster scope
Error from server (Forbidden): horizontalpodautoscalers.autoscaling is forbidden: User "usr-blue" cannot list resource "horizontalpodautoscalers" in API group "autoscaling" at the cluster scope
Error from server (Forbidden): jobs.batch is forbidden: User "usr-blue" cannot list resource "jobs" in API group "batch" at the cluster scope
Error from server (Forbidden): cronjobs.batch is forbidden: User "usr-blue" cannot list resource "cronjobs" in API group "batch" at the cluster scope
```


### Cluster User

Switch user to `usr-cluster`:
```
sudo sh usr-cluster
```

Try and access the pod list:
```
kubectl get pod
```

As we have a cluster user created, it will not natively access other namespaces, so we will get the error:
```
No resources found.
```

If we append `--all-namespaces` to the command, we will see:
```
usr-cluster@k8s-head:/home/vagrant/k8$ kubectl get pod --all-namespaces
NAMESPACE     NAME                               READY   STATUS    RESTARTS   AGE
blue          mariadb-7f86669b9-9htwk            1/1     Running   0          20h
blue          python-6844b4f794-gs7r7            1/1     Running   0          20h
green         mariadb-7f86669b9-j4z4q            1/1     Running   0          29m
green         python-6844b4f794-kckhf            1/1     Running   0          29m
kube-system   calico-node-5ct8m                  2/2     Running   0          20h
kube-system   calico-node-f8pff                  2/2     Running   0          20h
kube-system   calico-node-hph89                  2/2     Running   0          21h
kube-system   coredns-5c98db65d4-qndmw           1/1     Running   0          21h
kube-system   coredns-5c98db65d4-stlsr           1/1     Running   0          21h
kube-system   etcd-k8s-head                      1/1     Running   0          21h
kube-system   kube-apiserver-k8s-head            1/1     Running   0          21h
kube-system   kube-controller-manager-k8s-head   1/1     Running   0          21h
kube-system   kube-proxy-88vwk                   1/1     Running   0          20h
kube-system   kube-proxy-lwmt5                   1/1     Running   0          20h
kube-system   kube-proxy-njb5q                   1/1     Running   0          21h
kube-system   kube-scheduler-k8s-head            1/1     Running   0          21h
```

To ensure the correct permissions have been applied in the role, we can try and delete one of the pods:
```
kubectl delete pod mariadb-7f86669b9-9htwk --namespace=blue
```

If the permissions have been set correctly, you should see this error:
```
Error from server (Forbidden): pods "mariadb-7f86669b9-9htwk" is forbidden: User "usr-cluster" cannot delete resource "pods" in API group "" in the namespace "blue"
```


## Note

These links helped me, and would be useful for further reading:

- [Bitnami Docs - Configure RBAC in your Kubernetes cluster](https://docs.bitnami.com/kubernetes/how-to/configure-rbac-in-your-kubernetes-cluster/)
