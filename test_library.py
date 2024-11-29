import json

from main import LibraryManager


class TestLibraryManager():
    '''Класс для тестирования функционала класса LibraryManager.'''
    # Создаем эксземпляер тестируемого класса
    lm = LibraryManager()

    def test_add_book(self, monkeypatch, create_statuses):
        '''Тест создания книги.'''
        STATUSES = create_statuses
        monkeypatch.setattr(
            'builtins.input', lambda _: 'test_title test_author 2000'
        )
        self.lm.add_book()
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert len(data) == 1
        assert data[0]['id'] == 1
        assert data[0]['title'] == 'test_title'
        assert data[0]['author'] == 'test_author'
        assert data[0]['year'] == 2000
        assert data[0]['status'] == STATUSES[0]

    def test_find_book(self, monkeypatch):
        '''Тест поиска книги по id.'''
        monkeypatch.setattr('builtins.input', lambda _: '1')
        index = self.lm.find_book()
        assert index == 0

    def test_change_to_invalid_status(self, monkeypatch):
        '''Тест изменения статуса книги на неверный статус.'''
        inputs = iter(['1', 'invalid_status'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        self.lm.change_status()
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert data[0]['status'] == 'в наличии'

    def test_change_to_valid_status(self, monkeypatch):
        '''Тест изменения статуса книги на доступный статус.'''
        inputs = iter(['1', 'выдана'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        self.lm.change_status()
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert data[0]['status'] == 'выдана'

    def test_delete_book_with_invalid_args(self, monkeypatch):
        '''Тест удаления несуществующей книги.'''
        monkeypatch.setattr('builtins.input', lambda _: '100')
        self.lm.delete_book()
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert len(data) == 1

    def test_delete_book(self, monkeypatch):
        '''Тест удаления существующей книги.'''
        monkeypatch.setattr('builtins.input', lambda _: '1')
        self.lm.delete_book()
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert len(data) == 0

    def test_add_book_with_invalid_args(self, monkeypatch):
        '''Тест создания книги с невалидными аргументами.'''
        monkeypatch.setattr(
            'builtins.input', lambda _: 'test_title test_author string'
        )
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert len(data) == 0
