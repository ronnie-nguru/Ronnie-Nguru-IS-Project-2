# Use the official NGINX image
FROM nginx:latest

# Install dependencies and required build tools
RUN apt-get update && \
    apt-get install -y libmodsecurity3 libmodsecurity-dev wget git build-essential \
    libtool autoconf automake pkg-config && \
    git clone --depth 1 --branch v3/master https://github.com/SpiderLabs/ModSecurity /opt/ModSecurity && \
    cd /opt/ModSecurity && \
    git submodule init && \
    git submodule update && \
    ./build.sh && \
    ./configure && \
    make && \
    make install && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy over NGINX and ModSecurity configuration files
COPY nginx.conf /etc/nginx/nginx.conf
COPY modsecurity.conf /etc/nginx/modsecurity.conf

# Enable ModSecurity in NGINX
RUN echo 'Include /etc/nginx/modsecurity.conf' >> /etc/nginx/nginx.conf

# Expose ports
EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
