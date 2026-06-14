# Multi-Cloud Disaster Recovery Platform

This project is a local multi-cloud disaster recovery simulation built with Docker, Docker Compose, and Kubernetes.

The goal of this project is to understand how an application can continue running when the primary cloud environment becomes unavailable. The setup uses an AWS-style app as the primary service, an Azure-style app as the standby service, and a failover gateway that routes traffic based on health checks.

## What this project demonstrates

* Containerized application deployment
* Docker networking
* Docker Compose orchestration
* Kubernetes Deployments and Services
* Namespace-based resource organization
* Health-check based routing
* Failover from AWS to Azure
* Failback from Azure to AWS
* Service discovery inside Docker and Kubernetes

## Architecture

```text
User
 |
Failover Gateway
 |
 +-- AWS App
 |
 +-- Azure App
```

Normal flow:

```text
User → Gateway → AWS App
```

Failure flow:

```text
AWS App unavailable
User → Gateway → Azure App
```

Recovery flow:

```text
AWS App restored
User → Gateway → AWS App
```

## Application Endpoints

The application exposes three endpoints:

```text
/              → basic application response
/health        → health check endpoint
/cloud-status  → shows which cloud is serving traffic
```

Example response:

```json
{
  "cloud": "AWS",
  "status": "active"
}
```

## Tech Stack

* Python
* Flask
* Docker
* Docker Compose
* Kubernetes
* Docker Desktop Kubernetes
* PowerShell

## Local Docker Compose Setup

Start the full system:

```powershell
docker compose up --build
```

Access the failover gateway:

```text
http://localhost:8080
```

Expected response when AWS is healthy:

```json
{
  "response": {
    "cloud": "AWS",
    "status": "active"
  },
  "routed_to": "AWS"
}
```

To simulate AWS failure:

```powershell
docker compose stop aws-app
```

Refresh:

```text
http://localhost:8080
```

Expected response:

```json
{
  "response": {
    "cloud": "AZURE",
    "status": "active"
  },
  "routed_to": "AZURE"
}
```

To bring AWS back:

```powershell
docker compose start aws-app
```

The gateway routes traffic back to AWS.

## Kubernetes Setup

Create the namespace:

```powershell
kubectl apply -f kubernetes/namespace.yaml
```

Apply the Kubernetes resources:

```powershell
kubectl apply -f kubernetes/aws-app.yaml
kubectl apply -f kubernetes/azure-app.yaml
kubectl apply -f kubernetes/gateway.yaml
```

Verify pods:

```powershell
kubectl get pods -n multi-cloud-dr
```

Expected pods:

```text
aws-app              Running
azure-app            Running
failover-gateway     Running
```

Verify services:

```powershell
kubectl get svc -n multi-cloud-dr
```

Access the gateway using port-forward:

```powershell
kubectl port-forward svc/failover-gateway 8080:8080 -n multi-cloud-dr
```

Open:

```text
http://localhost:8080
```

## Kubernetes Failover Test

Scale AWS app down to zero:

```powershell
kubectl scale deployment/aws-app --replicas=0 -n multi-cloud-dr
```

Refresh:

```text
http://localhost:8080
```

The gateway should route traffic to Azure.

Bring AWS back:

```powershell
kubectl scale deployment/aws-app --replicas=1 -n multi-cloud-dr
```

The gateway should route traffic back to AWS.

## What I learned

Through this project, I practiced how disaster recovery works at a basic architecture level. I also learned how Docker Compose and Kubernetes handle networking, service discovery, health checks, and application recovery differently.

This project helped me understand why production systems use health checks, stable service names, container orchestration, and infrastructure definitions instead of relying on manual server-level setup.
