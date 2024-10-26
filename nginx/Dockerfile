FROM nginx:latest

# Install dependencies and ModSecurity
RUN apt-get update && \
    apt-get install -y libmodsecurity3 modsecurity && \
    apt-get clean

# Copy ModSecurity configuration files
COPY modsecurity.conf /etc/nginx/modsecurity/modsecurity.conf
COPY crs-setup.conf /etc/nginx/modsecurity/crs-setup.conf

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf
