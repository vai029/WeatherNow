from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import requests
import os
from dotenv import load_dotenv
import pymysql

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Weather data model
class WeatherData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# List of cities to track
CITIES = ['Mumbai', 'London', 'Delhi', 'Sydney', 'Paris']

def fetch_weather_data(city):
    """Fetch weather data from OpenWeatherMap API"""
    api_key = os.getenv('OPENWEATHER_API_KEY')
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if response.status_code == 200:
            return {
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description']
            }
    except Exception as e:
        print(f"Error fetching weather data for {city}: {str(e)}")
    return None

def update_weather_data():
    """Update weather data for all cities"""
    for city in CITIES:
        weather_data = fetch_weather_data(city)
        if weather_data:
            new_record = WeatherData(
                city=city,
                temperature=weather_data['temperature'],
                humidity=weather_data['humidity'],
                description=weather_data['description']
            )
            db.session.add(new_record)
    
    db.session.commit()

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html', cities=CITIES)

@app.route('/api/weather')
def get_weather():
    """API endpoint to get current weather data"""
    current_weather = {}
    for city in CITIES:
        latest_data = WeatherData.query.filter_by(city=city).order_by(WeatherData.timestamp.desc()).first()
        if latest_data:
            current_weather[city] = {
                'temperature': latest_data.temperature,
                'humidity': latest_data.humidity,
                'description': latest_data.description,
                'timestamp': latest_data.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
    return jsonify(current_weather)

@app.route('/api/history/<city>')
def get_history(city):
    """API endpoint to get historical weather data for a city"""
    if city not in CITIES:
        return jsonify({'error': 'City not found'}), 404
    
    # Get date filter from query parameters
    date_filter = request.args.get('date')
    
    query = WeatherData.query.filter_by(city=city)
    
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d')
            next_day = filter_date + timedelta(days=1)
            query = query.filter(
                WeatherData.timestamp >= filter_date,
                WeatherData.timestamp < next_day
            )
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    history = query.order_by(WeatherData.timestamp.desc()).limit(10).all()
    return jsonify([{
        'temperature': record.temperature,
        'humidity': record.humidity,
        'description': record.description,
        'timestamp': record.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for record in history])

@app.route('/api/dates')
def get_available_dates():
    """API endpoint to get all available dates in the database"""
    dates = db.session.query(
        db.func.date(WeatherData.timestamp)
    ).distinct().order_by(
        db.func.date(WeatherData.timestamp).desc()
    ).all()
    
    return jsonify([date[0].strftime('%Y-%m-%d') for date in dates])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Update weather data on startup
        update_weather_data()
    app.run(debug=True) 