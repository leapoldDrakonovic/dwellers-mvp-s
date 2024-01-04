from flask import Request
from app.database.models import db, MODELS, ListOfBuilders, ListOfBuildings, ListOfFlats, ListOfImages, ListOfUsers
from app.scripts.helpers import format_symbols
from random import randrange, choice, random
from hashlib import sha256
from app.scripts import filters as fl
import json


class DataBaseRequests:
    def __connect_and_exit(command):
        def wrapper(*args, **kwargs):
            try:
                db.connect()
            except Exception as error:
                db.close()
                return error
            args = command(*args, **kwargs)
            db.close()
            return args
        return wrapper

    @__connect_and_exit
    def index(language: str | None = None):
        # Получение данных из БД:
        builders = DataBaseOperations.get.builders.by_range_id(
            7, 'index', language)
        buildings = DataBaseOperations.get.buildings.by_range_id(
            12, 'index', language)
        logos = DataBaseOperations.get.images.by_type('builder')
        buildings_preview_images = DataBaseOperations.get.images.by_type(
            'building')
        length_of_all_buildings = DataBaseOperations.get.buildings.counted()

        # Обработка полученных данных:
        ids = []
        for builder in builders:
            ids.append(builder['id'])

        for builder in builders:
            for logo in logos:
                if builder['id'] == logo['group_id']:
                    builder['type'] = logo['type']
                    builder['group_id'] = logo['group_id']
                    builder['file_name'] = logo['file_name']
                    break

        for building in buildings:
            for image in buildings_preview_images:
                if building['id'] == image['group_id']:
                    building['type'] = image['type']
                    building['group_id_for_image'] = image['group_id']
                    building['file_name'] = image['file_name']
                    break
        return builders, buildings, length_of_all_buildings

    @__connect_and_exit
    def builder(builder_id: int, language: str | None = None):
        # Получение данных из БД:
        builders = DataBaseOperations.get.builders.by_id(builder_id, language)
        buildings, more_buildings_button_off = DataBaseOperations.get.buildings.merged.by_id__flats__grouped(
            builder_id, language)
        slider_images = DataBaseOperations.get.images.by_type('building')

        # Обработка полученных данных:
        for building in buildings:
            for flats in building['grouped_flats'].values():

                m2_list = []
                price_list = []

                for flat in flats:
                    m2_list.append(flat['all_size_m2'])
                    price_list.append(flat['price'])

                min_m2_value = min(m2_list)
                min_price_value = min(price_list)

                flats[0] = {}
                flats[0]['min_m2_value'] = min_m2_value
                flats[0]['min_price_value'] = min_price_value

        ids = []
        for building in buildings:
            ids.append(building['id'])

        for building in buildings:
            for image in slider_images:
                if building['id'] == image['group_id']:
                    building['type'] = image['type']
                    building['group_id_for_image'] = image['group_id']
                    building['file_name'] = image['file_name']
                    break

        return builders, buildings, more_buildings_button_off

    @__connect_and_exit
    def building(building_id: int, language: str):
        # Получение данных из БД:
        building = DataBaseOperations.get.buildings.by_id(
            building_id, language)
        all_images = DataBaseOperations.get.images.by_type('building')
        flats = DataBaseOperations.get.flats.by_group_id(building_id, language)
        all_flats_images = DataBaseOperations.get.images.by_type('flat')
        builder = DataBaseOperations.get.builders.by_id(
            building['group_id'], language)
        building['min_flats_price'] = DataBaseOperations.get.buildings.find__price__min(
            flat['price'] for flat in flats)
        simular_buildings = DataBaseOperations.get.buildings.filtered({
            'group_id': building['group_id'],
            'city': building['city'],
            'country': building['country'],
            '!id': building['id'],
            'limit': 3,
        }, language)
        for simular_building in simular_buildings:
            building_flats = DataBaseOperations.get.flats.by_group_id(
                simular_building['id'])
            simular_building['min_flats_price'] = DataBaseOperations.get.buildings.find__price__min(
                flat['price'] for flat in building_flats)
        # Обработка полученных данных:
        for simular_building in simular_buildings:
            for image in all_images:
                if simular_building['id'] == image['group_id']:
                    simular_building['type'] = image['type']
                    simular_building['group_id_for_image'] = image['group_id']
                    simular_building['file_name'] = image['file_name']
                    break

        building_images = []
        for image in all_images:
            if building['id'] == image['group_id']:
                building_images.append({
                    'type': image['type'],
                    'group_id_for_image': image['group_id'],
                    'file_name': image['file_name'],
                })

        for flat in flats:
            for image in all_flats_images:
                if flat['id'] == image['group_id'] and image['file_name'].startswith(
                        'plan'):
                    flat['type'] = image['type']
                    flat['group_id_for_image'] = image['group_id']
                    flat['file_name'] = image['file_name']
                    break

        grouped_flats = {}
        current_rooms = 0
        max_rooms = 10  # ЗАМЕНИТЬ ЭТО 100%!!!!!!!!!
        for i in range(max_rooms):
            for flat_id in range(len(flats)):
                if flats[flat_id]['rooms'] == current_rooms:
                    try:
                        grouped_flats[current_rooms].append(flats[flat_id])
                    except KeyError:
                        grouped_flats[current_rooms] = [flats[flat_id]]
                    # del flats[flat_id] # ?
            current_rooms += 1

        return building, building_images, flats, builder, simular_buildings, grouped_flats

    @__connect_and_exit
    def flat(flat_id: int, language: str | None = None):
        # Получение данных из БД:
        flat = DataBaseOperations.get.flats.by_id(flat_id, language)
        all_images = DataBaseOperations.get.images.by_type('flat')
        building = DataBaseOperations.get.buildings.by_id(
            flat['group_id'], language)
        builder = DataBaseOperations.get.builders.by_id(
            building['group_id'], language)
        another_flats = DataBaseOperations.get.flats.filtered({
            'group_id': flat['group_id'],
            '!id': flat_id,
        }, language)

        # Обработка полученных данных:
        for another_flat in another_flats:
            for image in all_images:
                if another_flat['id'] == image['group_id'] and image['file_name'].startswith(
                        'plan'):
                    another_flat['type'] = image['type']
                    another_flat['group_id_for_image'] = image['group_id']
                    another_flat['file_name'] = image['file_name']
                    break

        grouped_another_flats = {}
        current_rooms = 0
        max_rooms = 10  # ЗАМЕНИТЬ ЭТО 100%!!!!!!!!!
        for i in range(max_rooms):
            for flat_id in range(len(another_flats)):
                if another_flats[flat_id]['rooms'] == current_rooms:
                    try:
                        grouped_another_flats[current_rooms].append(
                            another_flats[flat_id])
                    except KeyError:
                        grouped_another_flats[current_rooms] = [
                            another_flats[flat_id]]
                    # del flats[flat_id] # ?
            current_rooms += 1

        flat_images = []
        for image in all_images:
            if flat['id'] == image['group_id']:
                flat_images.append({
                    'type': image['type'],
                    'group_id_for_image': image['group_id'],
                    'file_name': image['file_name'],
                })

        return flat, flat_images, building, builder, grouped_another_flats


    @__connect_and_exit
    def login(session, login: str, password: str) -> None:
        if DataBaseOperations.get.users.state_by_login_and_password__sha256(
                login, password):
            session['user'] = login
            session['user_role'] = DataBaseOperations.get.users.role_group_by_login_and_password__sha256(
                login, password)

    @__connect_and_exit
    def registrate(login: str, password: str):
        return DataBaseOperations.post.users(login, password)

    class API:
        def __connect_and_exit(command):
            def wrapper(*args, **kwargs):
                try:
                    db.connect()
                except Exception as error:
                    db.close()
                    return {'state': str(error)}
                args = command(*args, **kwargs)
                db.close()
                return args
            return wrapper

        @__connect_and_exit
        def connected():
            return {'state': 'True'}

        @__connect_and_exit
        def recreate_tables() -> dict:
            db.drop_tables([ListOfBuilders, ListOfBuildings,
                           ListOfFlats, ListOfImages, ListOfUsers])
            db.create_tables([ListOfBuilders, ListOfBuildings,
                             ListOfFlats, ListOfImages, ListOfUsers])
            return {'state': 'True'}

        @__connect_and_exit
        def delete_tables() -> dict:
            db.drop_tables([ListOfBuilders, ListOfBuildings,
                           ListOfFlats, ListOfImages, ListOfUsers])
            return {'state': 'True'}

        @__connect_and_exit
        def prepare():
            try:
                if db.get_tables() == []:
                    for model in MODELS.values():
                        model.create_table()
                    return {'state': 'True'}
                return {'state': 'False'}
            except Exception:
                return {'state': 'False'}

        @__connect_and_exit
        def update_tables_with_admin(
                login: str,
                password: str,
                role: str = 'admin'):
            ListOfUsers(
                login=login,
                password=sha256(
                    password.encode()).hexdigest(),
                role=role).save()
            return {'state': 'True'}

        @__connect_and_exit
        def update_tables_with_start_info():
            alphabet = 'abcdefghigklmnopqrstuvwxyz   '
            numbers = '123456789'
            years = [
                1990,
                1991,
                1992,
                1993,
                1994,
                1995,
                1996,
                1997,
                1998,
                1999,
                2000,
                2001,
                2002,
                2003,
                2004,
                2005,
                2006,
                2007,
                2008,
                2009,
                2010]
            countries = {
                'Russia': ['Moscow', 'Saint-Peterburg', 'Sochi'],
                'England': ['London', 'Liverpool', 'Bristol'],
                'Serbia': ['Belgrade', 'Bor', 'Pirot'],
            }
            addresses = [
                '1828 Golf Course Drive',
                '3817 Woodland Terrace',
                '4800 Golf Course Drive',
                '3092 Primrose Lane',
                '559 Armbrester Drive',
                '3188 Johnny Lane',
            ]

            coords_x = 55.60804306913301
            coords_y = 37.61597349999994

            types_of_buildings = ['In process', 'Soon', 'Marketing']

            data = {
                'builder': {
                    'name': [],
                    'info': [],
                    'foundation_year': [],
                    'price_start': [],
                    'price_end': [],
                    'completed_projects': [],
                    'projects_in_process': [],
                },
                'building': {
                    'name': [],
                    'price_start': [],
                    'price_end': [],
                    'country': [],
                    'city': [],
                    'address': [],
                    'price_m2': [],
                    'type_of_building': [],
                    'coord_x': [],
                    'coord_y': [],
                },
                'flat': {
                    'price': [],
                    'price_per_m2': [],
                    'rooms': [],
                    'floor': [],
                    'all_size_m2': [],
                    'another_size_m2': [],
                },
                'image': {

                },
            }
            builders_count = 16
            buildings_count = 23
            flats_count = 33
            # Заполнение data.builders:
            for i in range(builders_count):
                random_name_length = randrange(4, 17)
                name = ''
                for j in range(random_name_length):
                    name += choice(alphabet)
                data['builder']['name'].append(name)

                random_info_length = randrange(100, 250)
                info = ''
                for j in range(random_info_length):
                    info += choice(alphabet)
                data['builder']['info'].append(info)

                data['builder']['foundation_year'].append(choice(years))

                start_price = ''
                for j in range(7):
                    start_price += choice(numbers)
                data['builder']['price_start'].append(int(start_price))

                end_price = ''
                for j in range(7):
                    end_price += choice(numbers)
                data['builder']['price_end'].append(int(end_price))

                c_projects = ''
                for j in range(choice([1, 2])):
                    c_projects += choice(numbers)
                data['builder']['completed_projects'].append(int(c_projects))

                projects_in_p = ''
                for j in range(choice([1, 2])):
                    projects_in_p += choice(numbers)
                data['builder']['projects_in_process'].append(
                    int(projects_in_p))

            # Заполнение data.buildings:
            for i in range(buildings_count):
                random_name_length = randrange(10, 15)
                name = ''
                for j in range(random_name_length):
                    name += choice(alphabet)
                data['building']['name'].append(name)

                start_price = ''
                for j in range(7):
                    start_price += choice(numbers)
                data['building']['price_start'].append(int(start_price))

                end_price = ''
                for j in range(7):
                    end_price += choice(numbers)
                data['building']['price_end'].append(int(end_price))

                country = choice(list(countries.keys()))
                data['building']['country'].append(country)
                data['building']['city'].append(choice(countries[country]))
                data['building']['address'].append(choice(addresses))

                price_m2 = ''
                for j in range(choice([2, 3])):
                    price_m2 += choice(numbers)
                data['building']['price_m2'].append(int(price_m2))

                data['building']['type_of_building'].append(
                    choice(types_of_buildings))

                data['building']['coord_x'].append(coords_x + random())
                data['building']['coord_y'].append(coords_y + random())

            # Заполнение data.flats:
            for i in range(flats_count):
                price = ''
                for j in range(7):
                    price += choice(numbers)
                data['flat']['price'].append(int(price))

                price_per_m2 = ''
                for j in range(3):
                    price_per_m2 += choice(numbers)
                data['flat']['price_per_m2'].append(int(price_per_m2))

                rooms = ''
                for j in range(1):
                    rooms += choice(numbers)
                data['flat']['rooms'].append(int(rooms))

                floor = ''
                for j in range(choice([1, 2])):
                    floor += choice(numbers)
                data['flat']['floor'].append(int(floor))

                all_size_m2 = ''
                for j in range(choice([2, 3])):
                    all_size_m2 += choice(numbers)
                data['flat']['all_size_m2'].append(int(all_size_m2))

                another_size_m2 = ''
                for j in range(choice([2, 3])):
                    another_size_m2 += choice(numbers)
                data['flat']['another_size_m2'].append(int(another_size_m2))

            # Заполнение таблицы застройщиков:
            for i in range(builders_count):
                row = ListOfBuilders(
                    name=data['builder']['name'][i],
                    info=data['builder']['info'][i],
                    foundation_year=data['builder']['foundation_year'][i],
                    completed_projects=data['builder']['completed_projects'][i],
                    projects_in_process=data['builder']['projects_in_process'][i],
                    trusted=True)
                row.save()

            # Заполнение таблицы зданий:
            for i in range(buildings_count):
                row = ListOfBuildings(
                    group_id=randrange(
                        1,
                        builders_count + 1),
                    name=data['building']['name'][i],
                    info='kfl oapsf asoijf as  oasfjdsp asdp jasd asp jfs asdjiasd pfdsjksqi',
                    country=data['building']['country'][i],
                    city=data['building']['city'][i],
                    address=data['building']['address'][i],
                    parking=True,
                    type_of_building=data['building']['type_of_building'][i],
                    coord_x=data['building']['coord_x'][i],
                    coord_y=data['building']['coord_y'][i],
                )
                row.save()

            # Заполнение таблицы квартир
            for i in range(flats_count):
                row = ListOfFlats(
                    group_id=randrange(
                        1,
                        flats_count + 1),
                    info='kfl oapsf asoijf as  oasfjdsp asdp jasd asp jfs asdjiasd pfdsjksqi',
                    price=data['flat']['price'][i],
                    price_per_m2=data['flat']['price_per_m2'][i],
                    rooms=data['flat']['rooms'][i],
                    size=-1,
                    floor=data['flat']['floor'][i],
                    all_size_m2=data['flat']['all_size_m2'][i],
                    kitchen_size_m2=data['flat']['another_size_m2'][i],
                    bathroom_size_m2=data['flat']['all_size_m2'][i],
                    hall_size_m2=data['flat']['another_size_m2'][i],
                    inside_size_m2=data['flat']['all_size_m2'][i],
                )
                row.save()

            # Заполнение таблицы картинок
            for i in range(builders_count):
                row = ListOfImages(
                    type='builder',
                    group_id=i + 1,
                    file_name='logo.png')
                row.save()

            for i in range(buildings_count):
                row = ListOfImages(
                    type='building',
                    group_id=i + 1,
                    file_name='1.jpg')
                row.save()
                row = ListOfImages(
                    type='building',
                    group_id=i + 1,
                    file_name='2.jpg')
                row.save()
                row = ListOfImages(
                    type='building',
                    group_id=i + 1,
                    file_name='3.jpg')
                row.save()

            for i in range(flats_count):
                row = ListOfImages(
                    type='flat', group_id=i + 1, file_name='1.jpg')
                row.save()
                row = ListOfImages(
                    type='flat', group_id=i + 1, file_name='2.jpg')
                row.save()
                row = ListOfImages(
                    type='flat', group_id=i + 1, file_name='3.jpg')
                row.save()
                row = ListOfImages(
                    type='flat', group_id=i + 1, file_name='4.jpg')
                row.save()
                row = ListOfImages(
                    type='flat',
                    group_id=i + 1,
                    file_name='plan.jpg')
                row.save()

            try:
                row = ListOfUsers(
                    login='admin', password=sha256(
                        'admin'.encode()).hexdigest(), role='admin')
                row.save()
            except Exception:
                pass

            return {'state': 'True'}

        @__connect_and_exit
        def update_tables_with_file(
                table_name: str,
                file: str,
                file_path: str):
            if table_name == 'builders':
                post_table = DataBaseOperations.post.builders
            elif table_name == 'buildings':
                post_table = DataBaseOperations.post.buildings
            elif table_name == 'flats':
                post_table = DataBaseOperations.post.flats
            else:
                pass

            import csv
            try:
                with open(f'../tmp/{file_path}', newline='') as csvfile:
                    spamreader = csv.reader(csvfile)
                    i = 0
                    for row in spamreader:
                        for j in range(len(row)):
                            if row[j] == '':
                                row[j] = 0
                        if i == 0:  # чтобы не срабатывала строка с названиями столбцов
                            i += 1
                            continue
                        post_table(*row)
            except Exception as error:
                return {'state': str(error)}
            return {'state': 'True'}

        @__connect_and_exit
        def operate_table_data(
                request,
                table_name: str,
                type_of_operation: str):
            response_data = {}
            buttons_off = True
            if table_name == 'ListOfBuilders':
                if type_of_operation.lower() == 'get':
                    request_data = request.json['builders_ids']
                    for k in range(len(request_data)):
                        request_data[k] = int(request_data[k])
                    builders_new = []
                    new_builders_length = int(request.json['response_length'])
                    i = 1

                    if not request.json['same_builder'][0]:
                        for element in ListOfBuilders.select().where(
                                ListOfBuilders.id.not_in(request_data)):
                            builders_new.append(
                                {
                                    'id': element.id,
                                    'name': element.name,
                                    'info': element.info,
                                    'foundation_year': element.foundation_year,
                                    'completed_projects': element.completed_projects,
                                    'projects_in_process': element.projects_in_process,
                                    'trusted': element.trusted,
                                })
                            if i == new_builders_length:
                                for last_element in ListOfBuilders.select().where(
                                        ListOfBuilders.id == int(request_data[-1]) + new_builders_length):
                                    buttons_off = False
                                break
                            i += 1
                    else:
                        for element in ListOfBuilders.select().where(
                            (ListOfBuilders.id.not_in(request_data)) & (
                                ListOfBuilders.id == request.json['same_builder'][1])):
                            builders_new.append(
                                {
                                    'id': element.id,
                                    'name': element.name,
                                    'info': element.info,
                                    'foundation_year': element.foundation_year,
                                    'completed_projects': element.completed_projects,
                                    'projects_in_process': element.projects_in_process,
                                    'trusted': element.trusted,
                                })
                            if i == new_builders_length:
                                for last_element in ListOfBuilders.select().where(
                                        ListOfBuilders.id == int(request_data[-1]) + new_builders_length):
                                    buttons_off = False
                                break
                            i += 1

                    logos = []
                    ids = []
                    for builder in builders_new:
                        ids.append(builder['id'])

                    for element in ListOfImages.select().where(ListOfImages.type == 'builder'):
                        logos.append({'type': element.type,
                                      'group_id': element.group_id,
                                      'file_name': element.file_name,
                                      })

                    for builder in builders_new:
                        for logo in logos:
                            if builder['id'] == logo['group_id']:
                                builder['type'] = logo['type']
                                builder['group_id'] = logo['group_id']
                                builder['file_name'] = logo['file_name']
                                break

                    response_data = builders_new

            elif table_name == 'ListOfBuildings':
                if type_of_operation.lower() == 'get':
                    request_data = request.json['buildings_ids']
                    for k in range(len(request_data)):
                        try:
                            request_data[k] = int(request_data[k])
                        except TypeError:
                            pass
                    buildings_new = []
                    buildings_ids = []
                    new_buildings_length = int(request.json['response_length'])
                    i = 0

                    if not request.json['same_builder'][0]:
                        for element in ListOfBuildings.select().where(
                                ListOfBuildings.id.not_in(request_data)):
                            buildings_new.append(
                                {
                                    'id': element.id,
                                    'group_id': element.group_id,
                                    'name': element.name,
                                    'country': element.country,
                                    'city': element.city,
                                    'address': element.address,
                                    'parking': element.parking,
                                    'type_of_building': element.type_of_building,
                                })
                            if i == new_buildings_length:
                                for last_element in ListOfBuildings.select().where(
                                        ListOfBuildings.id == int(request_data[-1]) + new_buildings_length):
                                    buttons_off = False
                                break
                            i += 1
                    else:
                        for element in ListOfBuildings.select().where(
                            (ListOfBuildings.id.not_in(request_data)) & (
                                ListOfBuildings.group_id == request.json['same_builder'][1])):
                            buildings_new.append(
                                {
                                    'id': element.id,
                                    'group_id': element.group_id,
                                    'name': element.name,
                                    'country': element.country,
                                    'city': element.city,
                                    'address': element.address,
                                    'parking': element.parking,
                                    'type_of_building': element.type_of_building,
                                })
                            buildings_ids.append(element.id)

                            flats = []
                            for element in ListOfFlats.select().where(ListOfFlats.group_id == element.id):
                                flats.append({'id': element.id,
                                              'group_id': element.group_id,
                                              'price': element.price,
                                              'rooms': element.rooms,
                                              'floor': element.floor,
                                              'all_size_m2': element.all_size_m2,
                                              'kitchen_size_m2': element.kitchen_size_m2,
                                              'bathroom_size_m2': element.bathroom_size_m2,
                                              'hall_size_m2': element.hall_size_m2,
                                              'inside_size_m2': element.inside_size_m2,
                                              })

                            buildings_new[i]['grouped_flats'] = {}
                            current_rooms = 0
                            max_rooms = 10  # ЗАМЕНИТЬ ЭТО 100%?
                            for j in range(max_rooms):
                                for flat_id in range(len(flats)):
                                    if flats[flat_id]['rooms'] == current_rooms:
                                        try:
                                            buildings_new[i]['grouped_flats'][current_rooms].append(
                                                flats[flat_id])
                                        except KeyError:
                                            buildings_new[i]['grouped_flats'][current_rooms] = [
                                                flats[flat_id]]
                                        # del flats[flat_id] # ?
                                current_rooms += 1

                            if i == new_buildings_length:
                                for last_element in ListOfBuildings.select().where(
                                        ListOfBuildings.id == int(request_data[-1]) + new_buildings_length):
                                    buttons_off = False
                                break
                            i += 1

                        for building in buildings_new:
                            for flats in building['grouped_flats'].values():

                                m2_list = []
                                price_list = []

                                for flat in flats:
                                    m2_list.append(flat['all_size_m2'])
                                    price_list.append(flat['price'])

                                min_m2_value = min(m2_list)
                                min_price_value = min(price_list)

                                flats[0] = {}
                                flats[0]['min_m2_value'] = min_m2_value
                                flats[0]['min_price_value'] = min_price_value

                    buildings_images = []
                    for element in ListOfImages.select().where(ListOfImages.type == 'building'):
                        buildings_images.append({
                            'type': element.type, 'group_id': element.group_id, 'file_name': element.file_name,
                        })

                    for building in buildings_new:
                        for image in buildings_images:
                            if building['id'] == image['group_id']:
                                building['type'] = image['type']
                                building['group_id_for_image'] = image['group_id']
                                building['file_name'] = image['file_name']
                                break

                    response_data = buildings_new

            return {'data': response_data, 'buttons_off': buttons_off}

        @__connect_and_exit
        def operate_table_data_filtered(
                request: Request,
                table_name: str,
                type_of_operation: str):
            response_data = {}
            if table_name == 'ListOfBuildings':
                if type_of_operation.lower() == 'get':
                    # Получение списка уже отфильтрованных объектов из кэша:
                    # list_of_previous_filters = redis_worker.get_session_filters(request.cookies['unregistered_session'])

                    # Получение всех данных из БД:
                    try:
                        filters = request.json['filters']
                    except Exception:
                        try:
                            filters = json.loads(
                                request.args.get('filters'))['filters']
                        except KeyError:
                            filters = None

                    if filters is None:
                        buildings = fl.apply_filter(
                            ListOfBuildings, {}, ListOfFlats)
                        response_length = int(json.loads(
                            request.args.get('filters'))['length'])
                        i = 0
                        full_buildings_info = []
                        for building in buildings:
                            full_buildings_info.append({
                                'id': building.id, 'group_id': building.group_id,
                                'name': building.name,
                                'country': building.country,
                                'city': building.city, 'address': building.address,
                                'parking': building.parking,
                                'type_of_building': building.type_of_building,
                                'coord_x': building.coord_x,
                                'coord_y': building.coord_y,
                            })
                            i += 1
                            if i == response_length:
                                break
                        all_images = []
                        for element in ListOfImages.select().where(ListOfImages.type == 'building'):
                            all_images.append({
                                'type': element.type, 'group_id': element.group_id, 'file_name': element.file_name,
                            })
                        for building in full_buildings_info:
                            for image in all_images:
                                if building['id'] == image['group_id']:
                                    building['type'] = image['type']
                                    building['group_id_for_image'] = image['group_id']
                                    building['file_name'] = image['file_name']
                                    break

                        for building in full_buildings_info:
                            flats = []
                            for element in ListOfFlats.select().where(
                                    ListOfFlats.group_id == building['id']):
                                flats.append({'id': element.id,
                                              'group_id': element.group_id,
                                              'price': element.price,
                                              'rooms': element.rooms,
                                              'floor': element.floor,
                                              'all_size_m2': element.all_size_m2,
                                              'kitchen_size_m2': element.kitchen_size_m2,
                                              'bathroom_size_m2': element.bathroom_size_m2,
                                              'hall_size_m2': element.hall_size_m2,
                                              'inside_size_m2': element.inside_size_m2,
                                              })

                            building['grouped_flats'] = {}
                            current_rooms = 0
                            max_rooms = 10  # ЗАМЕНИТЬ ЭТО 100%?
                            for j in range(max_rooms):
                                for flat_id in range(len(flats)):
                                    if flats[flat_id]['rooms'] == current_rooms:
                                        try:
                                            building['grouped_flats'][current_rooms].append(
                                                flats[flat_id])
                                        except KeyError:
                                            building['grouped_flats'][current_rooms] = [
                                                flats[flat_id]]
                                        # del flats[flat_id] # ?
                                current_rooms += 1

                        for building in full_buildings_info:
                            for flats in building['grouped_flats'].values():
                                m2_list = []
                                price_list = []

                                for flat in flats:
                                    m2_list.append(flat['all_size_m2'])
                                    price_list.append(flat['price'])

                                min_m2_value = min(m2_list)
                                min_price_value = min(price_list)

                                flats[0] = {}
                                flats[0]['min_m2_value'] = min_m2_value
                                flats[0]['min_price_value'] = min_price_value

                        response_data = {'data': full_buildings_info}
                    else:
                        # Удаление пустых данных
                        filter_keys = []
                        for filter_key in filters.keys():
                            filter_keys.append(filter_key)
                        for filter_key in filter_keys:
                            if filters[filter_key] == '':
                                del filters[filter_key]
                            elif isinstance(filters[filter_key], list):
                                if len(filters[filter_key]) == 0:
                                    del filters[filter_key]

                        # Редактирование данных (в частности убираем знаки +, но потом вместо этого
                        # нужно будет сделать так, что если есть +, то берем все элементы, которые в БД
                        # больше значения перед плюсом
                        for filter_key in filters.keys():
                            if isinstance(filters[filter_key], list):
                                for sub_key in range(len(filters[filter_key])):
                                    filters[filter_key][sub_key] = format_symbols(
                                        filters[filter_key][sub_key])
                            else:
                                filters[filter_key] = format_symbols(
                                    filters[filter_key])

                        buildings = fl.apply_filter(
                            ListOfBuildings, filters, ListOfFlats)

                        if request.content_type != 'application/json':
                            if json.loads(request.args.get('filters'))[
                                    'configs']['responseType'] == 'fullData':
                                full_buildings_info = []
                                for building in buildings:
                                    full_buildings_info.append({
                                        'id': building.id, 'group_id': building.group_id,
                                        'name': building.name, 'country': building.country,
                                        'city': building.city, 'address': building.address,
                                        'parking': building.parking,
                                        'type_of_building': building.type_of_building,
                                        'coord_x': building.coord_x,
                                        'coord_y': building.coord_y,
                                    })
                                all_images = []
                                for element in ListOfImages.select().where(ListOfImages.type == 'building'):
                                    all_images.append({
                                        'type': element.type, 'group_id': element.group_id, 'file_name': element.file_name,
                                    })
                                for building in full_buildings_info:
                                    for image in all_images:
                                        if building['id'] == image['group_id']:
                                            building['type'] = image['type']
                                            building['group_id_for_image'] = image['group_id']
                                            building['file_name'] = image['file_name']
                                            break

                                for building in full_buildings_info:
                                    flats = []

                                    for element in ListOfFlats.select().where(
                                            ListOfFlats.group_id == building['id']):
                                        flats.append(
                                            {
                                                'id': element.id,
                                                'group_id': element.group_id,
                                                'price': element.price,
                                                'rooms': element.rooms,
                                                'floor': element.floor,
                                                'all_size_m2': element.all_size_m2,
                                                'kitchen_size_m2': element.kitchen_size_m2,
                                                'bathroom_size_m2': element.bathroom_size_m2,
                                                'hall_size_m2': element.hall_size_m2,
                                                'inside_size_m2': element.inside_size_m2,
                                            })

                                    building['grouped_flats'] = {}
                                    current_rooms = 0
                                    max_rooms = 10  # ЗАМЕНИТЬ ЭТО 100%?
                                    for j in range(max_rooms):
                                        for flat_id in range(len(flats)):
                                            if flats[flat_id]['rooms'] == current_rooms:
                                                try:
                                                    building['grouped_flats'][current_rooms].append(
                                                        flats[flat_id])
                                                except KeyError:
                                                    building['grouped_flats'][current_rooms] = [
                                                        flats[flat_id]]
                                                # del flats[flat_id] # ?
                                        current_rooms += 1

                                for building in full_buildings_info:
                                    for flats in building['grouped_flats'].values(
                                    ):
                                        m2_list = []
                                        price_list = []

                                        for flat in flats:
                                            m2_list.append(flat['all_size_m2'])
                                            price_list.append(flat['price'])

                                        min_m2_value = min(m2_list)
                                        min_price_value = min(price_list)

                                        flats[0] = {}
                                        flats[0]['min_m2_value'] = min_m2_value
                                        flats[0]['min_price_value'] = min_price_value

                                response_data = {'data': full_buildings_info}
                        else:
                            if request.json['configs']['responseType'] == 'length':
                                # Выдача только количества найденных элементов
                                response_data = {'data': len(buildings)}
                            elif request.json['configs']['responseType'] == 'smallData':
                                small_buildings_info = []
                                for building in buildings:
                                    small_buildings_info.append({
                                        'id': building.id,
                                        'name': building.name,
                                        'city': building.city,
                                        'country': building.country,
                                    })
                                all_images = []
                                for element in ListOfImages.select().where(ListOfImages.type == 'building'):
                                    all_images.append({
                                        'type': element.type, 'group_id': element.group_id, 'file_name': element.file_name,
                                    })
                                for building in small_buildings_info:
                                    for image in all_images:
                                        if building['id'] == image['group_id']:
                                            building['type'] = image['type']
                                            building['group_id_for_image'] = image['group_id']
                                            building['file_name'] = image['file_name']
                                            break
                                response_data = {'data': small_buildings_info}
                            elif request.json['configs']['responseType'] == 'fullData':
                                full_buildings_info = []
                                for building in buildings:
                                    full_buildings_info.append({
                                        'id': building.id, 'group_id': building.group_id,
                                        'name': building.name,
                                        'country': building.country,
                                        'city': building.city, 'address': building.address,
                                        'parking': building.parking,
                                        'type_of_building': building.type_of_building,
                                        'coord_x': building.coord_x,
                                        'coord_y': building.coord_y,
                                    })
                                all_images = []
                                for element in ListOfImages.select().where(ListOfImages.type == 'building'):
                                    all_images.append({
                                        'type': element.type, 'group_id': element.group_id, 'file_name': element.file_name,
                                    })
                                for building in full_buildings_info:
                                    for image in all_images:
                                        if building['id'] == image['group_id']:
                                            building['type'] = image['type']
                                            building['group_id_for_image'] = image['group_id']
                                            building['file_name'] = image['file_name']
                                            break

                                for building in full_buildings_info:
                                    flats = []
                                    for element in ListOfFlats.select().where(
                                            ListOfFlats.group_id == building['id']):
                                        flats.append(
                                            {
                                                'id': element.id,
                                                'group_id': element.group_id,
                                                'price': element.price,
                                                'rooms': element.rooms,
                                                'floor': element.floor,
                                                'all_size_m2': element.all_size_m2,
                                                'kitchen_size_m2': element.kitchen_size_m2,
                                                'bathroom_size_m2': element.bathroom_size_m2,
                                                'hall_size_m2': element.hall_size_m2,
                                                'inside_size_m2': element.inside_size_m2,
                                            })

                                    building['grouped_flats'] = {}
                                    current_rooms = 0
                                    max_rooms = 10  # ЗАМЕНИТЬ ЭТО 100%?
                                    for j in range(max_rooms):
                                        for flat_id in range(len(flats)):
                                            if flats[flat_id]['rooms'] == current_rooms:
                                                try:
                                                    building['grouped_flats'][current_rooms].append(
                                                        flats[flat_id])
                                                except KeyError:
                                                    building['grouped_flats'][current_rooms] = [
                                                        flats[flat_id]]
                                                # del flats[flat_id] # ?
                                        current_rooms += 1

                                for building in full_buildings_info:
                                    for flats in building['grouped_flats'].values(
                                    ):
                                        m2_list = []
                                        price_list = []

                                        for flat in flats:
                                            m2_list.append(flat['all_size_m2'])
                                            price_list.append(flat['price'])

                                        min_m2_value = min(m2_list)
                                        min_price_value = min(price_list)

                                        flats[0] = {}
                                        flats[0]['min_m2_value'] = min_m2_value
                                        flats[0]['min_price_value'] = min_price_value

                                response_data = {'data': full_buildings_info}

            return response_data

        @__connect_and_exit
        def operate_table_data_simpled(
                request: Request,
                table_name: str,
                type_of_operation: str):
            response_data = {}
            if table_name == 'ListOfBuildings':
                if type_of_operation.lower() == 'get':
                    buildings = DataBaseOperations.get.buildings.by_range_id(
                        int(request.json['data']['response_length']), 'index')
                    images = DataBaseOperations.get.images.by_type('building')
                    for building in buildings:
                        for image in images:
                            if building['id'] == image['group_id']:
                                building['type'] = image['type']
                                building['group_id_for_image'] = image['group_id']
                                building['file_name'] = image['file_name']
                                break
                    response_data = {'data': buildings}
            return response_data


