import requests

class WhoID:
    def __init__(self, token):
        self.token: str = token

    def check_user(self, mail, password):
        try:
            response = requests.get(
                f'https://whoid.ru/api/get?token={self.token}&mail={mail}&password={password}'
            ).json()
            return response
        except Exception as e:
            return e

    def check_fio(self, fio):
        try:
            response = requests.get(
                f'https://whoid.ru/api/fio?token={self.token}&name={fio}'
            ).json()
            return response
        except Exception as e:
            return e