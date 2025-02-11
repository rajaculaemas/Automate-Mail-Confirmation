import requests
import time
from datetime import datetime
import pytz
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Konfigurasi API
API_URL = "<Your API endpoint SOCRadar>"
API_KEY = "<Your SOCRadar API token/key>"

# Konfigurasi email
SENDER_EMAIL = "<sender mail addr"  # Ganti dengan email Outlook Anda
SENDER_PASSWORD = "<password>"        # Ganti dengan password Outlook Anda
RECIPIENT_EMAIL = "<recepient>"  # Email tujuan tetap

def get_static_dates():
    start_date = datetime(2024, 12, 29, tzinfo=pytz.utc)
    end_date = datetime(2024, 12, 30, tzinfo=pytz.utc)
    return start_date.strftime('%Y-%m-%dT%H:%M:%S'), end_date.strftime('%Y-%m-%dT%H:%M:%S')

def fetch_with_retries(url, params, retries=3, delay=5):
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Attempt {attempt + 1} failed with status code: {response.status_code}")
                time.sleep(delay)
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            time.sleep(delay)
    return None

def fetch_and_process_data():
    start_date, end_date = get_static_dates()
    params = {
        'key': API_KEY,
        'start_date': start_date,
        'end_date': end_date,
        'leak_type': 'employee'
    }
    print(f"Fetching data from {start_date} to {end_date}...")

    data = fetch_with_retries(API_URL, params)
    
    if data:
        for item in data.get("results", []):
            domain = item.get('domain')
            email = item.get('email')  # collect email for the report
            password = item.get('password')
            send_email(domain, email, password)

def send_email(domain, email, password):
    subject = "Konfirmasi Credential Leak"
    body = f"""
    Dear {email},  <!-- You can still include the email from API in the body if needed -->

    kami mendeteksi adanya compromissed credentials data dari akun anda dengan rincian sebagai berikut :
    Domain      : {domain}
    email       : {email}
    password    : {password}

    apabila detail kredensial diatas masih anda gunakan dan valid segera ganti password anda pada domain dan user tersebut dalam kesempatan pertama. konfirmasikan kepada kami jika anda sudah mengganti kredensial anda dengan cara menekan tombol konfirmasi dibawah ini.

    Terima kasih
    SOC247 Bot

    <a href="http://<your IP/DNS for handling confirmation>/confirm?email={email}">Saya sudah mengganti kredensial tersebut</a>
    """
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL  # Kirim email ke messigoatalien@gmail.com
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())  # Kirim ke alamat tetap
        server.quit()
        print(f"Email sent to {RECIPIENT_EMAIL}")
    except Exception as e:
        print(f"Error sending email: {e}")

# Main execution
fetch_and_process_data()
