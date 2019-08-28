# Helm

The source for this can be found on my [github](https://github.com/mrmcshane/k8s-training/tree/master/05-helm).

Namespaces are a way to seperate your cluster into virtual clusters.

We will be deploying two modified versions of the stateful application, each in a different namespace.


## Structure

Your directory structure should look something like this:
```
04-namespaces
|-- containers
|   `-- python
|       |-- code
|       |   |-- requirements.txt
|       |   `-- test.py
|       `-- Dockerfile
|-- deployment-blue.yml
`-- deployment-green.yml
```
The deployment files for mariadb and python have been merged into the same config files, one for each namespace (blue/green).


## Python Application


Like in [03-stateful-application](https://github.com/mrmcshane/k8s-training/tree/master/03-stateful-application), we are testing connectivity with a simple database connection string. However this time, each python application in both namespaces will be configured with two connection strings:
```
host="mariadb-clusterip.blue"
host="mariadb-clusterip.green"
```
