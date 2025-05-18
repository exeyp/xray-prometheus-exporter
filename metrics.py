import json
import logging
from typing import Dict, Any, List, Optional

import requests
from prometheus_client.core import GaugeMetricFamily

logger = logging.getLogger(__name__)

class XRayMetricsCollector:
    """
    Custom collector for XRay metrics.
    Fetches metrics from the XRay JSON endpoint and converts them to Prometheus format.
    """
    def __init__(self, endpoint_url: str):
        self.endpoint_url = endpoint_url
        
    def _fetch_data(self) -> Optional[Dict[str, Any]]:
        """Fetch JSON data from the endpoint."""
        try:
            response = requests.get(self.endpoint_url, timeout=5)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching metrics from {self.endpoint_url}: {e}")
            return None
    
    def _extract_memstats(self, data: Dict[str, Any]) -> List[GaugeMetricFamily]:
        """Extract memory statistics metrics."""
        metrics = []
        
        try:
            memstats_data = data.get('memstats', {})
            
            # Create gauge metrics for each memstat
            alloc = GaugeMetricFamily(
                'xray_memstats_alloc',
                'Memory allocated and not yet freed',
                labels=[]
            )
            alloc.add_metric([], memstats_data.get('Alloc', 0))
            metrics.append(alloc)
            
            total_alloc = GaugeMetricFamily(
                'xray_memstats_totalalloc',
                'Total memory allocated (even if freed)',
                labels=[]
            )
            total_alloc.add_metric([], memstats_data.get('TotalAlloc', 0))
            metrics.append(total_alloc)
            
            sys = GaugeMetricFamily(
                'xray_memstats_sys',
                'Memory obtained from system',
                labels=[]
            )
            sys.add_metric([], memstats_data.get('Sys', 0))
            metrics.append(sys)
            
            mallocs = GaugeMetricFamily(
                'xray_memstats_mallocs',
                'Number of mallocs',
                labels=[]
            )
            mallocs.add_metric([], memstats_data.get('Mallocs', 0))
            metrics.append(mallocs)
            
            frees = GaugeMetricFamily(
                'xray_memstats_frees',
                'Number of frees',
                labels=[]
            )
            frees.add_metric([], memstats_data.get('Frees', 0))
            metrics.append(frees)
            
        except Exception as e:
            logger.error(f"Error extracting memstats: {e}")
        
        return metrics
    
    def _extract_observatory(self, data: Dict[str, Any]) -> List[GaugeMetricFamily]:
        """Extract observatory metrics."""
        metrics = []
        
        try:
            observatory_data = data.get('observatory', {})
            
            # Create delay metric
            delay_metric = GaugeMetricFamily(
                'xray_observatory_delay',
                'Observatory delay metrics',
                labels=['outbound_tag']
            )
            
            # Create alive metric
            alive_metric = GaugeMetricFamily(
                'xray_observatory_alive',
                'Observatory alive status',
                labels=['outbound_tag']
            )
            
            # Add metrics for each outbound tag
            for tag, values in observatory_data.items():
                delay_metric.add_metric([tag], values.get('delay', 0))
                alive_metric.add_metric([tag], 1 if values.get('alive', False) else 0)
            
            metrics.extend([delay_metric, alive_metric])
            
        except Exception as e:
            logger.error(f"Error extracting observatory metrics: {e}")
        
        return metrics
    
    def _extract_stats_inbound(self, data: Dict[str, Any]) -> List[GaugeMetricFamily]:
        """Extract inbound traffic statistics."""
        metrics = []
        
        try:
            inbound_stats = data.get('stats', {}).get('inbound', {})
            
            # Create downlink metric
            downlink_metric = GaugeMetricFamily(
                'xray_stats_inbound_downlink',
                'Inbound downlink traffic',
                labels=['source']
            )
            
            # Create uplink metric
            uplink_metric = GaugeMetricFamily(
                'xray_stats_inbound_uplink',
                'Inbound uplink traffic',
                labels=['source']
            )
            
            # Add metrics for each source
            for source, values in inbound_stats.items():
                downlink_metric.add_metric([source], values.get('downlink', 0))
                uplink_metric.add_metric([source], values.get('uplink', 0))
            
            metrics.extend([downlink_metric, uplink_metric])
            
        except Exception as e:
            logger.error(f"Error extracting inbound stats: {e}")
        
        return metrics
    
    def _extract_stats_outbound(self, data: Dict[str, Any]) -> List[GaugeMetricFamily]:
        """Extract outbound traffic statistics."""
        metrics = []
        
        try:
            outbound_stats = data.get('stats', {}).get('outbound', {})
            
            # Create downlink metric
            downlink_metric = GaugeMetricFamily(
                'xray_stats_outbound_downlink',
                'Outbound downlink traffic',
                labels=['source']
            )
            
            # Create uplink metric
            uplink_metric = GaugeMetricFamily(
                'xray_stats_outbound_uplink',
                'Outbound uplink traffic',
                labels=['source']
            )
            
            # Add metrics for each source
            for source, values in outbound_stats.items():
                downlink_metric.add_metric([source], values.get('downlink', 0))
                uplink_metric.add_metric([source], values.get('uplink', 0))
            
            metrics.extend([downlink_metric, uplink_metric])
            
        except Exception as e:
            logger.error(f"Error extracting outbound stats: {e}")
        
        return metrics
    
    def _extract_stats_user(self, data: Dict[str, Any]) -> List[GaugeMetricFamily]:
        """Extract user traffic statistics."""
        metrics = []
        
        try:
            user_stats = data.get('stats', {}).get('user', {})
            
            # Create downlink metric
            downlink_metric = GaugeMetricFamily(
                'xray_stats_user_downlink',
                'User downlink traffic',
                labels=['source']
            )
            
            # Create uplink metric
            uplink_metric = GaugeMetricFamily(
                'xray_stats_user_uplink',
                'User uplink traffic',
                labels=['source']
            )
            
            # Add metrics for each source
            for source, values in user_stats.items():
                downlink_metric.add_metric([source], values.get('downlink', 0))
                uplink_metric.add_metric([source], values.get('uplink', 0))
            
            metrics.extend([downlink_metric, uplink_metric])
            
        except Exception as e:
            logger.error(f"Error extracting user stats: {e}")
        
        return metrics
    
    def collect(self):
        """
        Collect metrics from the XRay endpoint.
        This method is called by the Prometheus client when a scrape occurs.
        """
        data = self._fetch_data()
        if not data:
            # Return empty metrics if we couldn't fetch data
            return []
        
        # Extract and yield all metrics
        metrics = []
        metrics.extend(self._extract_memstats(data))
        metrics.extend(self._extract_observatory(data))
        metrics.extend(self._extract_stats_inbound(data))
        metrics.extend(self._extract_stats_outbound(data))
        metrics.extend(self._extract_stats_user(data))
        
        for metric in metrics:
            yield metric
