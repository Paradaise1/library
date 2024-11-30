import json
import os
import sys

from typing import Dict


# Все доступные команды
COMMANDS = [
    'add book - добавление книги по названию автору и году.',
    'delete book - удаление книги по id.',
    'find book - поиск книги по id.',
    'show books - отображение списка всех доступных книг.',
    'change status - изменение статука скини по id.',
    'help - список всех доступных команд.',
    'exit - завершение работы программы.'
]

# Все доступные статусы
STATUSES = {0: 'в наличии', 1: 'выдана'}
# Название локальной библиотеки
DATA_FILENAME = 'data.json'


class LibraryManager():
    '''Класс для работы с библиотекой.'''
    FILENAME = DATA_FILENAME
    def print_book(self, book: Dict) -> None:
        '''Вспомогательный метод для вывода конкретной книги.'''
        for key, value in book.items():
            print(f'{key} - {value};')

    def validate(self, val: str, message: str) -> None:
        '''Вспомогательный метод для валидации данных.'''
        try:
            val = int(val)
        except TypeError:
            print(f'{message} должен быть целым числом.')
        return val

    def add_book(self) -> None:
        '''Метод для добавление книги в библиотеку.'''
        # Запрашиваем данные книги
        try:
            title, author, year = input(
                'Введите название, автора и год выпуска книги через пробел: '
            ).split()
        except ValueError:
            print('Неверное количество аргументов.')
            return
        year = self.validate(year, 'Год выпуска')
        # Читаем файл, создаем и добавлем книгу, перезаписываем файл
        with open(self.FILENAME, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            if data:
                current_id = data[-1]['id'] + 1
            else:
                current_id = 1
            book = {
                'id': current_id,
                'title': title,
                'author': author,
                'year': year,
                'status': STATUSES[0]
            }
            data.append(book)
            f.seek(0)
            json.dump(data, f, indent=4, ensure_ascii=False)
        print('Книга успешно добавлена!')

    def find_book(self, flag: bool = True) -> int | None:
        '''Метод для поиска книги по id.'''
        # Запрашиваем id книги
        current_id = input('Введите id книги, которую хотите найти: ')
        current_id = self.validate(current_id, 'Индентификатор')
        # Открваем файл, ищем книгу, если нашли - возвращаем ее index
        # Иначе - None
        with open(self.FILENAME, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if data:
                for i, book in enumerate(data):
                    if book['id'] == current_id:
                        if flag:
                            self.print_book(book)
                        return i
            print('Такой книги не существует.')
            return

    def delete_book(self) -> None:
        '''Метод для удаления книги по id.'''
        # Находим книгу уже существующим методом
        current_id = self.find_book(flag=False)
        if current_id is None:
            return
        # Открваем файл, удаляем книгу
        with open(self.FILENAME, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            data.pop(current_id)
            f.seek(0)
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.truncate()
        print('Книга успешно удалена!')

    def show_books(self) -> None:
        '''Метод для вывода информации о всех книгах в библиотеке.'''
        # Открваем файл, читаем информацию, выводим ее
        with open(self.FILENAME, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if data:
            for book in data:
                self.print_book(book)
                print()
        else:
            print('Книг нет.')

    def change_status(self) -> None:
        '''Метод для изменения статуса конкретной книги.'''
        # Находим книгу уже существующим методом
        current_id = self.find_book(flag=False)
        if current_id is None:
            return
        # Запрашиваем новый статус
        statuses = ', '.join([status for status in STATUSES.values()])
        new_status = input(
            'Введите новый статус '
            f'(доступные статусы - {statuses}): ')
        if new_status not in STATUSES.values():
            print('Неверный статус.')
            return
        # Читаем файл, меняем статус, перезаписываем файл
        with open(self.FILENAME, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            data[current_id]['status'] = new_status
            f.seek(0)
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.truncate()
        print('Статус успешно изменен!')


class CommandsManager():
    '''Класс для управления командами,
    не относящимися к работе с библиотекой.'''
    def helping(self) -> None:
        '''Команда для вывода списка всех доступных команд.'''
        print('Все доступные команды:')
        for cmd in COMMANDS:
            print(cmd)

    def exiting(self) -> None:
        '''Команда для выхода из бесконечного цикла.'''
        print('Выход...')
        sys.exit()


def main() -> None:
    '''Основная логика программы.'''
    # Инициализируем все необходимое для работы программы
    if not os.path.exists(DATA_FILENAME):
        with open(DATA_FILENAME, 'w') as f:
            json.dump([], f)

    lm = LibraryManager()
    cm = CommandsManager()
    commands = {
        'add book': lm.add_book,
        'delete book': lm.delete_book,
        'find book': lm.find_book,
        'show books': lm.show_books,
        'change status': lm.change_status,
        'help': cm.helping,
        'exit': cm.exiting
    }

    # Выводим приветсвие
    print('Привет пользователь! Данное консольное приложение '
          'разработано для управления '
          'локальной библиотекой на твоем компьютере.')
    cm.helping()

    # Запрашиваем команды, пока пользователь не введет exit
    while True:
        cmd = input('Введите команду: ')
        try:
            commands[cmd]()
        except KeyError:
            print('Такой команды не существует. '
                  'Попробуйте help для просмотра всех доступных команд.')


if __name__ == '__main__':
    main()
