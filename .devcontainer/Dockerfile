FROM mcr.microsoft.com/devcontainers/universal:2

# The Yarn apt repo key in the base image is stale and breaks `apt-get update`
# (NO_PUBKEY 62D54FD4003F6525), which fails every feature install.
RUN rm -f /etc/apt/sources.list.d/yarn.list \
    && sed -i '/dl.yarnpkg.com/d' /etc/apt/sources.list 2>/dev/null || true
