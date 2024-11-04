# SQL Injection Detection and Prevention using Web Application Firewalls and Object Relational Mappings

## Project Overview
This project focuses on **detecting and preventing SQL injection attacks** in web applications by combining the power of **Web Application Firewalls (WAFs)** and **Object-Relational Mappings (ORM)**. Leveraging **Nginx**, **Gunicorn**, **PostgreSQL**, and **ModSecurity**, we create a robust security layer to safeguard web applications against common SQL injection vulnerabilities. We also utilize **Graylog** for centralized logging and monitoring to detect anomalies and respond to threats in real-time.

### Key Components
- **Web Server**: Nginx
- **Application Server**: Gunicorn
- **Database**: PostgreSQL
- **Security Layers**:
  - **ModSecurity** for SQL injection prevention.
  - **SQLAlchemy** for ORM-based database interactions, helping sanitize inputs and prevent SQL attacks.
- **Logging & Monitoring**: Graylog for real-time log analysis.
- **Automation**: Bash scripts in `utility_scripts` folder for setup, configuration, and status monitoring.

### Testing Environment
We’ll use a mock bank application, **Bank Sphere**, to test and validate the effectiveness of WAFs and ORM against SQL injection attacks. This application simulates typical bank functionalities, including login and transaction features, providing a realistic testing scenario.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Architecture](#architecture)
- [Setup and Installation](#setup-and-installation)
- [Configuration Details](#configuration-details)
- [Testing with Bank Sphere](#testing-with-bank-sphere)
- [Logging and Monitoring](#logging-and-monitoring)
- [Contribution Guidelines](#contribution-guidelines)
- [License](#license)

---

## Features
- **SQL Injection Prevention**: Blocks SQL injection attempts using ModSecurity and ORM.
- **Real-Time Monitoring**: Graylog integration to capture, monitor, and analyze logs.
- **Automated Deployment**: Setup and configuration managed through bash scripts.
- **Scalable Architecture**: Supports deployment across multiple servers.

## Architecture

The architecture includes:
- **Front-End Web Server**: Nginx handles incoming traffic and forwards requests to Gunicorn.
- **Backend Application Server**: Gunicorn serves the application, using SQLAlchemy for secure database transactions.
- **Database Server**: PostgreSQL with hardened configurations.
- **Security Components**: ModSecurity as a WAF to inspect incoming traffic, block malicious requests, and log incidents.
- **Monitoring**: Graylog captures logs for security events and anomaly detection.

## Setup and Installation

### Prerequisites
- **Operating System**: Ubuntu 24 (configured in a WSL environment)
- **Web Server**: Nginx
- **Application Server**: Gunicorn
- **Database**: PostgreSQL
- **Firewall**: ModSecurity
- **Logging System**: Graylog

### Installation Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com//ronnie-nguru/Ronnie-Nguru-IS-Project-2.git
   
   ```

2. **Set Up the Environment**:
   - The `utility_scripts` folder contains all the necessary bash scripts to install dependencies, configure services, and check their statuses.
   - Run the following command to execute the setup script:
     ```bash
     ./utility_scripts/setup_environment.sh
     ```
   - This script installs and configures Nginx, PostgreSQL, Gunicorn, ModSecurity, and Graylog.

3. **Configure the Web Application Firewall (WAF)**:
   - Install and configure ModSecurity for Nginx:
     ```bash
     sudo apt install libapache2-mod-security2
     # Configure ModSecurity rules for SQL injection prevention
     ```

4. **Deploy the Bank Sphere Application**:
   - Bank Sphere serves as a testing ground for the implemented security layers.
   - Configure Bank Sphere on Gunicorn and ensure database transactions are handled by SQLAlchemy for ORM-based SQL injection prevention.

5. **Status Check**:
   - To check the status of all components, run:
     ```bash
     ./utility_scripts/check_status.sh
     ```
   - This script verifies that Nginx, Gunicorn, PostgreSQL, ModSecurity, and Graylog are running correctly and reports any issues.

## Configuration Details

- **Nginx**: Configured to forward requests to Gunicorn on specified ports.
- **ModSecurity Rules**: Custom SQL injection rules added in `modsecurity.conf`.
- **Database**: PostgreSQL with restricted privileges and sanitized SQL queries via SQLAlchemy.
- **Logging**: ModSecurity logs are configured to be sent to Graylog for real-time monitoring.

### IPtables Configuration
IPtables is set to allow secure connections to specified ports (e.g., 3306, 25, and 443) to secure database and web traffic.

---

## Testing with Bank Sphere

1. **Deploy Bank Sphere** on the server to simulate banking transactions.
2. **Simulate SQL Injection Attacks**: Attempt to perform SQL injection attacks on Bank Sphere’s login and transaction endpoints.
3. **Analyze WAF Responses**: ModSecurity should detect and block SQL injection attempts.
4. **Review ORM Effectiveness**: SQLAlchemy ORM should prevent any SQL injections from untrusted inputs by parameterizing queries.
5. **Monitor Logs in Graylog**: Check Graylog for real-time alerts and logs of the SQL injection attempts.

---

## Logging and Monitoring

- **Graylog Dashboard**: Provides a real-time view of logs and alerts, including ModSecurity events.
- **Log Analysis**: All server logs, including failed login attempts and blocked SQL injection attempts, are aggregated for easy monitoring.
- **Anomaly Detection**: Graylog helps identify unusual patterns, such as repeated SQL injection attempts, for further investigation.

---

## Contribution Guidelines
We welcome contributions! To contribute:
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request and provide a detailed description.

## License
This project is licensed under the MIT License. 
---
