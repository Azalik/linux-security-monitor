# Linux System & Security Monitor with PostgreSQL

A lightweight Python-based monitoring utility designed to track Linux system health (CPU, RAM, Disk usage) and parse system security logs (`auth.log`) for suspicious login attempts, securely storing all data in a PostgreSQL database.

## 🚀 Features
- **Resource Monitoring:** Tracks CPU, RAM, and Disk utilization using `psutil`.
- **Security Auditing:** Parses `/var/log/auth.log` to detect failed password attempts and unauthorized logins.
- **PostgreSQL Integration:** Automatically commits system metrics and security events into structured relational tables.
- **Automation:** Designed to run seamlessly via Linux `cron` scheduler.

## 🛠️ Tech Stack
- **Language:** Python 3
- **Database:** PostgreSQL
- **OS Automation:** Linux (Bash, Cron, systemd)
- **Libraries:** `psutil`, `psycopg2-binary`

## 📋 Database Schema Setup
Run the following SQL commands in your PostgreSQL console to set up the required database and tables:
sql
CREATE DATABASE sys_monitor;
CREATE USER ilyas WITH ENCRYPTED PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE sys_monitor TO ilyas;
\c sys_monitor;

   CREATE TABLE system_metrics (
       id SERIAL PRIMARY KEY,
       cpu_usage FLOAT,
       ram_usage FLOAT,
       disk_usage FLOAT,
       recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

   CREATE TABLE security_logs (
       id SERIAL PRIMARY KEY,
       log_message TEXT,
       recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

## ⚙️ Installation & Usage
1. Clone the repository:
bash
git clone https://github.com/Azalik/linux-security-monitor.git
cd linux-security-monitor

2. Create and activate a virtual environment:
bash
python3 -m venv venv
source venv/bin/activate

3. Install dependencies:
bash
pip install -r requirements.txt

4. Configure your database credentials inside `monitor.py` and run the script manually:
bash
python monitor.py


## 🔄 Automation (Cron)
To run the monitor automatically every 5 minutes, open your crontab:
bash
sudo crontab -e

Add the following line:
cron
*/5 * * * * /path/to/linux_monitor/venv/bin/python /path/to/linux_monitor/monitor.py


## 👤 Author
Created by Ilyas Gaitov (Information Security Student & Developer).
