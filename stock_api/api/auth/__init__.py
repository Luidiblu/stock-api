from stock_api.config import AUTH_API_URL
import requests
import traceback
from werkzeug.exceptions import Unauthorized, InternalServerError, Forbidden
import sentry_sdk


class AuthHelper(object):

    @staticmethod
    def get_user_by_token(token):
        headers = {'Authorization': f'Token {token}'}
        url = f'{AUTH_API_URL}/api/user'
        try:
            resp = requests.get(url, headers=headers)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            traceback.print_exc()
            print(f'Erro ao realizar GET {AUTH_API_URL}')

        if resp.status_code != 200:
            raise Forbidden('Invalid Token')

        return resp.json().get('user')

    @staticmethod
    def validate_permissions(token, required_permission):
        user = AuthHelper.get_user_by_token(token)

        if required_permission not in user['permissions']:
            raise Unauthorized('User does not have the required permission')

        return user

    @staticmethod
    def user_is_cleared(token: str, clearance: str) -> bool:
        headers = {'Authorization': f'Token {token}'}
        payload = {
            'clearance': clearance
        }
        url = f'{AUTH_API_URL}/api/clearance'
        try:
            resp = requests.post(url, headers=headers, json=payload)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            traceback.print_exc()
            print(f'Erro ao realizar POST {AUTH_API_URL}')

        if resp.status_code != 401:
            return True

        return False

    @staticmethod
    def cleared_objects_list(token: str, clearance: str) -> [str]:
        headers = {'Authorization': f'Token {token}'}
        payload = {
            'clearance': clearance
        }
        url = f'{AUTH_API_URL}/api/clearedIds'
        try:
            resp = requests.post(url, headers=headers, json=payload)
            if resp.status_code != 200:
                return []
            return resp.json()
        except Exception as e:
            sentry_sdk.capture_exception(e)
            traceback.print_exc()
            print(f'Erro ao realizar POST {AUTH_API_URL}')
            raise InternalServerError('Failed to reach Auth Service. Try again in a few seconds')

    @staticmethod
    def read_token(args: dict):
        return args.get('Authorization', '').replace('Token ', '')
