import schedule
import time
from datetime import datetime
import os
import smtplib
from email.message import EmailMessage
import platform
import configparser

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Email parameters from the config file
email_address = config['EMAIL']['email_address']
email_password = config['EMAIL']['email_password']
smtp_server = config['EMAIL']['smtp_server']
smtp_port = int(config['EMAIL']['smtp_port'])

# Recipients from the config file
to_array = config['RECIPIENTS']['to_array'].split(',')

# Time for the cron job
cron_time = config['SETTINGS']['cron_time']

# Folders to check
folders_to_check = config['SETTINGS']['folders'].split(',')


def send_email(text, to):
    msg = EmailMessage()
    msg['Subject'] = "Cloud: Problem with Report Updates"
    msg['From'] = email_address
    msg['To'] = to
    msg.set_content(text)

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)


def creation_date(path_to_file):
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            return stat.st_mtime


def editing_date(file):
    datetime_str = time.ctime(os.path.getmtime(file))
    datetime_object = datetime.strptime(datetime_str, '%a %b %d %H:%M:%S %Y')
    return datetime_object


def cron_job():
    all_up_to_date = True
    for folder in folders_to_check:
        path = os.path.join("./data", folder)
        if os.path.exists(path):
            last_edited_time = editing_date(path)
            last_edited_date = last_edited_time.date()

            current_time = datetime.now()
            current_date = current_time.date()

            if current_date != last_edited_date:
                all_up_to_date = False
                for to in to_array:
                    send_email(f"Reports in folder '{folder}' were not updated!\nLast update: "
                               f"{str(last_edited_date)}\nToday's date: {str(current_date)}"
                               , to)

    if all_up_to_date:
        print("All folders are up to date")


cron_job()
schedule.every().day.at(cron_time).do(cron_job)
print("Service started")

while True:
    schedule.run_pending()
    time.sleep(1)
