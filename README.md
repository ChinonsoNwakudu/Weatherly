# Weatherly

A Python application that fetches real-time weather data and 5-day forecasts for multiple cities using the OpenWeather API. The application visualizes current weather conditions and forecast data while automatically storing the information in AWS S3 buckets for historical tracking and analysis.

## Features

- **Real-time Weather Data**: Fetches current weather conditions including temperature, humidity, and weather descriptions
- **5-Day Forecast**: Provides detailed 5-day weather forecasts with daily high/low temperatures, humidity, and wind conditions
- **Multiple Cities**: Supports monitoring multiple cities simultaneously with option to add custom locations
- **AWS S3 Integration**: Automatically stores weather data in JSON format for historical tracking
- **Interactive CLI**: User-friendly command-line interface for adding custom cities
- **Data Persistence**: Maintains historical weather data in organized S3 bucket structure

## Project structure
```

Weatherly-dashboard/
├── Src/
│   └── __init__.py
    └── weatherly_dashboard.py
└── data    
└── test
└── forecast-data/
    └── city-timestamp.json
└── README.md
└── requirements.txt

```
## Requirements

- Python 3.6+
- Boto3: AWS SDK for Python to interact with Amazon S3
- OpenWeather API key (free tier)
- AWS credentials with S3 access
- Required Python packages (see `requirements.txt`)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/weather-dashboard.git
cd weatherly-dashboard
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your credentials:
```
OPENWEATHER_API_KEY=your_api_key_here
AWS_BUCKET_NAME=your_bucket_name

```

## Usage

Run the application:
```bash
python weatherly_dashboard.py
```

The application will:
1. Create an S3 bucket if it doesn't exist
2. Display current weather for default cities (Lagos, New York, Doha)
3. Prompt for additional cities
4. Show current weather conditions including:
   - Temperature (°F)
   - Feels like temperature
   - Humidity percentage
   - Weather conditions
5. Display 5-day forecast with:
   - Daily high/low temperatures
   - Weather conditions
   - Humidity levels
   - Wind speeds
6. Save all data to S3 in JSON format

## Data Storage

Weather data is stored in the following S3 structure:
```
bucket_name/
├── weather-data/
│   └── city-timestamp.json
└── forecast-data/
    └── city-timestamp.json
```

## AWS S3 Requirements

The application requires:
- AWS credentials with S3 full access
- Permissions to create buckets (if bucket doesn't exist)
- Permissions to put objects in buckets

## Error Handling

The application includes comprehensive error handling for:
- API connection issues
- Invalid city names
- AWS credential/permission issues
- Data formatting problems

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenWeather API for weather data
- AWS for cloud storage capabilities
- Contributors who help improve the project

## Future Enhancements

- Web interface for data visualization
- Support for metric units
- Historical data analysis
- Weather alerts integration
- Custom data refresh intervals
- Additional weather metrics