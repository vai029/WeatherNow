pipeline {
    agent any

    environment {
        OPENWEATHER_API_KEY = '3aab362b4c66a414562d31fcdc08d614'
        MYSQL_USER = 'root'
        MYSQL_PASSWORD = '292002'
        MYSQL_HOST = 'localhost'
        MYSQL_DATABASE = 'weather_db'
        PYTHON_PATH = 'C:\\Users\\KIIT\\AppData\\Local\\Programs\\Python\\Python38\\python.exe'
        PYTHON_VERSION = '3.9'
        VENV_NAME = 'venv'
        COLLECT_DATA_ONLY = 'true'
    }

    triggers {
        cron('H 1 * * *') // Runs daily at 1 AM
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                bat """
                    ${PYTHON_PATH} -m venv ${VENV_NAME}
                    call ${VENV_NAME}\\Scripts\\activate
                    pip install -r requirements.txt
                """
            }
        }

        stage('Collect Weather Data') {
            steps {
                bat """
                    call ${VENV_NAME}\\Scripts\\activate
                    python app.py
                """
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo 'Weather data collection completed successfully!'
        }
        failure {
            echo 'Weather data collection failed. Check logs for errors.'
        }
    }
}
