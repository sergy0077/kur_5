-- Создание таблицы "companies" для хранения данных о компаниях
CREATE TABLE IF NOT EXISTS companies (
    id_company SERIAL PRIMARY KEY,
    title_company VARCHAR(255) UNIQUE NOT NULL,
    number_vacancies INTEGER
);

-- Создание таблицы "vacancies" для хранения данных о вакансиях
CREATE TABLE IF NOT EXISTS vacancies (
    vacancy_name TEXT,
    id_company INTEGER REFERENCES companies(id_company),
    title VARCHAR(255) UNIQUE,
    salary NUMERIC(10, 2),
    link TEXT
);

-- Добавляем компанию
INSERT INTO companies (title_company, number_vacancies) VALUES (%s, %s)
ON CONFLICT (title_company) DO
UPDATE SET number_vacancies = EXCLUDED.number_vacancies;

-- Получаем id компании из таблицы companies
SELECT id_company FROM companies WHERE title_company = %s;

-- Если компания существует, вставляем данные о вакансии с указанием id_company
INSERT INTO vacancies (id_company, vacancy_name, title, salary, link)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (title) DO UPDATE SET salary = EXCLUDED.salary

-- Получение списка всех компаний и количество вакансий у каждой компании
SELECT companies.title_company, COUNT(vacancies.id_company)
FROM companies
LEFT JOIN vacancies ON companies.id_company = vacancies.id_company
GROUP BY companies.title_company;

-- Получение списка всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию
SELECT companies.title_company, vacancies.title, vacancies.salary, vacancies.link
FROM vacancies
INNER JOIN companies
ON vacancies.id_company = companies.id_company;

-- Получение средней зарплаты по вакансиям
SELECT AVG(salary) FROM vacancies;

-- Получение списка всех вакансий, у которых зарплата выше средней по всем вакансиям
SELECT companies.title_company, vacancies.title, vacancies.salary, vacancies.link
FROM vacancies
INNER JOIN companies ON vacancies.id_company = companies.id_company
WHERE vacancies.salary > %s;

-- Получение списка всех вакансий, в названии которых содержатся переданные в метод слова
SELECT companies.title_company, vacancies.title, vacancies.salary, vacancies.link
FROM vacancies
INNER JOIN companies ON vacancies.id_company = companies.id_company
WHERE vacancies.title ILIKE %s
