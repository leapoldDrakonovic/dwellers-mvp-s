from flask import Request, Response, session
from dotenv import dotenv_values
import json


class Playground:
    def __init__(self, request: Request, response: Response) -> None:
        """ Обработчик запросов """
        self.request = request
        self.response = response

    def __cookie__set_safe(self,
                           key: str,
                           value: str,
                           secure_level: str | None = None,
                           max_age: int | None = None,
                           expires: str | int | float | None = None,
                           path: str | None = None,
                           domain: str | None = None,
                           secure: bool = False,
                           httponly: bool = False,
                           samesite: str | None = None
                           ):
        """ if secure_level is set to max, cookie will expire in 60 minutes """
        if secure_level is None:
            self.response.set_cookie(
                key,
                value,
                # max_age=max_age,
                # expires=expires,
                # path=path,
                # domain=domain,
                # secure=secure,
                # httponly=httponly,
                # samesite=samesite
            )
        elif secure_level == 'max':
            self.response.set_cookie(
                key,
                value,
                # max_age=3600,
                # expires=None,
                # path='/',
                # domain=None,
                # secure=True,
                # httponly=True,
                # samesite='Strict'
            )

    def cookie__set_safe(response: Response,
                         key: str,
                         value: str,
                         secure_level: str | None = None,
                         max_age: int | None = None,
                         expires: str | int | float | None = None,
                         path: str | None = None,
                         domain: str | None = None,
                         secure: bool = False,
                         httponly: bool = False,
                         samesite: str | None = None
                         ) -> Response:
        if secure_level is None:
            response.set_cookie(
                key,
                value,
                # max_age=max_age,
                # expires=expires,
                # path=path,
                # domain=domain,
                # secure=secure,
                # httponly=httponly,
                # samesite=samesite
            )
        elif secure_level == 'max':
            response.set_cookie(
                key,
                value,
                # max_age=3600,
                # expires=None,
                # path='/',
                # domain=None,
                # secure=True,
                # httponly=True,
                # samesite='Strict'
            )
        return response

    def set(self, is_cookie: bool, is_http: bool,
            content_type: str = 'text/html; charset=UTF-8') -> Response:
        """ Функция для правильной обработки запросов

        is_cookie: bool - нужно ли обрабатывать cookie
        is_http: bool - нужно ли обрабатывать http ответ
        """
        if is_cookie:
            self.__cookie_handler()
        if is_http:
            self.__http_handler(content_type)
        return self.response

    def __cookie_handler(self) -> None:
        # __language = self.request.cookies.get('__lang')
        # if __language is None:
        #     __env_values = dotenv_values('env/app.env')
        #     self.__cookie__set_safe('__lang', __env_values['BASIC_LANGUAGE'], None,
        # 63115200, None, '/', None, True, True, 'Strict')
        pass

    def __http_handler(self, content_type: str) -> None:
        # self.response.headers['X-Frame-Options'] = 'DENY'
        # self.response.headers['X-Content-Type-Options'] = 'nosniff'
        # self.response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        # self.response.headers['Content-Type'] = content_type
        # self.response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
        # self.response.headers['Content-Security-Policy'] = "default-src 'self'; style-src 'unsafe-inline' 'self' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; script-src 'unsafe-inline' 'self' https://ajax.googleapis.com https://api-maps.yandex.ru https://yastatic.net  https://core-renderer-tiles.maps.yandex.net; img-src 'self' data: https://api-maps.yandex.ru https://core-renderer-tiles.maps.yandex.net https://yandex.ru https://yandex.com;"
        # self.response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
        # self.response.headers['Cross-Origin-Resource-Policy'] = 'cross-origin'
        # self.response.headers['Cache-Control'] = 'max-age=100'
        pass


def __format_to_locale(__lang: str) -> str:
    if __lang is not None:
        if '-' in __lang:
            return __lang
        return '{}-{}'.format(__lang.lower(), __lang)
    __env_values = dotenv_values('env/app.env')
    return '{}-{}'.format(str(__env_values['BASIC_LANGUAGE']
                              ).lower(), __env_values['BASIC_LANGUAGE'])


def get_locale(__lang: str) -> dict:
    with open(f'languages/{__format_to_locale(__lang)}.json', 'r') as locale:
        return dict(json.load(locale))


def format_symbols(text: str) -> str:
    ''' Deleting some specific symbols from text and returning it '''
    symbols = '+'  # '+-/|\\!@#$%^&*()[]{}<>;:,.'
    for symbol in symbols:
        text = text.replace(symbol, '')
    return text
