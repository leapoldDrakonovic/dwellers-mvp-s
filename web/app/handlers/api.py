from flask import Flask, request, jsonify, redirect, session, make_response, abort
from werkzeug.utils import secure_filename
from app.scripts.requests import Requests
from app.scripts.helpers import Playground
from app.data.rules import AuthenticationRule


def handle_api(application: Flask, logger):
    """ Обработка запросов API """

    @application.route('/login', methods=['POST'])
    def login():
        logger.info('/login')
        Requests.login(
            session,
            request.form['login'],
            request.form['password'])
        return redirect('/')

    @application.route('/logout', methods=['POST'])
    def logout():
        logger.info('/logout')
        session.pop('user', default=None)
        session.pop('user_role', default=None)
        return redirect('/')

    @application.route('/registrate', methods=['POST'])  # Отключить
    def registrate():
        login = request.args.get('login')
        password = request.args.get('password')
        if login is None or password is None:
            logger.info('/registrate -> error.html')
            abort(400)
        logger.info('/registrate')
        return jsonify(Requests.registrate(login, password))

    @application.route('/lang/update/<string:new_lang>', methods=['POST'])
    def change_language(new_lang: str):
        prev_lang = request.cookies.get('__lang')
        logger.info(f'/lang/update/{new_lang}')
        response = make_response(redirect(request.get_json()['fromUrl']))
        if new_lang == prev_lang:
            return response
        elif prev_lang is None:
            operation = Requests.API.change_language(new_lang)
            if operation['state'] == 'False':
                logger.info(
                    f'/lang/update/{new_lang} error -> {operation["info"]}')
                return response
        else:
            operation = Requests.API.change_language(new_lang, prev_lang)
            if operation['state'] == 'False':
                logger.info(
                    f'/lang/update/{new_lang} error -> {operation["info"]}')
                return response
            response.delete_cookie('__lang')
        response = Playground.cookie__set_safe(
            response,
            '__lang',
            new_lang,
            None,
            63115200,
            None,
            '/',
            None,
            True,
            True,
            'Strict')
        return response

    @application.route('/db/tables/create', methods=['GET'])
    def db_tables_create():
        logger.info('/db/tables/create')
        if AuthenticationRule.check_rule():
            return jsonify(Requests.API.prepare())
        abort(403)

    @application.route('/db/tables/delete', methods=['GET'])
    def db_tables_delete():
        logger.info('/db/tables/delete')
        if AuthenticationRule.check_rule():
            return jsonify(Requests.API.delete_tables())
        abort(403)

    @application.route('/db/tables/recreate', methods=['GET'])
    def db_tables_recreate():
        logger.info('/db/tables/recreate')
        if AuthenticationRule.check_rule():
            return jsonify(Requests.API.recreate_tables())
        abort(403)

    @application.route('/db/tables/update/start_info', methods=['GET'])
    def db_tables_update_start_info__DEPRECATED():
        logger.info('/db/tables/update/start_info')
        if AuthenticationRule.check_rule():
            return jsonify(Requests.API.update_tables_with_start_info())
        abort(403)

    @application.route('/db/tables/update/with_file', methods=['POST'])
    def db_tables_update_with_file():
        logger.info('/db/tables/update/start_info')
        if AuthenticationRule.check_rule():
            if 'data_file' not in request.files:
                return redirect(request.url)
            file = request.files['data_file']
            if file.filename == '':
                return redirect(request.url)
            if file and file.filename.rsplit('.', 1)[1].lower() == 'csv':
                secure_filename(file.filename)
                file.save('/tmp/csv_file.csv')
            table_name = request.form.get('table_name')
            return jsonify(
                Requests.API.update_tables_with_file(
                    table_name,
                    file.stream.read().decode(),
                    'csv_file.csv'))
        abort(403)

    @application.route('/db/check_status', methods=['GET'])
    def db_read_check_status():
        logger.info('/db/check_status')
        if AuthenticationRule.check_rule():
            return jsonify(Requests.API.connected())
        abort(403)

    @application.route(
        '/db/tables/<string:table_name>/<string:type_of_operation>',
        methods=['POST'])
    def db_operate_table_data(table_name: str, type_of_operation: str):
        logger.info(f'/db/tables/{table_name}/{type_of_operation}')
        return jsonify(
            Requests.API.operate_table_data(
                request,
                table_name,
                type_of_operation))

    @application.route(
        '/db/tables/<string:table_name>/<string:type_of_operation>/filtered',
        methods=['POST'])
    def db_operate_table_data_filtered(
            table_name: str, type_of_operation: str):
        logger.info(f'/db/tables/{table_name}/{type_of_operation}/filtered')
        return jsonify(
            Requests.API.operate_table_data_filtered(
                request, table_name, type_of_operation))

    @application.route(
        '/db/tables/<string:table_name>/<string:type_of_operation>/simpled',
        methods=['POST'])
    def db_operate_table_data_simpled(table_name: str, type_of_operation: str):
        logger.info(f'/db/tables/{table_name}/{type_of_operation}/simpled')
        return jsonify(
            Requests.API.operate_table_data_simpled(
                request,
                table_name,
                type_of_operation))

    @application.route('/actions/mail/send', methods=['POST'])
    def send_mail():
        logger.info('/actions/mail/send')
        return jsonify(Requests.API.send_mail(request))
