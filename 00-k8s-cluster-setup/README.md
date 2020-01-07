# 00 - K8s Cluster Setup

Rough guide on creating a local k8s cluster on a mac.

- install virtualbox
  ```
  brew cask install virtualbox
  ```

- install git
  ```
  brew install git
  ```

- install kubectl
  ```
  https://kubernetes.io/docs/tasks/tools/install-kubectl/#install-kubectl-on-macos
  ```

- install helm
  ```
  brew install kubernetes-helm
  ```

- install minikube
  ```
  https://kubernetes.io/docs/tasks/tools/install-minikube/
  ```

- set up minikube
  ```
  minikube start
  ```

- get minikube ip (used for accessing applications deployed on this environment)
  ```
  minikube ip
  ```

- view minkube dashboard
  ```
  minikube dashboard
  ```
