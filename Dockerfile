FROM python:3.11-slim

WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directory for configuration and copy default config
RUN mkdir -p /etc/xray-prometheus-exporter
COPY config.yml /etc/xray-prometheus-exporter/config.yml

# Expose the metrics port
EXPOSE 9099

# Run the application with unbuffered output for proper logging
ENTRYPOINT ["python", "-u", "main.py"]
CMD ["--config", "/etc/xray-prometheus-exporter/config.yml"]
