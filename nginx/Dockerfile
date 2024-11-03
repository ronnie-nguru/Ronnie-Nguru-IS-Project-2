FROM nginx:latest

# Install dependencies and required build tools
RUN apt-get update && \
    apt-get install -y \
        libmodsecurity3 libmodsecurity-dev \
        wget git build-essential \
        libtool autoconf automake pkg-config \
        libpcre3 libpcre3-dev \
        libxml2 libxml2-dev \
        libcurl4-openssl-dev \
        uuid-dev zlib1g-dev \
        cmake && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Clone and build mbedTLS first
RUN cd /opt && \
    git clone -b 'mbedtls-2.28.2' --single-branch --depth 1 https://github.com/Mbed-TLS/mbedtls.git && \
    cd mbedtls && \
    cmake -DENABLE_TESTING=OFF . && \
    make && \
    make install && \
    cd .. && \
    rm -rf mbedtls

# Clone and build ModSecurity
RUN cd /opt && \
    git clone --depth 1 --branch v3/master https://github.com/SpiderLabs/ModSecurity && \
    cd ModSecurity && \
    git submodule init && \
    git submodule update --init --recursive --depth 1 && \
    ./build.sh && \
    ./configure && \
    make && \
    make install && \
    cd .. && \
    rm -rf ModSecurity

# Clone and install NGINX ModSecurity Connector
RUN cd /opt && \
    git clone --depth 1 https://github.com/SpiderLabs/ModSecurity-nginx.git

# Download and compile NGINX with ModSecurity support
RUN cd /opt && \
    wget http://nginx.org/download/nginx-1.21.6.tar.gz && \
    tar zxvf nginx-1.21.6.tar.gz && \
    cd nginx-1.21.6 && \
    ./configure --with-compat --add-dynamic-module=/opt/ModSecurity-nginx && \
    make modules && \
    cp objs/ngx_http_modsecurity_module.so /etc/nginx/modules && \
    cd .. && \
    rm -rf ModSecurity-nginx nginx-1.21.6*

# Copy configuration files
COPY nginx.conf /etc/nginx/nginx.conf
COPY modsecurity.conf /etc/nginx/modsecurity.conf

# Enable ModSecurity in NGINX
RUN echo 'load_module modules/ngx_http_modsecurity_module.so;' > /etc/nginx/modules-enabled/modsecurity.load

# Expose ports
EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]