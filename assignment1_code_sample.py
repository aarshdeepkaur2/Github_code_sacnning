import os
import logging
import pymysql
import smtplib
import ssl
from email.message import EmailMessage
import requests
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Securely fetch database credentials from environment variables
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "database": os.getenv("DB_NAME", "mydatabase"),
}


def get_user_input() -> str:
    """Prompt user for input and return the sanitized string."""
    return input("Enter your name: ").strip()


def send_email(to: str, subject: str, body: str) -> None:
    """Send an email securely using SMTP."""
    sender_email = os.getenv("EMAIL_SENDER", "no-reply@example.com")
    sender_password = os.getenv("EMAIL_PASSWORD", "")

    if not sender_password:
        logging.warning("Email password is not set. Skipping email.")
        return

    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.example.com", 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        logging.info("Email sent successfully.")
    except Exception as error:
        logging.error("Failed to send email: %s", error)


def get_data() -> Optional[str]:
    """Securely fetch data using HTTPS and handle exceptions."""
    url = "https://secure-api.com/get-data"  # Ensure HTTPS
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise HTTP errors if any
        return response.text
    except requests.RequestException as error:
        logging.error("Error fetching data: %s", error)
        return None


def save_to_db(data: str) -> None:
    """Securely save data using parameterized queries."""
    if not data:
        logging.warning("No data to save.")
        return

    query = "INSERT INTO mytable (column1, column2) VALUES (%s, %s)"
    values = (data, "Another Value")

    try:
        connection = pymysql.connect(**DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            cursor.execute(query, values)
        connection.commit()
        logging.info("Data saved to database successfully.")
    except pymysql.MySQLError as error:
        logging.error("Database error: %s", error)
    finally:
        if "connection" in locals():
            connection.close()


if __name__ == "__main__":
    user_input = get_user_input()
    data = get_data()
    save_to_db(data)
    send_email("admin@example.com", "User Input", f"User entered: {user_input}")
