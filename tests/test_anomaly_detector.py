import pytest
import numpy as np
from src.anomaly_detector import AnomalyDetector

@pytest.fixture
def detector():
    return AnomalyDetector(window_size=10, sensitivity=2.0)

@pytest.fixture
def sample_metrics():
    return {
        'cpu': 50.0,
        'memory': 60.0,
        'network': 30.0
    }

def test_initialization(detector):
    """Test detector initialization"""
    assert detector.window_size == 10
    assert detector.sensitivity == 2.0
    assert isinstance(detector.history, dict)
    assert len(detector.history) == 0

def test_update_history(detector, sample_metrics):
    """Test history update mechanism"""
    # Update once
    detector.update_history(sample_metrics)
    for metric in sample_metrics:
        assert metric in detector.history
        assert len(detector.history[metric]) == 1
        assert detector.history[metric][0] == sample_metrics[metric]

    # Update multiple times and check window size
    for _ in range(15):  # More than window_size
        detector.update_history(sample_metrics)
    
    for metric in sample_metrics:
        assert len(detector.history[metric]) == detector.window_size

def test_detect_anomalies_normal_distribution(detector):
    """Test anomaly detection with normal distribution"""
    # Generate normal distribution data
    mean = 50
    std = 10
    normal_data = np.random.normal(mean, std, 20)
    
    # Add normal data to history
    for value in normal_data[:10]:
        detector.update_history({'test_metric': value})
    
    # Test with a value within normal range
    normal_value = {'test_metric': mean}
    anomalies = detector.detect_anomalies(normal_value)
    assert len(anomalies) == 0
    
    # Test with an anomalous value (4 standard deviations away)
    anomalous_value = {'test_metric': mean + (4 * std)}
    anomalies = detector.detect_anomalies(anomalous_value)
    assert len(anomalies) == 1

def test_get_metric_trend(detector):
    """Test trend analysis"""
    # Test increasing trend
    increasing_data = list(range(50, 60, 1))  # [50, 51, 52, ..., 59]
    for value in increasing_data:
        detector.update_history({'test_metric': float(value)})
    assert detector.get_metric_trend('test_metric') == 'increasing'
    
    # Test decreasing trend
    detector.history = {}  # Reset history
    decreasing_data = list(range(59, 49, -1))  # [59, 58, 57, ..., 50]
    for value in decreasing_data:
        detector.update_history({'test_metric': float(value)})
    assert detector.get_metric_trend('test_metric') == 'decreasing'
    
    # Test stable trend
    detector.history = {}  # Reset history
    stable_data = [50.0] * 5
    for value in stable_data:
        detector.update_history({'test_metric': value})
    assert detector.get_metric_trend('test_metric') == 'stable'

def test_get_metric_stats(detector, sample_metrics):
    """Test statistical measures calculation"""
    # Add some known data
    for _ in range(5):
        detector.update_history(sample_metrics)
    
    for metric in sample_metrics:
        stats = detector.get_metric_stats(metric)
        assert 'mean' in stats
        assert 'std' in stats
        assert 'min' in stats
        assert 'max' in stats
        assert 'percentile_95' in stats
        
        # Check if stats are correct
        assert stats['mean'] == sample_metrics[metric]
        assert stats['min'] == sample_metrics[metric]
        assert stats['max'] == sample_metrics[metric]

def test_empty_history_handling(detector):
    """Test handling of empty history"""
    # Test trend with empty history
    assert detector.get_metric_trend('non_existent') == 'insufficient data'
    
    # Test stats with empty history
    assert detector.get_metric_stats('non_existent') == {}
    
    # Test anomaly detection with empty history
    anomalies = detector.detect_anomalies({'test_metric': 50.0})
    assert len(anomalies) == 0

@pytest.mark.parametrize("test_data,expected_anomalies", [
    ([10, 10, 10, 10, 100], 1),  # One anomaly at the end
    ([10, 10, 10, 10, 10], 0),   # No anomalies
    ([10, 100, 10, 100, 10], 2), # Multiple anomalies
])
def test_various_anomaly_patterns(detector, test_data, expected_anomalies):
    """Test detection of various anomaly patterns"""
    # Add test data to history
    for value in test_data[:-1]:
        detector.update_history({'test_metric': float(value)})
    
    # Test last value for anomaly
    anomalies = detector.detect_anomalies({'test_metric': float(test_data[-1])})
    assert len(anomalies) == expected_anomalies 