# Scripts

This folder contains helper scripts for proto generation, image building, and Kubernetes deployment.

## Files

- [build.sh](build.sh): builds Docker images for all services
- [deploy.sh](deploy.sh): deploys Kubernetes resources
- [generate_proto.sh](generate_proto.sh): regenerates gRPC Python bindings

## Expected Usage

Build images:

```bash
./scripts/build.sh
```

Deploy to Kubernetes:

```bash
./scripts/deploy.sh
```

Regenerate protobuf bindings:

```bash
./scripts/generate_proto.sh
```

## Deployment Script Behavior

`deploy.sh` checks:

- `kubectl` is installed
- a Kubernetes context is active
- the API server is reachable

After that it applies the namespace manifest and then applies the kustomize bundle.
