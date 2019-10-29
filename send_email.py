# Специально для этой программы я создал почтовый ящик:
# логин - novikov.vladimir.yalyceum@yandex.ru
# пароль - passwordforyandex111
# сервер - yandex
# Там есть 1 непрочитанное письмо от Яндекс.Паспорта

# Вы также можете использовать свой логин и пароль

import email
import imaplib
import smtplib


def main():
    print('Чтобы начать пользоваться, Вы должны войти в свой аккаунт.')
    client = MailClient()
    client.help()
    while True:
        command = input('Введите команду: ').split()  # "разрезаем" команду, чтобы было удобнее
        if command[0].lower() == 'login':
            if len(command) != 4:  # проверяем все атрибуты команды
                print('Команда написана некорректно.')
                continue
            if command[3].lower() == 'yandex':  # корректируем сервер
                command[3] = 'imap.yandex.ru'
            elif command[3].lower() == 'mail':
                command[3] = 'imap.mail.ru'
            elif command[3].lower() == 'gmail':
                command[3] = 'imap.gmail.com'
            else:
                print('Сервер указан неверно. Повторите попытку.')
                continue

            client.auth(command[1], command[2], command[3])  # авторизируемся
        elif command[0].lower() == 'read':
            if len(command) != 2:  # проверяем все атрибуты команды
                print('Команда написана некорректно.')
                continue
            if client.login is not None:
                client.receive_mail(int(command[1]))
            else:
                print('Чтобы прочитать почту, вы должны войти в неё. '
                      'Используйте команду "help" для помощи.')
        elif command[0].lower() == 'send':
            if len(command) < 4:  # проверяем все атрибуты команды
                print('Команда написана некорректно.')
                continue
            if client.login is not None:
                client.send_mail(command[1], command[2], ' '.join(command[3:]))
            else:
                print('Чтобы отправить письмо, вы должны войти в почту. '
                      'Используйте команду "help" для помощи.')
        elif command[0].lower() == 'help':
            if len(command) != 1:  # проверяем все атрибуты команды
                print('Команда написана некорректно.')
                continue
            client.help()
        elif command[0].lower() == 'exit':
            if len(command) != 1:  # проверяем все атрибуты команды
                print('Команда написана некорректно.')
                continue
            print('Bye-Bye!')
            exit()
        else:
            print('Команда не распознана.')


class MailClient:

    def __init__(self):
        self.login = None
        self.password = None
        self.server = None

    def auth(self, login, password, server):
        """Вход в аккаунт почты"""
        try:
            mail = imaplib.IMAP4_SSL(server)
            mail.login(login, password)
        except mail.error:  # если ошибка - выводим
            print('Неверный логин или пароль. Повторите попытку.')
            return None
        self.SMTPserver = 'smtp.' + ".".join(server.split('.')[1:])
        self.login = login
        self.password = password
        self.server = server
        print('Успешно.')

    def receive_mail(self, num):
        """Прочитать num писем"""
        serverAdr = self.server
        mailAdr = self.login
        passwAdr = self.password

        def det_body(mag):  # получение тела письма
            if mag.is_multipart():
                return det_body(mag.get_payload(0))
            else:
                return mag.get_payload(None, True)

        con = imaplib.IMAP4_SSL(serverAdr)  # авторизация
        con.login(mailAdr, passwAdr)

        con.select('INBOX')  # выбераем входящие
        ids = list(reversed(str(con.search(None, 'ALL')[1])[3:-2].split()))
        # конвертируем список id сообщений

        print(f'Количество сообщений: {num}:')

        for i in range(num):  # выводим num писем

            print('Сообщение №%s\n______\n' % str(i + 1))

            # тело письма
            result, data = con.fetch(ids[i], '(RFC822)')
            ran = email.message_from_bytes(data[0][1])
            print(det_body(ran).decode("utf-8") + '\n\n\n\n\n\n')

        con.close()  # выходим из майла
        con.logout()

    def send_mail(self, toAdr, subject, body):
        """Отправить письмо"""
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        msg = MIMEMultipart()  # Создаём прототип сообщения
        msg['From'] = self.login
        msg['To'] = toAdr
        msg['Subject'] = subject

        body = body
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(self.SMTPserver, 587)  # отправляем
        server.starttls()
        server.login(self.login, self.password)
        text = msg.as_string()
        server.sendmail(self.login, toAdr, text)
        server.quit()
        print('Успешно.')

    def help(self):
        """Помощь по командам"""
        print('Вот некоторые команды, которые помогут вам работать в клиенте:')
        print('\n1) login <email> <password> <server> - авторизироваться')
        print('EMAIL - ваш полный email')
        print('PASSWORD - пароль от вашей почты')
        print('SERVER - yandex, mail, или gmail - остальные сервера не поддерживаются')
        print('\n2) read <num> - прочитать почту')
        print('NUM - число сообщений, которые вы хотите прочитать')
        print('\n3) send <toEMAIL> <subject> <body> - отправить сообщение')
        print('TOEMAIL - почтовый адрес того, кому отсылать сообщение')
        print('SUBJECT - тема письма')
        print('BODY - тело письма')
        print('\n4) help - помощь по командам')
        print('\n5) exit - выход')


if __name__ == '__main__':
    main()
