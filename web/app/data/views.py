from flask import Flask, url_for, render_template
from flask_admin import BaseView, expose, AdminIndexView
from flask_admin.contrib.peewee import ModelView
from flask_admin.contrib.rediscli import RedisCli
from app.data.rules import AuthenticationRule


class AuthAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return AuthenticationRule.check_rule()

    def inaccessible_callback(self, name, **kwargs):
        return render_template(
            'error.html', data={
                'status_code': 403, 'status_text': 'Forbidden'}), 403


class AuthBaseView(BaseView):
    def is_accessible(self):
        return AuthenticationRule.check_rule()

    def inaccessible_callback(self, name, **kwargs):
        return render_template(
            'error.html', data={
                'status_code': 403, 'status_text': 'Forbidden'}), 403


class AuthModelView(ModelView):
    def is_accessible(self):
        return AuthenticationRule.check_rule()

    def inaccessible_callback(self, name, **kwargs):
        return render_template(
            'error.html', data={
                'status_code': 403, 'status_text': 'Forbidden'}), 403


class AuthRedisCli(RedisCli):
    def is_accessible(self):
        return AuthenticationRule.check_rule()

    def inaccessible_callback(self, name, **kwargs):
        return render_template(
            'error.html', data={
                'status_code': 403, 'status_text': 'Forbidden'}), 403


class ImagesView(AuthBaseView):
    @expose('/')
    def images(self):
        return self.render('admin/images.html')


class EndpointsView(AuthBaseView):
    application: Flask

    def get_app(application: Flask) -> None:
        EndpointsView.application = application

    def _has_no_empty_params(rule) -> bool:
        defaults = rule.defaults if rule.defaults is not None else ()
        arguments = rule.arguments if rule.arguments is not None else ()
        return len(defaults) >= len(arguments)

    def _get_routes() -> list:
        links = []
        for rule in EndpointsView.application.url_map.iter_rules():
            if "GET" in rule.methods and EndpointsView._has_no_empty_params(
                    rule):
                url = url_for(rule.endpoint, **(rule.defaults or {}))
                links.append((url, rule.endpoint))
        return links

    @expose('/')
    def endpoints(self):
        return self.render('admin/endpoints.html',
                           data={'endpoints': EndpointsView._get_routes()})


class SQLScriptsView(AuthBaseView):
    @expose('/')
    def sql_scripts(self):
        return self.render('admin/sql_scripts.html')


class SQLExecuteView(AuthBaseView):
    @expose('/')
    def sql_execute(self):
        return self.render('admin/sql_execute.html')
