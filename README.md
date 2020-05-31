# schedulytics-environment
This repository acts as a baseline for the backend architecture that we setup. We use Helm Charts where possible and sometimes rely on simple Kubernetes configuration files. This repository is integrated with Google Cloud Build, which will deploy the relevant components to GKE.
A GKE cluster must already exist prior to the first deployment. It also needs a service account secret defined in the namespace cert-manager (which also must be manually created).
