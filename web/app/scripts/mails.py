import smtplib as smtp
from configparser import ConfigParser


class MailSender:
    def __init__(
        self,
        mail_type: str = 'gmail',
        ssl_tls: bool = True,
        another_sender: bool = False,
        login: str | None = None,
        password: str | None = None,
        sender_mail_type: str = 'CORPORATE'  # Добавлено на будущее, может пригодится
    ) -> None:
        """ Модуль, предназначенный для отправки писем

        По умолчанию использует указанную в конфигурациях почту и другие данные,
        однако при необходимости, эти данные можно изменить
        """
        self.settings = {
            'mail_type': mail_type,
            'ssl_tls': ssl_tls,
            'another_sender': another_sender,
            'login': login,
            'password': password,
        }
        self.__configs = self.__get_config_parser()

    def __get_config_parser(self) -> ConfigParser:
        """ Сохраняет путь в конфигурационному файлу и возвращает объект парсера """
        self.__path_to_config = 'configs/mails.ini'
        return ConfigParser()

    def __unprepare_mail(
            self,
            mail_message: str,
            __replacer: str = ' ') -> str:
        """ Принимает готовое письмо в формате текста (такой вариант письма возвращает self.prepare_mail) и преобразует его в однострочный текст """
        return mail_message.replace('\n', __replacer)

    def __BROKEN_NOW_get_mail_context(
            self,
            mail_message: str,
            __return_type: str = 'dict'):
        """ Принимает готовое письмо в виде текста и возвращает его контекст и указанном виде """
        from json import loads
        __return_data: any
        if __return_type == 'dict':
            __return_data = {}
            for key, value in loads(
                mail_message.replace(
                    ' - ', ': ').split('\n')):
                __return_data[key] = value
        return __return_data if __return_data else {}

    def prepare_mail(
            self,
            subject: str,
            context: str | dict | list,
            mail_type: str = 'TO_BUILDER') -> str:
        """ Принимает шапку письма и сырые данные и возвращает полный текст письма, сгенерированный на основе требуемого типа """
        prepared_mail = f'Subject:{subject}\n'
        if mail_type == 'TO_BUILDER':
            if isinstance(context, dict):
                for key, value in context.items():
                    prepared_mail += f'{key} - {value}\n'
            # Пока ничего не делаем:
            else:
                pass
        elif mail_type == 'TO_LOG':
            if isinstance(context, dict):
                for key, value in context.items():
                    prepared_mail += f'{key} - {value}'.replace('\n', '')
        return prepared_mail

    def send(self, destination: str, mail: str, logger: any = None) -> dict:
        """ Отправляет письмо

        Использует данные, указанные в конфигурациях, либо при инициализации класса
        """
        rules = {}
        if not self.settings['another_sender']:
            self.__configs.read(self.__path_to_config)
            rules['login'] = self.__configs['SEND_GMAIL_1']['login']
            rules['password'] = self.__configs['SEND_GMAIL_1']['password']
        else:
            rules['login'] = self.settings['login']
            rules['password'] = self.settings['password']
        if self.settings['mail_type'] == 'gmail':
            rules['server_host'] = self.__configs['SEND_GMAIL_1']['server_host']
            if self.settings['ssl_tls']:
                # Если все стоит без изменений, берем все данные из конфигов
                rules['server_port'] = self.__configs['SEND_GMAIL_1']['server_port']
                __server = smtp.SMTP(
                    rules['server_host'], rules['server_port'])
                __server.starttls()
                __server.login(rules['login'], rules['password'])
                # Вероятнее всего, если добавятся настройки снизу, то вынести
                # отправление письма в самый низ (после всех if-else):
                __server.sendmail(rules['login'], destination, mail)

                logger.info(
                    f'EMAIL WAS SUCCESSFULLY SENT TO {destination} WITH THE FOLLOWING CONTEXT: {self.__unprepare_mail(mail)}') if logger is not None else None
                return {'state': True}
            else:
                logger.info(
                    f'WHILE SENDING EMAIL WITH THE FOLLOWING CONTEXT: {self.__unprepare_mail(mail)} TO {destination} ERROR OCCURED --> ssl_tls is turned to False') if logger is not None else None
                return {'state': False}
        else:
            logger.info(
                f'WHILE SENDING EMAIL WITH THE FOLLOWING CONTEXT: {self.__unprepare_mail(mail)} TO {destination} ERROR OCCURED --> mail_type is not "gmail" and uknowned') if logger is not None else None
            return {'state': False}
