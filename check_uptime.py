import requests
import time
from datetime import datetime

# Configurable parameters
URL = 'https://www.wisecow.com'  # Replace with the application URL you want to monitor
CHECK_INTERVAL = 60  # Time interval (in seconds) between checks
LOG_FILE = 'uptime_log.txt'  # File where uptime status will be logged

# Function to check the status of the application
def check_application_status(url):
    try:
        response = requests.get(url, timeout=10)  # Set a timeout to avoid hanging forever
        if response.status_code == 200:
            return 'UP', response.status_code
        else:
            return 'DOWN', response.status_code
    except requests.exceptions.Timeout:
        return 'DOWN', 'Timeout'
    except requests.exceptions.RequestException as e:
        return 'DOWN', str(e)

# Function to log the status with timestamp
def log_status(status, status_code):
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(f'{datetime.now()} - Status: {status} - Code: {status_code}\n')

# Main function that checks uptime in intervals
def monitor_uptime():
    print(f"Monitoring the application uptime for: {URL}")
    while True:
        status, status_code = check_application_status(URL)
        print(f"Status: {status} - HTTP Code: {status_code}")
        log_status(status, status_code)
        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    monitor_uptime()
