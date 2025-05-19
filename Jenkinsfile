pipeline {
    agent any

    environment {
        OPENWEATHER_API_KEY = '3aab362b4c66a414562d31fcdc08d614'
        MYSQL_USER = 'root'
        MYSQL_PASSWORD = '292002'
        MYSQL_HOST = 'localhost'
        MYSQL_DATABASE = 'weather_db'
    }

    triggers {
        cron('H 1 * * *') // Runs daily at 1 AM
    }

    stages {
        stage('Clone Repo') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Script') {
            steps {
                bat """
                set OPENWEATHER_API_KEY=${OPENWEATHER_API_KEY}
                set MYSQL_USER=${MYSQL_USER}
                set MYSQL_PASSWORD=${MYSQL_PASSWORD}
                set MYSQL_HOST=${MYSQL_HOST}
                set MYSQL_DATABASE=${MYSQL_DATABASE}

                python app.py
                """
            }
        }
    }
}
