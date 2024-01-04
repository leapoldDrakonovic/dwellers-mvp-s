from flask import session


class BaseRule:
    @staticmethod
    def check_rule(__rule) -> bool:
        return __rule()


class AuthenticationRule(BaseRule):
    def __is_auth() -> bool:
        if 'user' in session.keys() and 'user_role' in session.keys():
            if session['user_role'] == 'admin':
                return True
        return False

    def check_rule() -> bool:
        """ Проверка на то, является ли запрашиваемая ресурс сторона админом """
        return BaseRule.check_rule(AuthenticationRule.__is_auth)
