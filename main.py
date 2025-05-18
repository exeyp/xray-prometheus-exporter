import argparse
import logging
import os
import yaml
from prometheus_client import REGISTRY, make_wsgi_app
from wsgiref.simple_server import make_server
from metrics import XRayMetricsCollector

# Configure logging to stdout/stderr (Docker standard)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

def load_config(config_path):
    """Load configuration from YAML file."""
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Error loading config from {config_path}: {e}")
        return {
            'server': {'port': 9099, 'host': '0.0.0.0'},
            'metrics': {'endpoint': 'http://oblako.itisnotvpn.com:11111/debug/vars'},
            'logging': {'level': 'INFO'}
        }

def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(description='XRay Prometheus Exporter')
    parser.add_argument('--config', default='config.yml', help='Path to config file')
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Set logging level from config
    logging_level = config.get('logging', {}).get('level', 'INFO')
    logging.getLogger().setLevel(getattr(logging, logging_level))
    
    # Get server configuration
    host = config.get('server', {}).get('host', '0.0.0.0')
    port = int(config.get('server', {}).get('port', 9099))
    
    # Get metrics endpoint
    endpoint_url = config.get('metrics', {}).get('endpoint', 'http://oblako.itisnotvpn.com:11111/debug/vars')
    
    # Register metrics collector
    logger.info(f"Registering metrics collector for endpoint: {endpoint_url}")
    REGISTRY.register(XRayMetricsCollector(endpoint_url))
    
    # Create WSGI app
    app = make_wsgi_app()
    
    # Start HTTP server
    httpd = make_server(host, port, app)
    logger.info(f"Starting HTTP server on {host}:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")

if __name__ == "__main__":
    main()
