import logging
from typing import Dict, List, Optional
import psutil
import numpy as np
from datetime import datetime
import yaml
from pathlib import Path
from loguru import logger

class NetworkAgent:
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize the Network Agent with configuration.
        
        Args:
            config_path (str): Path to the configuration file
        """
        self.config = self._load_config(config_path)
        self._setup_logging()
        self.metrics_history: Dict[str, List[float]] = {}
        self.anomaly_thresholds: Dict[str, float] = {}
        self._initialize_metrics()
        
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found, using defaults")
            return self._get_default_config()
            
    def _get_default_config(self) -> dict:
        """Return default configuration."""
        return {
            'monitoring': {
                'interval': 60,  # seconds
                'metrics': ['cpu', 'memory', 'network'],
                'thresholds': {
                    'cpu': 80.0,
                    'memory': 85.0,
                    'network': 70.0
                }
            },
            'logging': {
                'level': 'INFO',
                'file': 'network_agent.log'
            }
        }
        
    def _setup_logging(self):
        """Configure logging based on config."""
        logger.add(
            self.config['logging']['file'],
            level=self.config['logging']['level'],
            rotation="1 day",
            retention="7 days"
        )
        
    def _initialize_metrics(self):
        """Initialize metrics history and thresholds."""
        for metric in self.config['monitoring']['metrics']:
            self.metrics_history[metric] = []
            self.anomaly_thresholds[metric] = self.config['monitoring']['thresholds'][metric]
            
    def collect_metrics(self) -> Dict[str, float]:
        """
        Collect current system metrics.
        
        Returns:
            Dict[str, float]: Current metric values
        """
        metrics = {}
        
        if 'cpu' in self.config['monitoring']['metrics']:
            metrics['cpu'] = psutil.cpu_percent(interval=1)
            
        if 'memory' in self.config['monitoring']['metrics']:
            metrics['memory'] = psutil.virtual_memory().percent
            
        if 'network' in self.config['monitoring']['metrics']:
            net_io = psutil.net_io_counters()
            metrics['network'] = (net_io.bytes_sent + net_io.bytes_recv) / 1024 / 1024  # MB
            
        return metrics
        
    def detect_anomalies(self, metrics: Dict[str, float]) -> List[str]:
        """
        Detect anomalies in the collected metrics.
        
        Args:
            metrics (Dict[str, float]): Current metric values
            
        Returns:
            List[str]: List of detected anomalies
        """
        anomalies = []
        
        for metric, value in metrics.items():
            if value > self.anomaly_thresholds[metric]:
                anomalies.append(f"{metric} usage ({value}%) exceeds threshold ({self.anomaly_thresholds[metric]}%)")
                
        return anomalies
        
    def resolve_anomaly(self, anomaly: str) -> bool:
        """
        Attempt to automatically resolve detected anomalies.
        
        Args:
            anomaly (str): Description of the anomaly
            
        Returns:
            bool: True if resolution was attempted, False otherwise
        """
        if "cpu" in anomaly.lower():
            # Example: Kill high CPU processes
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                if proc.info['cpu_percent'] > 50:
                    try:
                        proc.kill()
                        logger.info(f"Killed high CPU process: {proc.info['name']}")
                    except:
                        pass
            return True
            
        elif "memory" in anomaly.lower():
            # Example: Clear memory cache
            if hasattr(psutil, 'linux_swap_memory'):
                psutil.linux_swap_memory().clear()
            return True
            
        elif "network" in anomaly.lower():
            # Example: Reset network interface
            # Note: This is a placeholder - actual implementation would depend on OS
            logger.warning("Network anomaly detected - manual intervention may be required")
            return False
            
        return False
        
    def run(self):
        """Main execution loop for the network agent."""
        logger.info("Starting Network Agent")
        
        while True:
            try:
                # Collect metrics
                metrics = self.collect_metrics()
                
                # Detect anomalies
                anomalies = self.detect_anomalies(metrics)
                
                # Log metrics and anomalies
                logger.info(f"Current metrics: {metrics}")
                if anomalies:
                    logger.warning(f"Detected anomalies: {anomalies}")
                    
                    # Attempt to resolve each anomaly
                    for anomaly in anomalies:
                        if self.resolve_anomaly(anomaly):
                            logger.info(f"Attempted to resolve: {anomaly}")
                        else:
                            logger.warning(f"Could not automatically resolve: {anomaly}")
                            
            except Exception as e:
                logger.error(f"Error in main loop: {str(e)}")
                
            # Sleep for configured interval
            time.sleep(self.config['monitoring']['interval']) 