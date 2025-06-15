# Platform Engineering Self-Service Portal

A web-based self-service portal that allows developers to manage their development environments in Kubernetes. Built with Flask and Helm.

## Features

- Create development environments
- Check environment status
- Delete environments
- Automated secret management with Vault integration
- Kubernetes resource management
- Ingress configuration for applications

## Prerequisites

- Kubernetes cluster
- Helm
- Vault server
- Docker (for building/running the container)

## Installation

1. Clone the repository:
```sh
git clone [Platform Eng](https://github.com/ishimto/Platform-Engineering)
cd Platform-Engineering
```

2. Build and push the Docker image:
```sh
docker build -t your-registry/platform-eng:latest .
docker push your-registry/platform-eng:latest
```

3. Update the Helm values:
```yaml
# pod-platform/values.yaml
deployment:
  image: your-registry/platform-eng
  tag: latest
```

4. Deploy the platform service:
```sh
helm install platform-eng ./pod-platform
```

## Configuration

### Helm Values

The platform can be configured through Helm values in:
- `pod-platform/values.yaml` - Platform service configuration
- `charts/web_chart/values.yaml` - Application deployment configuration

Key configurations:
- Image repository and tag
- Service ports
- Ingress settings
- Vault configuration
- Secret management settings

## Usage

### Local Development

Run the Flask application locally:
```sh
python app.py
```

The service will be available at `http://localhost:5000`

### Docker

Build and run using Docker:
```sh
docker build -t platform-eng .
docker run -p 5000:5000 platform-eng
```

### Web Interface

Access the web interface and use the following features:

1. **Create Environment**
   - Enter username
   - Specify image tag
   - Creates namespace, copies secrets, and deploys application

2. **Check Status**
   - View deployed resources in your environment
   - Shows deployments, services ingresses, replicasets, and pods

3. **Delete Environment**
   - Remove all resources in your environment
   - Cleans up namespace and associated resources

## Architecture

- Flask web application
- Kubernetes backend
- Helm for deployment management
- External Secrets Operator for Vault integration
- Nginx Ingress for application access

## Security

- RBAC configuration for service account
- Namespace isolation for environments
- Vault integration for secret management
- Non-root container execution