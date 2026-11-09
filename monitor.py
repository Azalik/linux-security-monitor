import os
import psutil
import psycopg2
from datetime import datetime

# Данные для подключения к нашей базе (мы создали их на предыдущем шаге)
DB_CONFIG = {
    "dbname": "sys_monitor",
    "user": "ilyas",
    "password": "secure_password123",
    "host": "localhost",
    "port": "5432"
}

def check_system_resources():
    # Получаем текущую загрузку CPU, RAM и диска в процентах
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    return cpu, ram, disk

def check_auth_logs():
    # Путь к системному логу неудачных входов в Linux
    log_path = "/var/log/auth.log"
    failed_attempts = []
    
    if os.path.exists(log_path):
        try:
            with open(log_path, "r") as f:
                lines = f.readlines()
                # Проверяем последние 50 строк на наличие попыток взлома
                for line in lines[-50:]:
                    if "Failed password" in line or "Invalid user" in line:
                        failed_attempts.append(line.strip())
        except PermissionError:
            pass
    return failed_attempts

def save_to_db(cpu, ram, disk, logs):
    # Подключаемся к базе данных PostgreSQL
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    # Сохраняем системные метрики
    cur.execute(
        "INSERT INTO system_metrics (cpu_usage, ram_usage, disk_usage) VALUES (%s, %s, %s);",
        (cpu, ram, disk)
    )
    
    # Сохраняем логи безопасности, если они есть
    for log in logs:
        cur.execute(
            "INSERT INTO security_logs (log_message) VALUES (%s);",
            (log,)
        )
        
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    cpu, ram, disk = check_system_resources()
    logs = check_auth_logs()
    save_to_db(cpu, ram, disk, logs)
    print(f"[{datetime.now()}] Успешно! CPU={cpu}%, RAM={ram}%, Disk={disk}%")
