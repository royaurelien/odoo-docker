FROM debian:bullseye-slim

SHELL ["/bin/bash", "-xo", "pipefail", "-c"]

# Generate locale C.UTF-8 for postgres and general locale data
ENV LANG C.UTF-8

# ARG BUILD_DEPS=" \
#     build-essential \
#     libfreetype6-dev \
#     libfribidi-dev \
#     libghc-zlib-dev \
#     libharfbuzz-dev \
#     libjpeg-dev \
#     liblcms2-dev \
#     libldap2-dev \
#     libopenjp2-7-dev \
#     libpq-dev \
#     libsasl2-dev \
#     libtiff5-dev \
#     libwebp-dev \
#     libxml2-dev \
#     libxslt-dev \
#     tcl-dev \
#     tk-dev \
#     zlib1g-dev"

ARG PYTHON_PACKAGES="\
    git+https://github.com/OCA/openupgradelib.git \
    git+https://github.com/apikcloud/git-aggregator.git \
    click-odoo-contrib \
    phonenumbers \
    ipython \
    pysnooper \
    ipdb \
    pg_activity \
    pysaml2 \
    geoip2"

# RUN apt-get update \
#     && apt-get install -yqq --no-install-recommends $BUILD_DEPS

# Install some deps, lessc and less-plugin-clean-css, and wkhtmltopdf
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        dirmngr \
        fonts-noto-cjk \
        gnupg \
        libssl-dev \
        node-less \
        npm \
        python3-magic \
        python3-num2words \
        python3-odf \
        python3-pdfminer \
        python3-pip \
        python3-phonenumbers \
        python3-pyldap \
        python3-qrcode \
        python3-renderpm \
        python3-setuptools \
        python3-slugify \
        python3-vobject \
        python3-watchdog \
        python3-xlrd \
        python3-xlwt \
        xz-utils \
        chromium \
        ffmpeg \
        fonts-liberation2 \
        gettext-base \
        git \
        gnupg2 \
        locales-all \
        nano \
        npm \
        wget \
        openssh-client \
        telnet \
        vim \
        zip \
        xmlsec1 \
        sudo \
        pip \
    && curl -o wkhtmltox.deb -sSL https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.buster_amd64.deb \
    && echo 'ea8277df4297afc507c61122f3c349af142f31e5 wkhtmltox.deb' | sha1sum -c - \
    && apt-get install -y --no-install-recommends ./wkhtmltox.deb \
    && rm -rf /var/lib/apt/lists/* wkhtmltox.deb

# install latest postgresql-client
RUN echo 'deb http://apt.postgresql.org/pub/repos/apt/ bullseye-pgdg main' > /etc/apt/sources.list.d/pgdg.list \
    && GNUPGHOME="$(mktemp -d)" \
    && export GNUPGHOME \
    && repokey='B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8' \
    && gpg --batch --keyserver keyserver.ubuntu.com --recv-keys "${repokey}" \
    && gpg --batch --armor --export "${repokey}" > /etc/apt/trusted.gpg.d/pgdg.gpg.asc \
    && gpgconf --kill all \
    && rm -rf "$GNUPGHOME" \
    && apt-get update  \
    && apt-get install --no-install-recommends -y postgresql-client \
    && rm -f /etc/apt/sources.list.d/pgdg.list \
    && rm -rf /var/lib/apt/lists/*

# Install rtlcss (on Debian buster)
RUN npm install -g rtlcss

# Install Python packages
RUN pip install --no-cache-dir $PYTHON_PACKAGES

# Create directory structure
ENV SOURCES=/home/odoo/src \
    CUSTOM=/home/odoo/custom \
    RESOURCES=/home/odoo/.resources \
    CONFIG_DIR=/home/odoo/.config \
    DATA_DIR=/home/odoo/data \
    PACKAGES_DIR=/home/odoo/packages
RUN mkdir -p $SOURCES/repositories && \
    mkdir -p $CUSTOM/repositories && \
    mkdir -p $DATA_DIR && \
    mkdir -p $CONFIG_DIR && \
    mkdir -p $RESOURCES && \
    mkdir -p $PACKAGES_DIR

# Config env
ENV OPENERP_SERVER=$CONFIG_DIR/odoo.conf
ENV ODOO_RC=$OPENERP_SERVER

# ODOO CONF DEFAULT VALUES
ARG UNACCENT=true
ARG PROXY_MODE=true
ARG WITHOUT_DEMO=true
ARG WAIT_PG=true
ARG PGUSER=odoo
ARG PGPASSWORD=odoo
ARG PGHOST=db
ARG PGPORT=5432
ARG ADMIN_PASSWORD=admin
# BUILD ARGS
ARG GITHUB_USER
ARG GITHUB_TOKEN
ENV ODOO_VERSION=saas-16.3
ARG ODOO_RELEASE=20230807
ARG ODOO_SOURCE=odoo/odoo
ARG ODOO_SOURCE_DEPTH=1
ARG INSTALL_ODOO=false
ARG INSTALL_ENTERPRISE=false
# Set env from args
ENV \
    UNACCENT="$UNACCENT" \
    PROXY_MODE="$PROXY_MODE" \
    WITHOUT_DEMO="$WITHOUT_DEMO" \
    WAIT_PG="$WAIT_PG" \
    PGUSER="$PGUSER" \
    PGPASSWORD="$PGPASSWORD" \
    PGHOST="$PGHOST" \
    PGPORT="$PGPORT" \
    ADMIN_PASSWORD="$ADMIN_PASSWORD" \
    ODOO_VERSION="$ODOO_VERSION"

# Metadata
ARG VCS_REF
ARG BUILD_DATE
ARG VERSION
LABEL org.label-schema.schema-version="$VERSION" \
      org.label-schema.vendor=Adhoc \
      org.label-schema.license=Apache-2.0 \
      org.label-schema.build-date="$BUILD_DATE" \
      org.label-schema.vcs-ref="$VCS_REF" \
      org.label-schema.vcs-url="https://github.com/ingadhoc/docker-odoo"

# ARG ODOO_SHA=648042fc38a4f0021ad180e1bccbbe77a5c80c2c
# RUN curl -o odoo.deb -sSL http://nightly.odoo.com/${ODOO_VERSION}/nightly/deb/odoo_${ODOO_VERSION}.${ODOO_RELEASE}_all.deb \
#     && echo "${ODOO_SHA} odoo.deb" | sha1sum -c - \
#     && apt-get update \
#     && apt-get -y install --no-install-recommends ./odoo.deb \
#     && rm -rf /var/lib/apt/lists/* odoo.deb

COPY deb/odoo.deb $PACKAGES_DIR/

RUN apt-get update \
    && apt-get -y install --no-install-recommends $PACKAGES_DIR/odoo.deb \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://$GITHUB_USER:$GITHUB_TOKEN@github.com/odoo/enterprise.git --single-branch --depth=1 --branch $ODOO_VERSION $SOURCES/enterprise

# Set permissions and Mount /var/lib/odoo to allow restoring filestore and /mnt/extra-addons for users addons
RUN chown odoo /etc/odoo/odoo.conf \
    && chown odoo /home/odoo -R

# Image building scripts
COPY bin/* /usr/local/bin/
COPY build.d $RESOURCES/build.d
COPY conf.d $RESOURCES/conf.d
COPY entrypoint.d $RESOURCES/entrypoint.d
COPY entrypoint.sh $RESOURCES/entrypoint.sh
RUN ln /usr/local/bin/direxec $RESOURCES/entrypoint \
    && ln /usr/local/bin/direxec $RESOURCES/build

# Copy entrypoint script and Odoo configuration file
# COPY ./entrypoint.sh /
# COPY ./odoo.conf /etc/odoo/

RUN chown -R odoo $RESOURCES \
    && chmod -R a+rx $RESOURCES/entrypoint* $RESOURCES/build* /usr/local/bin \
    && sync

# Expose Odoo services
EXPOSE 8069 8071 8072

# Set the default config file
ENV ODOO_RC /etc/odoo/odoo.conf

COPY wait-for-psql.py /usr/local/bin/wait-for-psql.py

VOLUME ["/home/odoo/data"]
WORKDIR "/home/odoo"

# Set default user when running the container
USER odoo

# ENTRYPOINT ["/entrypoint.sh"]
# CMD ["odoo"]

ENTRYPOINT ["/home/odoo/.resources/entrypoint.sh"]
CMD ["odoo"]
