import smtplib
from email.message import EmailMessage

with open('weather.txt', 'r') as fp:
    msg = EmailMessage()
    msg.set_content(fp.read())
    
msg['Subject'] = f'Daily weather forecast'
msg['From'] = 'cnsmaster69@gmail.com'
msg['To'] = 'blackangelmusic22@gmail.com'

s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()