import json
import os
import pytest


@pytest.fixture(scope='session', autouse=True)
def create_json_file():
    '''Фикстура для создания json файла.'''
    if not os.path.exists('data.json'):
        with open('data.json', 'w') as f:
            json.dump([], f)
    yield
    os.remove('data.json')


@pytest.fixture()
def create_statuses():
    '''Фикстура для создания доступных статусов.'''
    return {0: 'в наличии', 1: 'выдана'}
