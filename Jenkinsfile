pipeline {
    agent any

    environment {
        OPENWEATHER_API_KEY = credentials('3aab362b4c66a414562d31fcdc08d614')
        MYSQL_USER = credentials('root')
        MYSQL_PASSWORD = credentials('292002')
        MYSQL_HOST = credentials('localhost')
        MYSQL_DATABASE = credentials('weather_db')
    }

    
    triggers {
        cron('H 1 * * *')  // 🔁 Triggers the job daily at 1 AM (H = hash for load balancing)
    }

    stages {
        stage('Setup Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Flask App') {
            steps {
                sh '''
                    source venv/bin/activate
                    export FLASK_APP=app.py
                    flask run --host=0.0.0.0 --port=5000
                '''
            }
        }
    }
}