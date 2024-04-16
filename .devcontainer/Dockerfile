FROM python:latest

RUN apt update && apt upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt install -y sudo git gnupg locales \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8 \
    && echo "LANG=en_US.utf8" >> /etc/environment \
    && groupadd devgroup \
    && useradd -g devgroup -m -s /bin/bash dev \
    && echo "dev ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers \
    && rm -rf /var/lib/apt/lists/*

USER dev

WORKDIR /workspace