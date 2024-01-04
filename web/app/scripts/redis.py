from functools import wraps
from peewee import ProgrammingError
import redis
from flask import request, session, make_response, render_template
from app.database.scripts import DataBaseOperations


class RedisWorker:
    def __init__(
            self,
            host: str,
            port: int,
            decode_responses: bool = True) -> None:
        self.worker = redis.Redis(
            host=host,
            port=port,
            decode_responses=decode_responses)

    def unregistred_session(self, route_function):
        @wraps(route_function)
        def decorated_function(*args, **kwargs):
            def set_unreg_cookie(file_path: str, data: dict):
                response_object = make_response(
                    render_template(file_path, data=data))

                counter = self.worker.get('unregistered_sessions_counter')
                values = self.worker.hgetall('unregistered_sessions_filters')
                values[counter] = ''
                self.worker.set(
                    'unregistered_sessions_counter',
                    int(counter) + 1)
                self.worker.hset(
                    'unregistered_sessions_filters',
                    mapping=values)

                response_object.set_cookie('unregistered_session', counter)
                return response_object

            def pass_unreg_cookie(file_path: str, data: dict):
                response_object = make_response(
                    render_template(file_path, data=data))
                response_object.delete_cookie('unregistered_session')
                return response_object
            if 'unregistered_session' not in request.cookies.keys():
                kwargs['response'] = set_unreg_cookie
            else:
                kwargs['response'] = pass_unreg_cookie
            return route_function(*args, **kwargs)
        return decorated_function

    def save_view(self, route_function):
        """ Сохранение уникальных, не уникальных и других посещений """
        @wraps(route_function)
        def decorated_function(*args, **kwargs):
            self.__new__ordinary_view()
            self.__new__registered_view() if 'user' in session.keys(
            ) else self.__new__unregistered__view()
            return route_function(*args, **kwargs)
        return decorated_function

    def save_builder_request(
            self,
            builder_id: int,
            __type_of: str = 'feedback'):
        """ Сохранение запроса пользователя """
        if __type_of == 'feedback':
            self.__new__feedback_request(builder_id)
        else:
            pass

    def __new__unic_view(self):
        pass

    def __new__ordinary_view(self):
        self.worker.set('total_views', int(self.worker.get('total_views')) + 1)

    def __new__unregistered__view(self):
        self.worker.set('total_unregistered_views', int(
            self.worker.get('total_unregistered_views')) + 1)

    def __new__registered_view(self):
        self.worker.set('total_registered_views', int(
            self.worker.get('total_registered_views')) + 1)

    def __new__feedback_request(self, builder_id: int):
        if self.worker.hsetnx(
            'total_developers_feedback_requests',
            builder_id,
                1) == 0:
            self.worker.hset('total_developers_feedback_requests', builder_id, int(
                self.worker.hget('total_developers_feedback_requests', builder_id)) + 1)

    def update_price_range_values(self) -> bool:
        try:
            buildings = DataBaseOperations.get.buildings.merged.flats()
        except ProgrammingError:
            return False
        flats_prices = []
        for building in buildings:
            for flat in building['flats']:
                flats_prices.append(int(flat['price']))

        # self.worker.set('stats_buildings_price_min', DataBaseOperations.get.buildings.find__price__min(flats_prices))
        self.worker.set(
            'stats_buildings_price_max',
            DataBaseOperations.get.buildings.find__price__max(flats_prices))
        return True

    def debug__prepare_space(self) -> None:
        self.worker.set('total_unregistered_views', 0)
        self.worker.set('total_registered_views', 0)
        self.worker.set('total_unic_views', 0)
        self.worker.set('total_views', 0)
        self.update_price_range_values()

    def get(self, keys: list = []) -> list:
        """ Возвращает каждому указанному ключу его значение, доступное по такому же индексу в списке """
        values = []

        for key in keys:
            if key == 'buildings_min':
                # Заглушка, так как получение минимального ценового значения
                # работает неправильно
                values.append(0)
            elif key == 'buildings_max':
                values.append(self.worker.get('stats_buildings_price_max'))

        return values
