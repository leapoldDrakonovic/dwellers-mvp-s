from app.scripts.prepare import prepare
from app.handlers.errors import handle_errors
from app.handlers.www import handle_www
from app.handlers.api import handle_api

logger, application, dev_config, redis_worker = prepare()
handle_errors(application)
handle_www(application, logger, redis_worker)
handle_api(application, logger)

if __name__ == '__main__':
    try:
        application.run(
            host=dev_config['APP_HOST'],
            port=dev_config['APP_PORT'])
    except KeyError:
        application.run(
            host=dev_config['APP_HOST_OUTSIDE_CONTAINER'],
            port=dev_config['APP_PORT_OUTSIDE_CONTAINER'])
