# XRay Prometheus Exporter - Product Context

## Purpose

Prometheus exporter for XRay metrics, enabling monitoring through Prometheus and Grafana.

## Problems Solved

- Converts Go expvar JSON format to Prometheus metrics format
- Integrates XRay metrics into Prometheus monitoring systems
- Provides visibility into memory usage, network performance, and traffic

## Goals

- Simple deployment via Docker Compose
- Reliable operation with robust error handling
- Low overhead with on-demand metric collection
- Standard Prometheus metric naming and labeling
