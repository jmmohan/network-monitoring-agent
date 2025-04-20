# Autonomous Network Management Agent

An intelligent system for automated network monitoring, anomaly detection, and resolution.

## Features

- Real-time system metrics monitoring (CPU, Memory, Network)
- Advanced statistical anomaly detection using z-scores
- Automated resolution of common network issues
- Configurable monitoring intervals and thresholds
- Comprehensive logging and trend analysis
- Support for multiple network interfaces

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
│   └── __init__.py
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- psutil for system metrics collection
- scikit-learn for statistical analysis
- loguru for advanced logging 