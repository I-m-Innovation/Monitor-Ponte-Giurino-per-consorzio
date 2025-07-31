from ftplib import FTP
from .secrets import secrets

def FTPLogIn():

    secret_key = secrets.get('SECRET_KEY')
    IP1 = secrets.get('IP1')
    IP2 = secrets.get('IP2')
    db_user = secrets.get('DATABASE_USER', 'root')
    db_pass = secrets.get('DATABASE_PASSWORD', 'pass')

    try:
        ftp = FTP(IP1, timeout=120)
        # ftp = FTP("93.33.192.68", timeout=120)
    except:
        ftp = FTP(IP2, timeout=120)

    ftp.login(db_user, db_pass)

    return ftp