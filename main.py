from postgres_db import DBManager
from config import config


def main():
    params = config(filename=r"database.ini")

    # Получаем значение User-Agent от пользователя
    user_agent = input("Введите значение User-Agent, взятого из личного кабинета hh.ru: ")

    # Добавляем user_agent в params
    params['user_agent'] = user_agent

    print(params)

    # Создание экземпляра DBManager
    db_manager = DBManager(params)

    # Создание таблиц и вставка данных о компаниях и вакансиях
    db_manager.create_tables()
    db_manager.insert_companies_and_vacancies()

    # Получение списка всех компаний и количество вакансий у каждой компании
    companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
    print(companies_and_vacancies_count)

    # Получение списка всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию
    all_vacancies = db_manager.get_all_vacancies()
    print(all_vacancies)

    # Получение средней зарплаты по вакансиям
    avg_salary = db_manager.get_avg_salary()
    print(avg_salary)

    # Получение списка всех вакансий, у которых зарплата выше средней по всем вакансиям
    higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
    print(higher_salary_vacancies)

    # Получение списка всех вакансий, в названии которых содержится переданное в метод слово "python"
    keyword = 'python'
    keyword_vacancies = db_manager.get_vacancies_with_keyword(keyword)
    print(keyword_vacancies)

    while True:
        print("\nВыберите действие:")
        print("1. Получить список всех компаний и количество вакансий у каждой компании")
        print("2. Получить список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию")
        print("3. Получить среднюю зарплату по вакансиям")
        print("4. Получить список всех вакансий с зарплатой выше средней")
        print("5. Получить список всех вакансий, в названии которых содержится определенное слово")
        print("0. Выйти из программы")

        choice = input("Введите номер действия: ")

        if choice == "1":
            companies_and_vacancies = db_manager.get_companies_and_vacancies_count()
            print("Список всех компаний и количество вакансий у каждой компании:")
            for company, vacancies_count in companies_and_vacancies:
                print(f"Компания: {company}, Количество вакансий: {vacancies_count}")

        elif choice == "2":
            all_vacancies = db_manager.get_all_vacancies()
            print("Список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию:")
            for company, title, salary, link in all_vacancies:
                print(f"Компания: {company}, Вакансия: {title}, Зарплата: {salary}, Ссылка: {link}")

        elif choice == "3":
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата по вакансиям: {avg_salary}")

        elif choice == "4":
            vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
            print("Список всех вакансий с зарплатой выше средней:")
            for company, title, salary, link in vacancies_with_higher_salary:
                print(f"Компания: {company}, Вакансия: {title}, Зарплата: {salary}, Ссылка: {link}")

        elif choice == "5":
            keyword = input("Введите ключевое слово: ")
            vacancies_with_keyword = db_manager.get_vacancies_with_keyword(keyword)
            print(f"Список всех вакансий, в названии которых содержится слово '{keyword}':")
            for company, title, salary, link in vacancies_with_keyword:
                print(f"Компания: {company}, Вакансия: {title}, Зарплата: {salary}, Ссылка: {link}")

        elif choice == "0":
            print("Программа завершена.")
            break

        else:
            print("Неверный ввод. Попробуйте снова.")



if __name__ == "__main__":
    main()
