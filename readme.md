Учебный проект на тему меню ресторана. Реализован CRUD на python (FastAPI) + PostgreSQL.

Инструкция по установке для Ubuntu 22.04:

Скопировать проект с репозитория га локальную машину
git clone https://github.com/Sana451/fast_api_v1.git

Перейти в папку с проектом
cd fast_api_v1/

При необходимости создать виртуальное окружение
python3 -m venv api
source api/bin/activate

Установить зависимости
pip install -r requirements.txt

Открыть файл models.py и настроить параметры подключения к базе данных PostgreSQL 
(DB_USER, DB_PASSWD, DB_HOST, DB_PORT, DB_NAME).

Запустить сервер
uvicorn main:app --host localhost --port 8000 --reload