# Autonomous Network Management Agent

An intelligent system for automated network monitoring, anomaly detection, and resolution.

## Features

- Real-time system metrics monitoring (CPU, Memory, Network)
- Advanced statistical anomaly detection using z-scores
- Automated resolution of common network issues
- Configurable monitoring intervals and thresholds
- Comprehensive logging and trend analysis
- Support for multiple network interfaces
- Extensive test coverage with pytest

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/network-monitoring-agent.git
cd network-monitoring-agent
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

The system can be configured through `config.yaml`. Key configuration options include:

- Monitoring intervals
- Metric thresholds
- Anomaly detection sensitivity
- Logging settings
- Automated resolution parameters

## Usage

Run the main script:
```bash
python src/main.py
```

The agent will:
- Monitor system metrics at configured intervals
- Detect anomalies using statistical methods
- Attempt to automatically resolve detected issues
- Log all activities and provide detailed metrics

## Testing

The project includes comprehensive unit tests and integration tests using pytest.

### Running Tests

Run all tests:
```bash
pytest
```

Run tests with coverage report:
```bash
pytest --cov=src --cov-report=term-missing
```

Run specific test categories:
```bash
pytest -m "not slow"  # Skip slow tests
pytest -m integration  # Run only integration tests
```

### Test Structure

- `tests/test_network_agent.py`: Tests for the main agent functionality
- `tests/test_anomaly_detector.py`: Tests for anomaly detection algorithms
- `tests/test_config.yaml`: Test configuration file

## Project Structure

```
network-monitoring-agent/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── network_agent.py
│   └── anomaly_detector.py
├── config/
│   └── config.yaml
├── tests/
│   ├── __init__.py
│   ├── test_network_agent.py
│   ├── test_anomaly_detector.py
│   └── test_config.yaml
├── requirements.txt
├── pytest.ini
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Commit your changes
6. Push to the branch
7. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- psutil for system metrics collection
- scikit-learn for statistical analysis
- loguru for advanced logging
- pytest for testing framework 