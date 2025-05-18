# XRay Prometheus Exporter - System Patterns

## Architecture

```
Prometheus Server ◄── XRay Prometheus Exporter ◄── XRay JSON Endpoint
    (Scrapes)             (Transforms)                 (Provides)
```

## Key Technical Decisions

1. **On-Demand Collection**: Metrics fetched only when /metrics is accessed
2. **Custom Collector**: Uses Prometheus Python client's collector interface
3. **Metric Separation**: Each metric type handled by separate methods
4. **Error Isolation**: Errors in one metric don't affect others
5. **Docker Compose**: Single-stage build with host gateway access

## Components

- **Configuration**: YAML-based settings loader
- **Metrics Collector**: JSON fetching and transformation
- **HTTP Server**: Exposes metrics endpoint
- **Main Application**: Orchestration and error handling
