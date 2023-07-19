import psycopg2
from psycopg2 import sql

import requests


class DBManager:
    def __init__(self, params):
        self.connection = psycopg2.connect(
            host=params['db_host'],
            port=params['db_port'],
            database=params['db_name'],
            user=params['db_user'],
            password=params['db_password']
        )
        self.companies = []  # Объявляем переменную экземпляра 'companies' как список
        self.vacancies = []  # Объявляем переменную экземпляра 'vacancies' как список

    def create_tables(self):
        # Создание таблицы "companies" для хранения данных о компаниях
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS companies (
                   id_company SERIAL PRIMARY KEY,
                   title_company VARCHAR(255) UNIQUE NOT NULL,
                   number_vacancies INTEGER
               ); 
            """)

        # Создание таблицы "vacancies" для хранения данных о вакансиях
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                   vacancy_name TEXT,
                   id_company INTEGER REFERENCES companies(id_company),
                   title VARCHAR(255) UNIQUE,
                   salary NUMERIC(10, 2), 
                   link TEXT
                );
            """)

        self.connection.commit()

    def _get_companies_from_api(self, id_company):
        # Получение списка компаний с API hh.ru
        url_hh = f"https://api.hh.ru/employers/{id_company}"
        params = {'per_page': '100'}
        headers = {"User-Agent": "50355527"}  # User-Agent взят из личного кабинета hh.ru
        response = requests.get(url_hh, headers=headers, params=params)
        if response.status_code == 200:
            companies_data = response.json()
            companies_list = [companies_data] if isinstance(companies_data, dict) else companies_data
            # pprint.pprint(companies_list)
            return companies_list
        return []

    def _get_vacancies_from_api(self, id_company):
        # Получение списка вакансий с API hh.ru
        url_hh = f"https://api.hh.ru/vacancies"
        params = {'employer_id': id_company, 'per_page': '100'}
        headers = {"User-Agent": "6589757"}  # User-Agent из личного кабинета hh.ru
        response = requests.get(url_hh, headers=headers, params=params)
        if response.status_code == 200:
            vacancies_data = response.json()
            if 'items' in vacancies_data:
                # pprint.pprint(vacancies_data)
                return vacancies_data['items']
        return []

    def insert_companies_and_vacancies(self):
        # Получение данных о компаниях и вакансиях с API hh.ru
        try:
            self.companies = []  # Очищаем список компаний
            self.vacancies = []  # Очищаем список вакансий
            # Список id компаний, которые необходимо получить из API HH
            company_ids = ['3529', '3526', '3521', '78638', '64174', '64176', '64189', '64193', '64199', '64204']
            for id_company in company_ids:
                self.companies.extend(self._get_companies_from_api(id_company))
                self.vacancies.extend(self._get_vacancies_from_api(id_company))

            # Вставляем данные в таблицы о компаниях
            with self.connection.cursor() as cursor:
                for company in self.companies:
                    if not isinstance(company, dict):
                        print("Ошибка: Некорректный формат данных о компании:", company)
                        continue  # Пропускаем некорректные данные

                    company_name = company.get('name')
                    if not isinstance(company_name, str):
                        print("Ошибка: Некорректный формат имени компании:", company_name)
                        continue  # Пропускаем компанию с некорректным именем

                    vacancies_count = len(self._get_vacancies_from_api(company['id']))
                    print("Добавляем компанию:", company_name)
                    insert_company_query = sql.SQL(
                        "INSERT INTO companies (title_company, number_vacancies) "
                        "VALUES (%s, %s) "
                        "ON CONFLICT (title_company) DO UPDATE SET number_vacancies = EXCLUDED.number_vacancies")
                    try:
                        cursor.execute(insert_company_query, [company_name, vacancies_count])
                    except Exception as e:
                        print("Ошибка при добавлении компании", company_name)
                        print("Сообщение об ошибке:", str(e))
                        continue

            # Вставляем данные в таблицы о вакансиях
            with self.connection.cursor() as cursor:
                for vacancy in self.vacancies:
                    company_name = vacancy.get('employer', {}).get('name', '')
                    title = vacancy.get('name', '')
                    link = vacancy.get('alternate_url', '')
                    salary = vacancy.get('salary', {})
                    salary_from = salary.get('from') if salary is not None else 0

                    # Получаем id компании из таблицы companies
                    get_company_id_query = sql.SQL("SELECT id_company FROM companies WHERE title_company = %s")
                    cursor.execute(get_company_id_query, [company_name])
                    id_company = cursor.fetchone()

                    # Если компания существует, вставляем данные о вакансии с указанием id_company
                    if id_company is not None:
                        id_company = id_company[0]
                        insert_vacancy_query = sql.SQL(
                            "INSERT INTO vacancies (id_company, vacancy_name, title, salary, link) "
                            "VALUES (%s, %s, %s, %s, %s) "
                            "ON CONFLICT (title) DO UPDATE SET salary = EXCLUDED.salary"
                        )
                        try:
                            cursor.execute(insert_vacancy_query, [id_company, company_name, title, salary_from, link])

                        except Exception as e:
                            print("Ошибка при добавлении вакансии:")
                            print("Компания:", company_name)
                            print("Название:", title)
                            print("Зарплата:", salary_from)
                            print("Ссылка:", link)
                            print("Сообщение об ошибке:", str(e))

            # Если все прошло успешно, фиксируем транзакцию
            self.connection.commit()

        except Exception as e:
            # Если произошла ошибка, отменяем транзакцию
            self.connection.rollback()
            print("Ошибка транзакции. Транзакция отменена.")
            print("Сообщение об ошибке:", str(e))

    def get_companies_and_vacancies_count(self):
        # Получение списка всех компаний и количества вакансий у каждой компании
        with self.connection.cursor() as cursor:
            query = sql.SQL("SELECT companies.title_company, COUNT(vacancies.id_company) "
                            "FROM companies "
                            "LEFT JOIN vacancies ON companies.id_company = vacancies.id_company "
                            "GROUP BY companies.title_company")
            cursor.execute(query)
            result = cursor.fetchall()
        return result

    def get_all_vacancies(self):
        # Получение списка всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию
        with self.connection.cursor() as cursor:
            query = sql.SQL("SELECT companies.title_company, vacancies.title, vacancies.salary, vacancies.link "
                            "FROM vacancies "
                            "INNER JOIN companies ON vacancies.id_company = companies.id_company")
            cursor.execute(query)
            result = cursor.fetchall()
        return result

    def get_avg_salary(self):
        # Получение средней зарплаты по вакансиям
        with self.connection.cursor() as cursor:
            query = sql.SQL("SELECT AVG(salary) FROM vacancies")
            cursor.execute(query)
            result = cursor.fetchone()[0]
        return result

    def get_vacancies_with_higher_salary(self):
        # Получение списка всех вакансий, у которых зарплата выше средней по всем вакансиям
        avg_salary = self.get_avg_salary()

        with self.connection.cursor() as cursor:
            query = sql.SQL("SELECT companies.title_company, vacancies.title, vacancies.salary, vacancies.link "
                            "FROM vacancies "
                            "INNER JOIN companies ON vacancies.id_company = companies.id_company "
                            "WHERE vacancies.salary > %s")
            cursor.execute(query, [avg_salary])
            result = cursor.fetchall()
        return result

    def get_vacancies_with_keyword(self, keyword):
        # Получение списка всех вакансий, в названии которых содержится переданное в метод слово
        with self.connection.cursor() as cursor:
            query = sql.SQL("SELECT companies.title_company, vacancies.title, vacancies.salary, vacancies.link "
                            "FROM vacancies "
                            "INNER JOIN companies ON vacancies.id_company = companies.id_company "
                            "WHERE vacancies.title ILIKE %s")
            cursor.execute(query, ['%' + keyword + '%'])
            result = cursor.fetchall()
        return result