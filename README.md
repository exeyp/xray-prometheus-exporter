# XRay Prometheus Exporter

A Prometheus exporter for XRay metrics from a remote JSON endpoint.

## Quick Start

```bash
# Using Docker Compose (recommended)
docker-compose up -d

# Access metrics
curl http://localhost:9099/metrics
```

## Configuration

Default configuration file (`config.yml`):
```yaml
server:
  port: 9099
  host: "0.0.0.0"
metrics:
  endpoint: "http://oblako.itisnotvpn.com:11111/debug/vars"
logging:
  level: "INFO"
```

To use a custom configuration, uncomment the volumes section in `docker-compose.yml`:
```yaml
volumes:
  - ./custom-config.yml:/etc/xray-prometheus-exporter/config.yml
```

## Available Metrics

- `xray_memstats_*`: Memory statistics (alloc, totalalloc, sys, mallocs, frees)
- `xray_observatory_*`: Observatory metrics with outbound_tag labels
- `xray_stats_inbound_*`: Inbound traffic statistics
- `xray_stats_outbound_*`: Outbound traffic statistics
- `xray_stats_user_*`: User traffic statistics
