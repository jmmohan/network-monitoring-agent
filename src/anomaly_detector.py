import numpy as np
from typing import Dict, List, Tuple
from loguru import logger

class AnomalyDetector:
    def __init__(self, window_size: int = 60, sensitivity: float = 1.5):
        """
        Initialize the anomaly detector.
        
        Args:
            window_size (int): Number of historical samples to consider
            sensitivity (float): Number of standard deviations for anomaly threshold
        """
        self.window_size = window_size
        self.sensitivity = sensitivity
        self.history: Dict[str, List[float]] = {}
        
    def update_history(self, metrics: Dict[str, float]):
        """
        Update the historical metrics data.
        
        Args:
            metrics (Dict[str, float]): Current metric values
        """
        for metric, value in metrics.items():
            if metric not in self.history:
                self.history[metric] = []
            self.history[metric].append(value)
            
            # Keep only the last window_size samples
            if len(self.history[metric]) > self.window_size:
                self.history[metric] = self.history[metric][-self.window_size:]
                
    def detect_anomalies(self, current_metrics: Dict[str, float]) -> List[Tuple[str, float, float]]:
        """
        Detect anomalies using statistical methods.
        
        Args:
            current_metrics (Dict[str, float]): Current metric values
            
        Returns:
            List[Tuple[str, float, float]]: List of (metric, current_value, threshold) tuples
        """
        anomalies = []
        
        for metric, current_value in current_metrics.items():
            if metric not in self.history or len(self.history[metric]) < self.window_size:
                continue
                
            history = np.array(self.history[metric])
            mean = np.mean(history)
            std = np.std(history)
            
            if std == 0:  # Avoid division by zero
                continue
                
            z_score = abs(current_value - mean) / std
            
            if z_score > self.sensitivity:
                threshold = mean + (self.sensitivity * std)
                anomalies.append((metric, current_value, threshold))
                logger.warning(
                    f"Anomaly detected in {metric}: "
                    f"current={current_value:.2f}, "
                    f"mean={mean:.2f}, "
                    f"std={std:.2f}, "
                    f"z-score={z_score:.2f}"
                )
                
        return anomalies
        
    def get_metric_trend(self, metric: str) -> str:
        """
        Analyze the trend of a specific metric.
        
        Args:
            metric (str): Metric name
            
        Returns:
            str: Trend description
        """
        if metric not in self.history or len(self.history[metric]) < 2:
            return "insufficient data"
            
        values = np.array(self.history[metric])
        slope = np.polyfit(range(len(values)), values, 1)[0]
        
        if slope > 0.1:
            return "increasing"
        elif slope < -0.1:
            return "decreasing"
        else:
            return "stable"
            
    def get_metric_stats(self, metric: str) -> Dict[str, float]:
        """
        Get statistical measures for a metric.
        
        Args:
            metric (str): Metric name
            
        Returns:
            Dict[str, float]: Statistical measures
        """
        if metric not in self.history or len(self.history[metric]) < 2:
            return {}
            
        values = np.array(self.history[metric])
        return {
            'mean': float(np.mean(values)),
            'std': float(np.std(values)),
            'min': float(np.min(values)),
            'max': float(np.max(values)),
            'percentile_95': float(np.percentile(values, 95))
        } 