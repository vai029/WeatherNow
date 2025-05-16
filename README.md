# WeatherNow - Weather Tracking Application

This application displays weather information for 5 cities and stores historical weather data in a MySQL database.

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a MySQL database named 'weather_db'

4. Create a .env file with the following variables:
```
OPENWEATHER_API_KEY=your_api_key_here
MYSQL_USER=your_mysql_username
MYSQL_PASSWORD=your_mysql_password
MYSQL_HOST=localhost
MYSQL_DATABASE=weather_db
```

5. Run the application:
```bash
python app.py
```

## Features
- Real-time weather data for 5 cities
- Historical weather data storage (10 days)
- Daily weather updates
- Temperature, humidity, and weather condition tracking

## Cities Tracked
- New York
- London
- Tokyo
- Sydney
- Paris 