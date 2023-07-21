# Курсовая 5. Работа с базами данных


## Реализовано:

- Получены данные о работодателях и их вакансиях с сайта [hh.ru](http://hh.ru/) через публичный API [hh.ru](http://hh.ru/) и библиотеку `requests`.
- Выбраны 10 компаний, от которых получены данные о вакансиях по API.
- Созданы таблицы в БД north (Postgres) для хранения полученных данных о работодателях и их вакансиях.
- Реализован код, который заполняет созданные таблицы данными о работодателях и их вакансиях и выводит их пользователю.
- Создан интерактивный пользовательский интерфейс для удобной работы с данными в БД.

## В классе DBManager есть следующие методы:

- `get_companies_and_vacancies_count()`: получает список всех компаний и количество вакансий у каждой компании.
- `get_all_vacancies()`: получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
- `get_avg_salary()`: получает среднюю зарплату по вакансиям.
- `get_vacancies_with_higher_salary()`: получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
- `get_vacancies_with_keyword()`: получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”.

## Настройка и запуск проекта 

Для настройки взаимодействия и корректной работы кода необходимо выполнить:
* в файле postgres_db.py импортируем модули psycopg2, sql и requests
* в файле config.py импортируем модуль configparser, импорт выполняем средствами Pycharm
* в файле postgres_db.py пользователь указывает свой User-Agent (из личного кабинета на hh.ru)
* на основе файла database.ini.example пользователь создает файл database.ini и указывает в нем db_name (своей базы) и db_password свой пароль для доступа к БД Postgres)
* запускаем Python-модуль main.py 
* после запуска код реализует получение информации с АПИ hh.ru, создание таблиц, запись данных в таблицы, чтение из таблиц и обработку согласно ТЗ
* пользователю выводится информация из таблиц согласно реализованным методам и для наглядности при изучении информации предлагается выбрать одно из несколько действий:

1. Получить список всех компаний и количество вакансий у каждой компании
2. Получить список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию
3. Получить среднюю зарплату по вакансиям
4. Получить список всех вакансий с зарплатой выше средней
5. Получить список всех вакансий, в названии которых содержится определенное слово
0. Выйти из программы

## SQL-запросы для портала хранятся в файле queries.sql