import pytest
from pathlib import Path
import psutil
from src.network_agent import NetworkAgent

@pytest.fixture
def test_config_path():
    return Path(__file__).parent / 'test_config.yaml'

@pytest.fixture
def network_agent(test_config_path):
    return NetworkAgent(config_path=str(test_config_path))

def test_load_config(network_agent):
    """Test configuration loading"""
    assert network_agent.config is not None
    assert 'monitoring' in network_agent.config
    assert 'metrics' in network_agent.config['monitoring']
    assert 'thresholds' in network_agent.config['monitoring']

def test_initialize_metrics(network_agent):
    """Test metrics initialization"""
    expected_metrics = network_agent.config['monitoring']['metrics']
    for metric in expected_metrics:
        assert metric in network_agent.metrics_history
        assert metric in network_agent.anomaly_thresholds

def test_collect_metrics(network_agent):
    """Test metrics collection"""
    metrics = network_agent.collect_metrics()
    assert isinstance(metrics, dict)
    assert all(metric in metrics for metric in network_agent.config['monitoring']['metrics'])
    assert all(isinstance(value, (int, float)) for value in metrics.values())

def test_detect_anomalies(network_agent):
    """Test anomaly detection"""
    # Test with values above threshold
    test_metrics = {
        'cpu': 90.0,  # Above threshold
        'memory': 50.0,  # Below threshold
        'network': 80.0  # Above threshold
    }
    anomalies = network_agent.detect_anomalies(test_metrics)
    assert len(anomalies) == 2
    assert any('cpu' in anomaly for anomaly in anomalies)
    assert any('network' in anomaly for anomaly in anomalies)

    # Test with values below threshold
    test_metrics = {
        'cpu': 50.0,
        'memory': 50.0,
        'network': 50.0
    }
    anomalies = network_agent.detect_anomalies(test_metrics)
    assert len(anomalies) == 0

@pytest.mark.parametrize("anomaly_type,expected_result", [
    ("cpu anomaly", True),
    ("memory anomaly", True),
    ("network anomaly", False),
    ("unknown anomaly", False)
])
def test_resolve_anomaly(network_agent, anomaly_type, expected_result):
    """Test anomaly resolution for different types"""
    result = network_agent.resolve_anomaly(anomaly_type)
    assert result == expected_result

def test_default_config():
    """Test default configuration when config file is not found"""
    non_existent_path = "non_existent_config.yaml"
    agent = NetworkAgent(config_path=non_existent_path)
    default_config = agent._get_default_config()
    
    assert agent.config == default_config
    assert 'monitoring' in agent.config
    assert 'logging' in agent.config

@pytest.mark.integration
def test_full_monitoring_cycle(network_agent):
    """Integration test for a full monitoring cycle"""
    # Collect metrics
    metrics = network_agent.collect_metrics()
    assert metrics
    
    # Check for anomalies
    anomalies = network_agent.detect_anomalies(metrics)
    
    # If there are anomalies, test resolution
    for anomaly in anomalies:
        resolution_result = network_agent.resolve_anomaly(anomaly)
        assert isinstance(resolution_result, bool) 