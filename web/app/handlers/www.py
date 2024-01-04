from flask import Flask, request, render_template, redirect, session, make_response, abort
from app.scripts.requests import Requests
from app.scripts.helpers import get_locale, Playground
import json


def handle_www(application: Flask, logger, redis_worker):
    """ Обработка запросов WWW """

    @application.route('/', methods=['GET'])
    @redis_worker.save_view
    def index():
        """

            Index page
        """
        logger.info('/')
        language = request.cookies.get('__lang')
        builders, buildings, length_of_all_buildings = Requests.index(language)
        range_buildings_values = redis_worker.get(
            ['buildings_min', 'buildings_max'])

        response = Playground(
            request,
            make_response(
                render_template(
                    'index.html',
                    data={
                        'session': session,
                        'builders': builders,
                        'buildings': buildings,
                        'length_of_all_buildings': length_of_all_buildings,
                        'range_buildings_values': range_buildings_values,
                        'locale': get_locale(language)}))).set(
                    is_cookie=True,
            is_http=True)

        return response

    @application.route('/builder', methods=['GET'])
    @redis_worker.save_view
    def builder():
        """

            Builder page
        """
        builder_id = request.args.get('builder_id')
        if builder_id is None:
            logger.info('/builder -> error.html')
            abort(404)
        language = request.cookies.get('__lang')
        logger.info(f'/builder?builder_id={builder_id}')
        builders, slides_buildings, more_buildings_button_off = Requests.builder(
            builder_id, language)

        response = Playground(
            request,
            make_response(
                render_template(
                    'builder.html',
                    data={
                        'session': session,
                        'builders': builders,
                        'slides_buildings': slides_buildings,
                        'more_buildings_button_off': more_buildings_button_off,
                        'locale': get_locale(language)}))).set(
                    is_cookie=True,
            is_http=True)

        return response

    @application.route('/building', methods=['GET'])
    @redis_worker.save_view
    def building():
        """

            Building page
        """
        building_id = request.args.get('building_id')
        language = request.cookies.get('__lang')

        if building_id is None:
            logger.info('/building -> error.html')
            abort(404)
        logger.info(f'/building?building_id={building_id}')
        building, building_images, flats, builder, simular_buildings, grouped_flats = Requests.building(
            building_id, language)

        response = Playground(
            request,
            make_response(
                render_template(
                    'building.html',
                    data={
                        'session': session,
                        'building': building,
                        'building_images': building_images,
                        'flats': flats,
                        'builder': builder,
                        'simular_buildings': simular_buildings,
                        'grouped_flats': grouped_flats,
                        'locale': get_locale(language)}))).set(
                    is_cookie=True,
            is_http=True)

        return response

    @application.route('/flat', methods=['GET'])
    @redis_worker.save_view
    def flat():
        """

            Flat page
        """
        flat_id = request.args.get('flat_id')
        language = request.cookies.get('__lang')
        if flat_id is None:
            logger.info('/flat -> error.html')
            abort(404)
        logger.info(f'/flat?flat_id={flat_id}')
        flat, flat_images, building, builder, grouped_another_flats = Requests.flat(
            flat_id, language)

        response = Playground(
            request,
            make_response(
                render_template(
                    'flat.html',
                    data={
                        'session': session,
                        'flat': flat,
                        'flat_images': flat_images,
                        'building': building,
                        'builder': builder,
                        'grouped_another_flats': grouped_another_flats,
                        'locale': get_locale(language)}))).set(
                    is_cookie=True,
            is_http=True)

        return response

    @application.route('/map', methods=['GET'])
    @redis_worker.save_view
    def map():
        map_filters = request.args.get('filters')
        range_buildings_values = redis_worker.get(
            ['buildings_min', 'buildings_max'])
        language = request.cookies.get('__lang')

        if map_filters is None or map_filters == {}:
            logger.info('/map')

            response = Playground(
                request,
                make_response(
                    render_template(
                        'map.html',
                        data={
                            'session': session,
                            'range_buildings_values': range_buildings_values,
                            'locale': get_locale(language)}))).set(
                is_cookie=True,
                is_http=True)

            return response
        else:
            logger.info(f'/map?filters={map_filters}')
            filters_output = Requests.API.operate_table_data_filtered(
                request=request, table_name='ListOfBuildings', type_of_operation='get')

            if 'filters' in json.loads(map_filters).keys():
                response = Playground(
                    request,
                    make_response(
                        render_template(
                            'map.html',
                            data={
                                'session': session,
                                'filters_output': filters_output,
                                'filters': json.loads(map_filters)['filters'],
                                'range_buildings_values': range_buildings_values,
                                'locale': get_locale(language)}))).set(
                    is_cookie=True,
                    is_http=True)

                return response
            else:
                response = Playground(
                    request,
                    make_response(
                        render_template(
                            'map.html',
                            data={
                                'session': session,
                                'filters_output': filters_output,
                                'filters': {},
                                'range_buildings_values': range_buildings_values,
                                'locale': get_locale(language)}))).set(
                    is_cookie=True,
                    is_http=True)

                return response

    @application.route('/about_us', methods=['GET'])
    @redis_worker.save_view
    def about_us():
        logger.info('/about_us')
        language = request.cookies.get('__lang')
        response = Playground(
            request,
            make_response(
                render_template(
                    'about_us.html',
                    data={
                        'session': session,
                        'locale': get_locale(language)}))).set(
                    is_cookie=True,
            is_http=True)

        return response

    @application.route('/index', methods=['GET'])
    @application.route('/home', methods=['GET'])
    @application.route('/start', methods=['GET'])
    def index_redirect():
        return redirect('/')
