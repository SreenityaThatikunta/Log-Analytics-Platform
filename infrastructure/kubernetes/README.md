# Kubernetes

This folder contains the Kubernetes deployment manifests for the platform.

## Resources

- [namespace.yaml](namespace.yaml): namespace creation
- [configmap.yaml](configmap.yaml): shared environment configuration
- [kustomization.yaml](kustomization.yaml): aggregate manifest entrypoint
- [ingress.yaml](ingress.yaml): frontend and API routing

Service-specific subfolders:

- `elasticsearch/`
- `log-collector/`
- `processor/`
- `query-service/`
- `frontend/`

## Deployment Model

- Elasticsearch runs as a StatefulSet with persistent storage
- app-tier services run as Deployments
- internal communication uses ClusterIP Services
- query-service and frontend are exposed through an ingress
- log-collector and query-service have HPAs

## Expected Namespace

All resources are deployed into:

- `log-analytics`

## Minikube Workflow

Build images into Minikube:

```bash
eval $(minikube docker-env)
./scripts/build.sh
```

Apply resources:

```bash
./scripts/deploy.sh
```

Verify:

```bash
kubectl get pods -n log-analytics
kubectl get svc -n log-analytics
kubectl get ingress -n log-analytics
kubectl get hpa -n log-analytics
kubectl top pods -n log-analytics
```

## Port-Forward Workflow

Collector:

```bash
kubectl port-forward svc/log-collector 50051:50051 -n log-analytics
```

Query service:

```bash
kubectl port-forward svc/query-service 8000:8000 -n log-analytics
```

Frontend:

```bash
kubectl port-forward svc/frontend 5173:80 -n log-analytics
```
