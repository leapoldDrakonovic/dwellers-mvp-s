from flask import Flask, session
from flask_admin import Admin
from flask.logging import default_handler
from dotenv import dotenv_values
from typing import Dict
import logging
import datetime
from app.scripts.redis import RedisWorker
from app.data.views import ImagesView, EndpointsView, AuthAdminIndexView, SQLExecuteView, AuthModelView, AuthRedisCli, SQLScriptsView
from app.database.scripts import DataBaseRequests

PREPARE_ENVS = dotenv_values('env/prepare.env')


def prepare() -> tuple[logging.Logger, Flask, Dict, RedisWorker]:
    """ Подготовка приложения и всех его производных к работе и возврат этих объектов """
    logger = __logger()
    logger.debug('STARTING SERVER...')
    logger.debug('WORKER IS STARTING...')
    application = __application(logger=logger)
    logger.debug('WORKER STARTED AND CONFIGURED SUCCESFULLY')
    logger.debug('DATABASE, ENV AND REDIS CONNECTIONS ARE STARTING...')
    __database()
    dev_config = __environment()
    logger.debug('ENVIRONMENT CREATED SUCCESFULLY')
    redis_worker = __redis()
    logger.debug(
        'DATABASE AND REDIS CONNECTIONS STARTED AND CONFIGURED SUCCESFULLY')
    __admin(application, redis_worker)
    logger.debug('ADMIN PANEL IS CONNECTED AND CONFIGURED SUCCESFULLY')
    logger.debug('SERVER IS READY TO ACCEPT CONNECTIONS')

    return logger, application, dev_config, redis_worker


def __application(**instances) -> Flask:
    """ Подготовка приложения """
    # ../ так как поиск директорий идет от prepare.py, то есть на уровень выше, чем app.py:
    application = Flask(
        __name__,  # не будет ли здесь __name__ prepare.py???
        template_folder=PREPARE_ENVS['APPLICATION_TEMPLATE_FOLDER'],
        static_folder=PREPARE_ENVS['APPLICATON_STATIC_FOLDER'],
    )
    application.secret_key = PREPARE_ENVS['APPLICATION_SECRET_KEY']
    application.debug = False
    application.config['SESSION_COOKIE_SECURE'] = True
    application.config['SESSION_COOKIE_NAME'] = '__s'
    application.config['SESSION_COOKIE_SAMESITE'] = 'Strict'

    if 'logger' in instances.keys():
        application.logger.addHandler(instances['logger'])
        application.logger.removeHandler(default_handler)

    return application


def __database(**instances) -> None:
    """ Подготовка базы данных (ее инициализация и заполнение, если в переменных
    окружения DATA_BASE_DEBUG_MODE установлен в true) """
    if PREPARE_ENVS['DATABASE_DEBUG_MODE']:
        if DataBaseRequests.API.connected()['state']:
            if DataBaseRequests.API.prepare()['state'] == 'True':
                DataBaseRequests.API.update_tables_with_admin(
                    PREPARE_ENVS['ADMIN_LOGIN'],
                    PREPARE_ENVS['ADMIN_PASSWORD'],
                    PREPARE_ENVS['ADMIN_ROLE']
                )
                print('CREATED TABLES')
            else:
                print('DATABASE TABLES ALREADY EXIST! PASSING THIS PHASE...')
        else:
            print('ERROR WITH CONNECTING TO DATABASE')


def __environment(*args, **kwargs) -> Dict:
    """ Подготовка окружения для работы приложения """
    dev_config = dotenv_values('env/app.env')

    return dev_config


def __setup_logger(
        formatter,
        name,
        log_file,
        level=logging.DEBUG) -> logging.Logger:
    """ Setup ane return one loggers instance """

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


def __logger(*args, **kwargs) -> logging.Logger:
    """ Подготовка модуля логирования """
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)8s] [WORKER:%(process)2d] [%(module)s:%(lineno)4d]: %(message)s',
        '%Y-%m-%d %H:%M:%S')  # '%(asctime)s %(levelname)s %(process)d ---- %(threadName)s %(module)s : %(funcName)s {%(pathname)s:%(lineno)d}: %(message)s','%Y-%m-%dT%H:%M:%SZ'
    _logger = __setup_logger(
        formatter,
        'logger',
        f"{PREPARE_ENVS['LOGGER_FOLDER']}/{str(datetime.datetime.now())[:-7]}".replace(
            ' ',
            '-') +
        '.log')
    return _logger


def __redis(*args, **kwargs):
    """ Подготовка redis """
    worker = RedisWorker(
        PREPARE_ENVS['REDIS_HOST'],
        PREPARE_ENVS['REDIS_PORT'],
        PREPARE_ENVS['REDIS_DECODE_RESPONSES'])
    if PREPARE_ENVS['APPLICATION_DEVELOPMENT_AREA']:
        worker.debug__prepare_space()
    return worker


def __admin(application: Flask, redis_worker: RedisWorker):
    """ Подготовка админ-панели """
    application.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(
        application,
        name='Admin Panel v0.2.0',
        template_mode='bootstrap3',
        index_view=AuthAdminIndexView())  # subdomain='admin'
    from app.database.models import ListOfBuilders, ListOfBuildings, ListOfFlats, ListOfImages, ListOfUsers
    admin.add_view(
        AuthModelView(
            ListOfBuilders, category='Database'
        )
    )
    admin.add_view(
        AuthModelView(
            ListOfBuildings, category='Database'
        )
    )
    admin.add_view(
        AuthModelView(
            ListOfFlats, category='Database'
        )
    )
    admin.add_view(
        AuthModelView(
            ListOfImages, category='Database'
        )
    )
    admin.add_view(
        AuthModelView(
            ListOfUsers, category='Database'
        )
    )
    admin.add_view(
        SQLScriptsView(
            name='SQL Scripts', endpoint='sql_scripts', category='Database'
        )
    )
    admin.add_view(
        AuthRedisCli(
            redis_worker.worker, name='Redis'
        )
    )
    admin.add_view(
        ImagesView(
            name='Images', endpoint='images'
        )
    )
    EndpointsView.get_app(application)
    admin.add_view(
        EndpointsView(
            name='Endpoints', endpoint='endpoints'
        )
    )
    admin.add_view(
        SQLExecuteView(
            name='SQL Execute', endpoint='sql_execute'
        )
    )
