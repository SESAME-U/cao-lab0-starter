FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm

# Stale Yarn apt key (NO_PUBKEY 62D54FD4003F6525) breaks `apt-get update` in every feature install.
RUN rm -f /etc/apt/sources.list.d/yarn.list \
    && sed -i '/dl.yarnpkg.com/d' /etc/apt/sources.list 2>/dev/null || true
