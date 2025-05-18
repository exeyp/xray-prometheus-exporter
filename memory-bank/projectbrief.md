# XRay Prometheus Exporter - Project Brief

## Core Requirements

1. Python application exposing XRay metrics in Prometheus format
2. Fetch metrics from http://oblako.itisnotvpn.com:11111/debug/vars
3. HTTP server on port 9099 with /metrics endpoint
4. Docker container with Docker Compose support
5. Standard pip dependency management
6. YAML configuration

## Metrics

- **xray_memstats**: Memory statistics (alloc, totalalloc, sys, mallocs, frees)
- **xray_observatory**: Observatory metrics with outbound_tag labels
- **xray_stats_inbound/outbound/user**: Traffic statistics with source labels

## Key Constraints

1. On-demand metrics collection (only when /metrics is accessed)
2. Standard Docker logging to stdout/stderr
3. External YAML configuration
4. Host gateway access for container
