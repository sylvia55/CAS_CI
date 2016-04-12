import smtplib

def send_email(from_addr, password, to_addr):
    smtp = smtplib.SMTP('smtp.qq.com', 587)
    smtp.set_debuglevel(1)
    smtp.login(from_addr, password)
    msg = ("From: %s\r\nTo: %s\r\n\r\n"
       % (fromaddr, ", ".join(to_addr)))
    smtp.sendmail(from_addr, to_addr, msg)
    smtp.quit()
from_addr = 'wuwuyunhu@qq.com'
password = 'gmknynzycjuocajd'
to_addr = 'wuwuyunhu@qq.com'
send_email(from_addr, password, to_addr)