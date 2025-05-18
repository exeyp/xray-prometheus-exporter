# XRay Prometheus Exporter - Technical Context

## Technologies

- **Python 3.11**
- **prometheus_client**: Prometheus metrics library
- **requests**: HTTP client
- **pyyaml**: YAML configuration
- **jsonpath-ng**: JSON parsing
- **Docker & Docker Compose**: Containerization

## Quick Start

```bash
# Local development
pip install -r requirements.txt
python main.py --config config.yml

# Docker Compose (recommended)
docker-compose up -d
```

## Dependencies

- prometheus_client >= 0.16.0
- pyyaml >= 6.0
- requests >= 2.28.2
- jsonpath-ng >= 1.5.0
