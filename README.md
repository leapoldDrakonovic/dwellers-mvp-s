# dwellers-mvp

> Текущая версия продукта: 0.7.0

> Версия продукта для тестирования: 0.5.0 -> 0.6.0

> Версия продукта для релиза: 1.0.0

# Для запуска проекта необходимы:
    - Docker
    - docker-compose
    - Утилита Makefile

# --DEBUG
## Если при запуске проекта отсутствуют созданные таблицы (директория data в качестве volume) следует:
    - Обратиться к конечной точке /db/tables/create
    - Обратиться к конечной точке /db/tables/update/start_info
    - Перезапустить код make-методом: make update-all (Для того, чтобы при инициализации проекта сработал код подготовки redis)
    - Если 3-ий пункт не работает, следует перезапустить весь проект make-методом: make restart-compose

# Для запуска проекта требуется:
    - make start-compose

# Для остановки проекта требуется:
    - make stop-compose

# Для перезагрузки проекта можно:
    - make restart-compose

# Для обновления измененного кода можно:
    - make update-all

# Открыть проект можно:
    - Левое меню VSCode -> DOCKER -> mvp-nginx контейнер -> Открыть в браузере
    - Адресная строка в браузере -> localhost:1337/

    - БАГИ: После запуска проекта и открытия его в браузере переодично несколько раз может выводиться ошибка, необходимо перезапускать страницу несколько раз, пока ошибка не перестанет появляться

> Другие команды расположены в Makefile корневой директории

# Перечень конечных точек URL и будущего API:

## URL:
- [x] /   ==   /index   ==   /home   ==   /start
- [x] /builder?builder_id={int}
- [x] /building?building_id={int}
- [x] /flat?flat_id={int}
- [x] /map?map_filters={dict}
- [x] /about_us
- [x] /login # FORM[user, password]
- [x] /logout
- [x] /registrate

## API:
- [x] /db/tables/create
- [x] /db/tables/delete
- [x] /db/tables/recreate
- [x] /db/tables/update/start_info # устарел, теперь сделает использовать /db/tables/update/with_file
- [x] /db/tables/update/with_file
- [x] /db/check_status
- [x] /db/tables/{str::table_name}/{str::type_of_operation}
- [x] /db/tables/{str::table_name}/{str::type_of_operation}/filtered
- [x] /db/tables/{str::table_name}/{str::type_of_operation}/simpled
- [x] /actions/mail/send

> Все представленные конечные точки доступны, однако не отмеченные точки еще не доделаны даже до стадии тестирования и исправления ошибок

# Конфигурации:

> Для правильной работы конфигураций, необходимо:

- Для каждого файла конфигурации (например, ini), в названии которого указано .example, добавить соответствующий файл без .example
- Указать свои данные в новом файле
#   d w e l l e r s - m v p - s  
 