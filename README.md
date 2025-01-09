# Weatherly

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![OpenWeather](https://img.shields.io/badge/OpenWeather-API-orange)
![AWS](https://img.shields.io/badge/AWS-S3-yellow)

A Python application that fetches real-time weather data and 5-day forecasts for multiple cities using the OpenWeather API. The application visualizes current weather conditions and forecast data while automatically storing the information in AWS S3 buckets for historical tracking and analysis.

## Features

- **Real-time Weather Data**: Fetches current weather conditions including temperature, humidity, and weather descriptions
- **5-Day Forecast**: This is an added feature I Implemented that Provides detailed 5-day weather forecasts with daily high/low temperatures, humidity, and wind conditions
- **Multiple Cities**: Supports monitoring multiple cities simultaneously with option to add custom locations of your choice
- **AWS S3 Integration**: Automatically stores weather data in JSON format for historical tracking
- **Interactive CLI**: User-friendly command-line interface for adding custom cities
- **Data Persistence**: Maintains historical weather data in organized S3 bucket structure

## Project Structure
```
Weatherly-dashboard/
├── Src/
│   ├── __init__.py
│   └── weatherly_dashboard.py
├── forecast-data/
│   └── city-timestamp.json
├── README.md
├── requirements.txt
├── .env
└── support
```

## Prerequisites

- Python 3.6+
- OpenWeather API key (free tier)
- AWS account with S3 access
- Operating System: Windows, macOS, or Linux

## Setup & Configuration

### AWS Configuration
1. Create an AWS IAM user with S3 access:
   - Go to AWS IAM Console
   - Create new user with programmatic access
   - Attach `AmazonS3FullAccess` policy

2. Configure AWS credentials locally:
```bash
aws configure
# OR set environment variables
export AWS_ACCESS_KEY_ID="your_access_key"
export AWS_SECRET_ACCESS_KEY="your_secret_key"
export AWS_DEFAULT_REGION="your_region"
```

### OpenWeather API Setup
1. Sign up at [OpenWeather](https://openweathermap.org/api)
2. Generate an API key
3. Note: Free tier allows 60 calls/minute

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ChinonsoNwakudu/Weatherly.git

```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create `.env` and update with your credentials:
```
OPENWEATHER_API_KEY=your_api_key_here
AWS_BUCKET_NAME=your_bucket_name
REFRESH_INTERVAL=30
DEFAULT_CITIES=Lagos,New York,Doha
```

## Usage

Run the application:
```bash
python weatherly_dashboard.py
```

### Configuration Options

#### Environment Variables
- `OPENWEATHER_API_KEY`: Your OpenWeather API key
- `AWS_BUCKET_NAME`: S3 bucket name for data storage
- `REFRESH_INTERVAL`: Data refresh interval in minutes (default: 30)
- `DEFAULT_CITIES`: Comma-separated list of default cities to monitor

## Data Schema

### Weather Data JSON Format
```json
{
    "city": "New York",
    "timestamp": "2024-01-09T12:00:00Z",
    "temperature": 72.5,
    "feels_like": 75.2,
    "humidity": 65,
    "conditions": "partly cloudy",
    "wind_speed": 5.7
}
```

### Forecast Data JSON Format
```json
{
    "city": "New York",
    "generated_at": "2024-01-09T12:00:00Z",
    "forecast": [
        {
            "date": "2024-01-10",
            "high": 75.2,
            "low": 62.8,
            "humidity": 70,
            "wind_speed": 6.2,
            "conditions": "sunny"
        }
    ]
}
```

## Data Storage

Weather data is stored in AWS S3 with the following structure:
```
bucket_name/
├── weather-data/
│   └── city-timestamp.json
└── forecast-data/
    └── city-timestamp.json
```

## Troubleshooting

### Common Issues

1. API Connection Errors
   - Verify API key validity in `.env`
   - Check internet connection
   - Confirm you haven't exceeded rate limits (60 calls/minute)

2. AWS S3 Access Issues
   - Verify AWS credentials are configured correctly
   - Check bucket permissions and policies
   - Ensure IAM user has proper S3 access

3. Data Processing Errors
   - Validate city names are spelled correctly
   - Check JSON data format integrity
   - Verify storage paths exist

## Local Development

### Development Setup
1. Install development dependencies:
```bash
pip install -r requirements.txt
```

## Performance Considerations

- API rate limiting: Default refresh rate is 30 minutes
- Data storage: JSON files organized by date
- Memory usage: Batch processing for multiple cities
- Network requests: Implemented with timeout and retry logic



## Future Enhancements

- Web interface for data visualization
- Support for metric units
- Historical data analysis
- Weather alerts integration
- Custom data refresh intervals
- Additional weather metrics

