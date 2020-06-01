#########################################################################
# This script can be executed for local deployment.
# This script must never be used on an environment exposed to the public,
# because instead of overwriting the secrets during the build process,
# it will use the defaults values we set in the values.yaml of the
# respective charts.
#########################################################################

# Set secrets to be used during deployment
# TODO: NECESSARY?
# export SCHEDULYTICS_CERT_MANAGER_SA=xxx      # Required for values yaml
# export MONGODB_ROOT_PW=gwrqgj4293fsdd
# export MONGODB_USER_PW=sdgl354053fdks

# Prepare helm
helm repo add jetstack https://charts.jetstack.io
helm repo add traefik https://containous.github.io/traefik-helm-chart
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add stable https://kubernetes-charts.storage.googleapis.com/

# Deploy Secrets
# TODO: Change Issuer for local since DNS will fail
# kubectl apply --filename=./cert-manager/secrets.yaml

# Deploy infrastructure
helm upgrade -i cert-manager --namespace cert-manager jetstack/cert-manager -f ./cert-manager/values.yaml --version v0.15.1
helm upgrade -i traefik --namespace default traefik/traefik -f ./traefik/values.yaml
helm upgrade -i mongodb --namespace default bitnami/mongodb -f ./mongodb/values.yaml
helm upgrade -i schedulytics-frontend --namespace default ./schedulytics-frontend -f ./schedulytics-frontend/values.yaml
helm upgrade -i schedulytics-grpc-server --namespace default ./schedulytics-grpc-server -f ./schedulytics-grpc-server/values.yaml
helm upgrade -i envoy --namespace default stable/envoy -f ./envoy/values.yaml

# Deploy CRDs
kubectl apply --filename=./cert-manager/certs.yaml
kubectl apply --filename=./traefik/routes.yaml