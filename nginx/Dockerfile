# Use Ubuntu as base image
FROM ubuntu:20.04

# Prevent interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    bison \
    build-essential \
    ca-certificates \
    curl \
    dh-autoreconf \
    doxygen \
    flex \
    gawk \
    git \
    iputils-ping \
    libcurl4-gnutls-dev \
    libexpat1-dev \
    libgeoip-dev \
    liblmdb-dev \
    libpcre3-dev \
    libpcre++-dev \
    libssl-dev \
    libtool \
    libxml2 \
    libxml2-dev \
    libyajl-dev \
    locales \
    lua5.3-dev \
    pkg-config \
    wget \
    zlib1g-dev \
    zlibc \
    libxslt-dev \
    libgd-dev \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /opt

# Clone and build ModSecurity
RUN git clone --depth 1 https://github.com/SpiderLabs/ModSecurity && \
    cd ModSecurity && \
    git submodule init && \
    git submodule update && \
    ./build.sh && \
    ./configure && \
    make && \
    make install

# Clone ModSecurity-nginx connector
RUN git clone --depth 1 https://github.com/SpiderLabs/ModSecurity-nginx.git

# Get Nginx version and build ModSecurity module
RUN nginx_version=$(nginx -v 2>&1 | awk -F/ '{print $2}') && \
    wget http://nginx.org/download/nginx-${nginx_version}.tar.gz && \
    tar -xvzmf nginx-${nginx_version}.tar.gz && \
    cd nginx-${nginx_version} && \
    nginx -V 2>&1 | grep "configure arguments:" | cut -d " " -f2- | xargs ./configure --add-dynamic-module=../ModSecurity-nginx && \
    make modules

# Create necessary directories
RUN mkdir -p /etc/nginx/modules /etc/nginx/modsec

# Copy ModSecurity module
RUN cp /opt/nginx-$(nginx -v 2>&1 | awk -F/ '{print $2}')/objs/ngx_http_modsecurity_module.so /etc/nginx/modules/

# Setup OWASP CRS
RUN git clone https://github.com/coreruleset/coreruleset /usr/local/modsecurity-crs && \
    mv /usr/local/modsecurity-crs/crs-setup.conf.example /usr/local/modsecurity-crs/crs-setup.conf && \
    mv /usr/local/modsecurity-crs/rules/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf.example \
       /usr/local/modsecurity-crs/rules/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf

# Copy ModSecurity configuration files
RUN cp /opt/ModSecurity/unicode.mapping /etc/nginx/modsec/ && \
    cp /opt/ModSecurity/modsecurity.conf-recommended /etc/nginx/modsec/modsecurity.conf

# Create main.conf
RUN echo "Include /etc/nginx/modsec/modsecurity.conf\n\
Include /usr/local/modsecurity-crs/crs-setup.conf\n\
Include /usr/local/modsecurity-crs/rules/*.conf" > /etc/nginx/modsec/main.conf

# Configure ModSecurity
RUN sed -i 's/SecRuleEngine DetectionOnly/SecRuleEngine On/' /etc/nginx/modsec/modsecurity.conf

# Configure Nginx
COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]