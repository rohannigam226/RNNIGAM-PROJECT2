import psutil
import time
import logging

# Configure logging to file and console
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("system_health.log"), 
                              logging.StreamHandler()])

# Define threshold values
CPU_THRESHOLD = 80  # percent
MEMORY_THRESHOLD = 20  # percent
DISK_THRESHOLD = 90  # percent

# Function to check CPU usage
def check_cpu_usage():
    cpu_percent = psutil.cpu_percent(interval=1)  # gets the CPU usage percentage
    if cpu_percent > CPU_THRESHOLD:
        logging.warning(f"High CPU usage: {cpu_percent}% (Threshold: {CPU_THRESHOLD}%)")
    else:
        logging.info(f"CPU usage is normal: {cpu_percent}%")

# Function to check memory usage
def check_memory_usage():
    memory = psutil.virtual_memory()
    if memory.percent > MEMORY_THRESHOLD:
        logging.warning(f"High memory usage: {memory.percent}% (Threshold: {MEMORY_THRESHOLD}%)")
    else:
        logging.info(f"Memory usage is normal: {memory.percent}%")

# Function to check disk usage
def check_disk_usage():
    disk = psutil.disk_usage('/')
    if disk.percent > DISK_THRESHOLD:
        logging.warning(f"High disk usage: {disk.percent}% (Threshold: {DISK_THRESHOLD}%)")
    else:
        logging.info(f"Disk usage is normal: {disk.percent}%")

# Function to check running processes
def check_running_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        processes.append(proc.info)

    # Print the top 5 resource-consuming processes
    sorted_processes = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:5]
    if sorted_processes:
        logging.info("Top 5 CPU consuming processes:")
        for proc in sorted_processes:
            logging.info(f"PID: {proc['pid']}, Name: {proc['name']}, CPU: {proc['cpu_percent']}%, Memory: {proc['memory_percent']}%")
    else:
        logging.info("No processes found.")

# Main function to monitor system health
def monitor_system_health():
    while True:
        check_cpu_usage()
        check_memory_usage()
        check_disk_usage()
        check_running_processes()
        
        # Wait for 60 seconds before checking again
        time.sleep(60)

if __name__ == "__main__":
    logging.info("Starting system health monitoring...")
    monitor_system_health()