class DataBaseOperations:
    class get:
        class builders:
            def counted() -> int:
                return ListOfBuilders.select().count()

            def by_range_id(
                    id_range: int,
                    page_context: str = '',
                    language: str | None = None) -> list:
                """ Получение информации о застройщиках от 1 id до id_range id

                id_range: максимальный id выдаваемых застройщиков

                page context: позволяет определить объем выдаваемых ответов для оптимизации ответа на основе страницы, для который данные выдаются
                """
                builders = []
                if page_context == 'index':
                    for element in ListOfBuilders.select().where(
                            ListOfBuilders.id <= int(id_range) + 1):
                        builders.append(
                            {'id': element.id, 'name': element.name})
                else:
                    for element in ListOfBuilders.select().where(
                            ListOfBuilders.id <= int(id_range)):
                        builders.append(
                            {
                                'id': element.id,
                                'name': element.name,
                                'info': element.info if language in [
                                    None,
                                    'EN'] else element.info__lang_hebrew if language == 'HE' else None,
                                'foundation_year': element.foundation_year,
                                'completed_projects': element.completed_projects,
                                'projects_in_process': element.projects_in_process,
                                'trusted': element.trusted,
                            })
                return builders

            def by_id(builder_id: int, language: str | None = None) -> dict:
                """ Получение информации о застройщике по его id """
                for element in ListOfBuilders.select().where(ListOfBuilders.id == builder_id):
                    return {
                        'id': element.id,
                        'name': element.name,
                        'info': element.info if language in [
                            None,
                            'EN'] else element.info__lang_hebrew if language == 'HE' else None,
                        'foundation_year': element.foundation_year,
                        'completed_projects': element.completed_projects,
                        'projects_in_process': element.projects_in_process,
                        'trusted': element.trusted,
                    }

        class buildings:
            def counted() -> int:
                """ Нахождение количества """
                return ListOfBuildings.select().count()

            def find__price__min(values: list) -> int:
                """ Нахождение минимального целочисленного элемента по указанному списку ЖК ------------  """
                return fl.range_filter(values, 'min')

            def find__price__max(values: list) -> int:
                """ Нахождение максимального цедочисленного элемента по указанному списку ЖК ------------ """
                return fl.range_filter(values, 'max')

            def by_range_id(
                    id_range: int,
                    page_context: str = '',
                    language: str | None = None) -> list:
                """ Получение информации о ЖК от 1 id до id_range id

                id_range: максимальный id выдаваемых ЖК

                page context: позволяет определить объем выдаваемых ответов для оптимизации ответа на основе страницы, для который данные выдаются
                """
                buildings = []
                i = 0

                if page_context == 'index':
                    for element in ListOfBuildings.select():
                        if i >= id_range:
                            break
                        buildings.append(
                            {
                                'id': element.id,
                                'name': element.name,
                                'country': element.country if language in [
                                    None,
                                    'EN'] else element.country__lang_hebrew if language == 'HE' else None,
                                'city': element.city if language in [
                                    None,
                                    'EN'] else element.city__lang_hebrew if language == 'HE' else None})
                        i += 1
                else:
                    for element in ListOfBuildings.select():
                        if i >= id_range:
                            break
                        buildings.append(
                            {
                                'id': element.id,
                                'group_id': element.group_id,
                                'name': element.name,
                                'country': element.country if language in [
                                    None,
                                    'EN'] else element.country__lang_hebrew if language == 'HE' else None,
                                'city': element.city if language in [
                                    None,
                                    'EN'] else element.city__lang_hebrew if language == 'HE' else None,
                                'address': element.address if language in [
                                    None,
                                    'EN'] else element.address__lang_hebrew if language == 'HE' else None,
                                'parking': element.parking,
                                'type_of_building': element.type_of_building,
                            })
                        i += 1
                return buildings

            def by_id(building_id: int, language: str | None = None) -> dict:
                """ Получение информации о ЖК по его id """
                for element in ListOfBuildings.select().where(
                        ListOfBuildings.id == building_id):
                    return {
                        'id': element.id,
                        'group_id': element.group_id,
                        'name': element.name,
                        'country': element.country if language in [
                            None,
                            'EN'] else element.country__lang_hebrew if language == 'HE' else None,
                        'city': element.city if language in [
                            None,
                            'EN'] else element.city__lang_hebrew if language == 'HE' else None,
                        'address': element.address if language in [
                            None,
                            'EN'] else element.address__lang_hebrew if language == 'HE' else None,
                        'parking': element.parking,
                        'type_of_building': element.type_of_building,
                        'coord_x': element.coord_x,
                        'coord_y': element.coord_y,
                    }

            def filtered(filters: dict, language: str | None = None):
                """ Получение информации о ЖК, отфильтрованной по предоставленным ключам """
                raw_buildings = fl.simple_filter(ListOfBuildings, filters)
                buildings = []
                for building in raw_buildings:
                    buildings.append(
                        {
                            'id': building.id,
                            'group_id': building.group_id,
                            'name': building.name,
                            'country': building.country if language in [
                                None,
                                'EN'] else building.country__lang_hebrew if language == 'HE' else None,
                            'city': building.city if language in [
                                None,
                                'EN'] else building.city__lang_hebrew if language == 'HE' else None,
                            'address': building.address if language in [
                                None,
                                'EN'] else building.address__lang_hebrew if language == 'HE' else None,
                            'parking': building.parking,
                            'type_of_building': building.type_of_building,
                            'coord_x': building.coord_x,
                            'coord_y': building.coord_y,
                        })
                return buildings

            class merged:
                """ Получение информации о ЖК, совмещенной с информацией из других таблиц """
                def by_id__flats__grouped(
                        builder_id: int, language: str | None = None):
                    """ Получение информации о ЖК по их групповому id, при этом добавление к этим данным сгрупированной информации о квартирах в этих ЖК """
                    buildings = []
                    buildings_ids = []
                    more_buildings_button_off = True
                    i = 0
                    for element in ListOfBuildings.select().where(
                            ListOfBuildings.group_id == builder_id):
                        i += 1
                        if i == 4:
                            more_buildings_button_off = False
                            break

                        buildings.append(
                            {
                                'id': element.id,
                                'group_id': element.group_id,
                                'name': element.name,
                                'country': element.country if language in [
                                    None,
                                    'EN'] else element.country__lang_hebrew if language == 'HE' else None,
                                'city': element.city if language in [
                                    None,
                                    'EN'] else element.city__lang_hebrew if language == 'HE' else None,
                                'address': element.address if language in [
                                    None,
                                    'EN'] else element.address__lang_hebrew if language == 'HE' else None,
                                'parking': element.parking,
                                'type_of_building': element.type_of_building,
                            })
                        buildings_ids.append(element.id)

                        flats = []
                        for element in ListOfFlats.select().where(ListOfFlats.group_id == element.id):
                            flats.append({'id': element.id,
                                          'group_id': element.group_id,
                                          'price': element.price,
                                          'rooms': element.rooms,
                                          'floor': element.floor,
                                          'all_size_m2': element.all_size_m2,
                                          'kitchen_size_m2': element.kitchen_size_m2,
                                          'bathroom_size_m2': element.bathroom_size_m2,
                                          'hall_size_m2': element.hall_size_m2,
                                          'inside_size_m2': element.inside_size_m2,
                                          })

                        buildings[i - 1]['grouped_flats'] = {}
                        current_rooms = 0
                        max_rooms = 10  # ЗАМЕНИТЬ ЭТО 100%?
                        for j in range(max_rooms):
                            for flat_id in range(len(flats)):
                                if flats[flat_id]['rooms'] == current_rooms:
                                    try:
                                        buildings[i - 1]['grouped_flats'][current_rooms].append(
                                            flats[flat_id])
                                    except KeyError:
                                        buildings[i -
                                                  1]['grouped_flats'][current_rooms] = [flats[flat_id]]
                                    # del flats[flat_id] # ?
                            current_rooms += 1
                    return buildings, more_buildings_button_off

                def flats(language: str | None = None):
                    """ Получение информации о всех ЖК, при этом добавление к этим данным не сгрупированной информации о квартирах в этих ЖК """
                    buildings = []
                    buildings_ids = []
                    i = 0
                    for element in ListOfBuildings.select():
                        i += 1
                        buildings.append(
                            {
                                'id': element.id,
                                'group_id': element.group_id,
                                'name': element.name,
                                'country': element.country if language in [
                                    None,
                                    'EN'] else element.country__lang_hebrew if language == 'HE' else None,
                                'city': element.city if language in [
                                    None,
                                    'EN'] else element.city__lang_hebrew if language == 'HE' else None,
                                'address': element.address if language in [
                                    None,
                                    'EN'] else element.address__lang_hebrew if language == 'HE' else None,
                                'parking': element.parking,
                                'type_of_building': element.type_of_building,
                            })
                        buildings_ids.append(element.id)
                        flats = []
                        for element in ListOfFlats.select().where(ListOfFlats.group_id == element.id):
                            flats.append({'id': element.id,
                                          'group_id': element.group_id,
                                          'price': element.price,
                                          'rooms': element.rooms,
                                          'floor': element.floor,
                                          'price_per_m2': element.price_per_m2,
                                          'all_size_m2': element.all_size_m2,
                                          'kitchen_size_m2': element.kitchen_size_m2,
                                          'bathroom_size_m2': element.bathroom_size_m2,
                                          'hall_size_m2': element.hall_size_m2,
                                          'inside_size_m2': element.inside_size_m2,
                                          })
                        buildings[i - 1]['flats'] = flats
                    return buildings

        class flats:
            def counted() -> int:
                return ListOfFlats.select().count()

            def by_group_id(
                    building_id: int,
                    language: str | None = None) -> list:
                """ Получение информации о квартирах по их групповому id """
                flats = []
                for element in ListOfFlats.select().where(ListOfFlats.group_id == building_id):
                    flats.append({'id': element.id,
                                  'group_id': element.group_id,
                                  'price': element.price,
                                  'rooms': element.rooms,
                                  'floor': element.floor,
                                  'all_size_m2': element.all_size_m2,
                                  'kitchen_size_m2': element.kitchen_size_m2,
                                  'bathroom_size_m2': element.bathroom_size_m2,
                                  'hall_size_m2': element.hall_size_m2,
                                  'inside_size_m2': element.inside_size_m2,
                                  })
                return flats

            def by_id(flat_id: int, language: str | None = None) -> dict:
                """ Получение информации о квартире по ее id """
                for element in ListOfFlats.select().where(ListOfFlats.id == flat_id):
                    return {
                        'id': element.id,
                        'group_id': element.group_id,
                        'price': element.price,
                        'rooms': element.rooms,
                        'floor': element.floor,
                        'all_size_m2': element.all_size_m2,
                        'kitchen_size_m2': element.kitchen_size_m2,
                        'bathroom_size_m2': element.bathroom_size_m2,
                        'hall_size_m2': element.hall_size_m2,
                        'inside_size_m2': element.inside_size_m2,
                    }

            def filtered(filters: dict, language: str | None = None):
                """ Получение информации о квартирах, отфильтрованной по предоставленным ключам """
                raw_flats = fl.simple_filter(ListOfFlats, filters)
                flats = []
                for flat in raw_flats:
                    flats.append({'id': flat.id,
                                  'group_id': flat.group_id,
                                  'price': flat.price,
                                  'rooms': flat.rooms,
                                  'floor': flat.floor,
                                  'all_size_m2': flat.all_size_m2,
                                  'kitchen_size_m2': flat.kitchen_size_m2,
                                  'bathroom_size_m2': flat.bathroom_size_m2,
                                  'hall_size_m2': flat.hall_size_m2,
                                  'inside_size_m2': flat.inside_size_m2,
                                  })
                return flats

        class images:
            def counted() -> int:
                return ListOfImages.select().count()

            def by_type(images_type: str) -> list:
                """ Получение информации об изображениях на основе типа """
                logos = []
                for element in ListOfImages.select().where(ListOfImages.type == images_type):
                    logos.append({'type': element.type,
                                  'group_id': element.group_id,
                                  'file_name': element.file_name,
                                  })
                return logos

        class users:
            def state_by_login_and_password__sha256(
                    login: str, password: str) -> bool:
                """ Авторизация клиента """
                # Синхронизация с БД, сохранение печенек и сессии если все
                # хорошо и вывод предупреждения о неправильных данных, если что
                # то не так
                for user in ListOfUsers.select().where(
                    ListOfUsers.login == login and ListOfUsers.password == sha256(
                        password.encode()).hexdigest()):
                    return True
                return False

            def role_group_by_login_and_password__sha256(
                    login: str, password: str) -> str:
                """ Сохранение роли клиента """
                for user in ListOfUsers.select().where(
                    ListOfUsers.login == login and ListOfUsers.password == sha256(
                        password.encode()).hexdigest()):
                    return user.role

    class post:
        def builders(id: int, name: str, info: str, foundation_year: int,
                     completed_projects: int, projects_in_process: int,
                     trusted: bool, images: int, info__lang_hebrew: str):
            row = ListOfBuilders(
                name=name,
                info=info,
                foundation_year=foundation_year,
                completed_projects=completed_projects,
                projects_in_process=projects_in_process,
                trusted=True,
                info__lang_hebrew=info__lang_hebrew)
            row.save()
            for image in images.split(';'):
                row = ListOfImages(
                    type='builder', group_id=id, file_name=image)
                row.save()
            return {
                'state': 'True',
                'info': 'Added new builder in ListOfBuilders'}

        def buildings(
                id: int,
                group_id: int,
                name: str,
                city: str,
                country: str,
                address: str,
                parking: int,
                price_per_m2: int,
                type_of_building: str,
                coord_x: float,
                coord_y: float,
                info: str,
                images: int,
                city__lang_hebrew: str,
                country__lang_hebrew,
                address__lang_hebrew: str,
                info__lang_hebrew: str):
            row = ListOfBuildings(
                group_id=int(group_id),
                name=name,
                info=info,
                country=country,
                city=city,
                address=address,
                parking=parking,
                type_of_building=type_of_building,
                coord_x=float(coord_x),
                coord_y=float(coord_y),
                info__lang_hebrew=info__lang_hebrew,
                city__lang_hebrew=city__lang_hebrew,
                address__lang_hebrew=address__lang_hebrew,
                country__lang_hebrew=country__lang_hebrew)
            row.save()
            for image in images.split(';'):
                row = ListOfImages(
                    type='building', group_id=id, file_name=image)
                row.save()
            return {
                'state': 'True',
                'info': 'Added new building in ListOfBuildings'}

        def flats(
                id: int,
                group_id: int,
                price: int,
                price_per_m2: int,
                rooms: int,
                floor: int,
                all_size_m2: int,
                kitchen_size_m2: int,
                bathroom_size_m2: int,
                hall_size_m2: int,
                inside_size_m2: int,
                images: int):
            row = ListOfFlats(
                group_id=group_id,
                info='-',
                price=price,
                price_per_m2=price_per_m2,
                rooms=rooms,
                floor=floor,
                all_size_m2=all_size_m2,
                kitchen_size_m2=kitchen_size_m2,
                bathroom_size_m2=bathroom_size_m2,
                hall_size_m2=hall_size_m2,
                inside_size_m2=inside_size_m2,
                info__lang_hebrew='')
            row.save()
            for image in images.split(';'):
                row = ListOfImages(type='flat', group_id=id, file_name=image)
                row.save()
            return {'state': 'True', 'info': 'Added new flat in ListOfFlats'}

        def users(login: str, password: str) -> dict:
            """ Регистрация """
            if ListOfUsers.get_or_none(ListOfUsers.login == login) is None:
                row = ListOfUsers(
                    login=login, password=sha256(
                        password.encode()).hexdigest())
                row.save()
                return {
                    'state': 'True',
                    'info': 'User {} was successfully registered!'.format(login)}
            return {
                'state': 'False',
                'info': 'User {} already exists!'.format(login)}
