import time
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.network_agent import NetworkAgent
from src.anomaly_detector import AnomalyDetector
from loguru import logger

def main():
    # Initialize the network agent with the config path
    config_path = os.path.join(project_root, 'config', 'config.yaml')
    agent = NetworkAgent(config_path=config_path)
    
    # Initialize the anomaly detector
    detector = AnomalyDetector(
        window_size=agent.config['anomaly_detection']['window_size'],
        sensitivity=agent.config['anomaly_detection']['sensitivity']
    )
    
    logger.info("Starting Autonomous Network Management Agent")
    
    try:
        while True:
            # Collect metrics
            metrics = agent.collect_metrics()
            
            # Update anomaly detector history
            detector.update_history(metrics)
            
            # Detect anomalies using statistical methods
            anomalies = detector.detect_anomalies(metrics)
            
            # Log metrics and trends
            for metric in metrics:
                trend = detector.get_metric_trend(metric)
                stats = detector.get_metric_stats(metric)
                logger.info(
                    f"Metric: {metric}, "
                    f"Current: {metrics[metric]:.2f}, "
                    f"Trend: {trend}, "
                    f"Stats: {stats}"
                )
            
            # Handle anomalies
            for metric, current_value, threshold in anomalies:
                logger.warning(
                    f"Anomaly detected in {metric}: "
                    f"current={current_value:.2f}, "
                    f"threshold={threshold:.2f}"
                )
                
                if agent.config['automated_resolution']['enabled']:
                    resolution_success = agent.resolve_anomaly(f"{metric} anomaly")
                    if resolution_success:
                        logger.info(f"Successfully resolved {metric} anomaly")
                    else:
                        logger.warning(f"Failed to automatically resolve {metric} anomaly")
            
            # Sleep for configured interval
            time.sleep(agent.config['monitoring']['interval'])
            
    except KeyboardInterrupt:
        logger.info("Shutting down Network Agent")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise

if __name__ == "__main__":
    main() 