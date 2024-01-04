from app.database.scripts import DataBaseRequests
from app.scripts.mails import MailSender

# Все ответы и отсюда будет обращение в скрипты БД


class Requests:
    def index(language: str | None = None) -> tuple:
        return DataBaseRequests.index(language)

    def builder(builder_id: int, language: str | None = None) -> tuple:
        return DataBaseRequests.builder(builder_id, language)

    def building(building_id: int, language: str | None = None) -> tuple:
        return DataBaseRequests.building(building_id, language)

    def flat(flat_id: int, language: str | None = None) -> tuple:
        return DataBaseRequests.flat(flat_id, language)

    def login(session, login: str, password: str) -> None:
        DataBaseRequests.login(session, login, password)

    def registrate(login: str, password: str) -> dict:
        return DataBaseRequests.registrate(login, password)

    class API:
        def change_language(new_lang: str,
                            prev_lang: str | None = None) -> dict:
            from dotenv import dotenv_values
            __LANGUAGES = dotenv_values('env/app.env')['LANGUAGES']
            if new_lang not in __LANGUAGES:
                return {
                    'state': 'False',
                    'info': f'UNSUPPORTED LANGUAGE. ONLY SUPPORT {__LANGUAGES}'}
            return {'state': 'True'}

        def connected():
            return DataBaseRequests.API.connected()

        def recreate_tables():
            return DataBaseRequests.API.recreate_tables()

        def delete_tables():
            return DataBaseRequests.API.delete_tables()

        def prepare():
            return DataBaseRequests.API.prepare()

        def update_tables_with_start_info():
            return DataBaseRequests.API.update_tables_with_start_info()

        def update_tables_with_file(
                table_name: str,
                file: str,
                file_path: str):
            return DataBaseRequests.API.update_tables_with_file(
                table_name, file, file_path)

        def operate_table_data(
                request,
                table_name: str,
                type_of_operation: str):
            return DataBaseRequests.API.operate_table_data(
                request, table_name, type_of_operation)

        def operate_table_data_filtered(
                request,
                table_name: str,
                type_of_operation: str):
            return DataBaseRequests.API.operate_table_data_filtered(
                request, table_name, type_of_operation)

        def operate_table_data_simpled(
                request,
                table_name: str,
                type_of_operation: str):
            return DataBaseRequests.API.operate_table_data_simpled(
                request, table_name, type_of_operation)

        def send_mail(request):
            __mail_sender = MailSender()
            # Временно:
            from configparser import ConfigParser
            __configs = ConfigParser()
            __configs.read('configs/mails.ini')

            # Requests.REDIS_WORKER.save_builder_request(request.json['destination']['builder_id'])

            # ---
            # В аргументах .send() у destination должно указываться письмо застройщика,
            # сформированное на основе request.json['destination']['builder_id'].
            # Возможно, хранить всю контактную информацию в БД, либо в конфигах
            return __mail_sender.send(
                __configs['SEND_GMAIL_1']['login'],
                __mail_sender.prepare_mail(
                    'SUBJECT_TEXT',
                    request.json['data']
                )
            )
