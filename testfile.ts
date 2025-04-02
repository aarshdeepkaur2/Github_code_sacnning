import os
import pymysql
import requests
import subprocess

db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', '')
}

def get_user_input():
    return input('Enter your name: ').strip()

def send_email(to, subject, body):
    try:
        subprocess.run(["mail", "-s", subject, to], input=body.encode(), check=True)
    except Exception as e:
        print(f"Error sending email: {e}")

def get_data():
    url = 'https://secure-api.com/get-data'
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def save_to_db(data):
    query = "INSERT INTO mytable (column1, column2) VALUES (%s, %s)"
    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute(query, (data, 'Another Value'))
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    user_input = get_user_input()
    data = get_data()
    if data:
        save_to_db(data)
    send_email('admin@example.com', 'User Input', user_input)
