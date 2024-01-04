from flask import Flask, make_response, render_template


def handle_errors(application: Flask):
    """ Обработка ошибок """
    @application.errorhandler(404)
    def handler_404(error):
        response = make_response(
            render_template(
                'error.html',
                data={
                    'status_code': 404,
                    'status_text': 'Not Found'}))
        response.status_code = 404
        return response

    @application.errorhandler(400)
    def handler_400(error):
        response = make_response(
            render_template(
                'error.html',
                data={
                    'status_code': 400,
                    'status_text': 'Bad Request'}))
        response.status_code = 400
        return response

    @application.errorhandler(500)
    def handler_500(error):
        response = make_response(
            render_template(
                'error.html',
                data={
                    'status_code': 500,
                    'status_text': 'Internal Server Error'}))
        response.status_code = 500
        return response

    @application.errorhandler(403)
    def handler_403(error):
        response = make_response(
            render_template(
                'error.html',
                data={
                    'status_code': 403,
                    'status_text': 'Forbidden'}))
        response.status_code = 403
        return response
