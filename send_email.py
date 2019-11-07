import imaplib
import smtplib


def send_email(name, acc_login, acc_password, toAdr):
    """
    Выполняет отправку сообщения о регистрации
    :param name: имя пользователя
    :param acc_login: хэндл пользователя
    :param acc_password: пароль пользователя
    :param toAdr: адрес электронной почты пользователя
    :return: None
    """
    login = 'yourmesseger@yandex.ru'
    password = 'passwordforyandex111'
    server = 'imap.yandex.ru'
    mail = imaplib.IMAP4_SSL(server)
    mail.login(login, password)
    SMTPserver = 'smtp.' + ".".join(server.split('.')[1:])

    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    msg = MIMEMultipart()  # Создаём прототип сообщения
    msg['From'] = login
    msg['To'] = toAdr
    msg['Subject'] = 'Регистрация в Messenger'

    body = f'''{name}, поздравляем!!!
Регистрция в Messenger прошла успешно.
Ваш логин: {acc_login}
Ваш пароль: {acc_password}'''
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(SMTPserver, 587)  # отправляем
    server.starttls()
    server.login(login, password)
    text = msg.as_string()
    server.sendmail(login, toAdr, text)
    server.quit()
