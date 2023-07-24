# Учебный проект на тему меню ресторана. Реализован CRUD на python (FastAPI) + PostgreSQL.

### Инструкция по установке для Ubuntu 22.04:

Скопировать проект с репозитория на локальную машину, командой:
*   git clone https://github.com/Sana451/fast_api_project.git


Перейти в папку с проектом командой:
*   cd ./fast_api_project/


При необходимости создать виртуальное окружение, командой:
*   python3 -m venv api
*   source api/bin/activate


Установить python зависимости, командой:
*   pip install -r requirements.txt


Открыть файл models.py и настроить параметры подключения к базе данных PostgreSQL 
(DB_USER, DB_PASSWD, DB_HOST, DB_PORT, DB_NAME).


Запустить сервер, командой:
*   uvicorn main:app --host localhost --port 8000 --reload
