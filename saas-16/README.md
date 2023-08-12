## Build

```bash
    cat .env

    SAAS_PROVIDER_URL=xxx \
    SAAS_PROVIDER_TOKEN=xxx \
    ODOO_VERSION='saas-16.3' \
    DOCKER_REPO='apik/odoo-saas' \
    GITHUB_USER=xxx \
    GITHUB_TOKEN=xxx \
    GITLAB_USER=xxx \
    GITLAB_TOKEN=xxx

    docker build \
    --build-arg SAAS_PROVIDER_URL=${SAAS_PROVIDER_URL} \
    --build-arg SAAS_PROVIDER_TOKEN=${SAAS_PROVIDER_TOKEN} \
    --build-arg ODOO_VERSION=${ODOO_VERSION} \
    --build-arg DOCKER_REPO=${DOCKER_REPO} \
    --build-arg GITHUB_USER=${GITHUB_USER} \
    --build-arg GITHUB_TOKEN=${GITHUB_TOKEN} \
    --build-arg GITLAB_USER=${GITLAB_USER} \
    --build-arg GITLAB_TOKEN=${GITLAB_TOKEN} \
    --build-arg MINOR_VERSION=3 \
    --build-arg INSTALL_ODOO=true \
    --build-arg INSTALL_ENTERPRISE=true \
    --tag ${DOCKER_REPO}:${ODOO_VERSION} .

```

