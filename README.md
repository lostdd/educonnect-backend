# educonnect


## Установка
0. Клонируйте репозиторий
1. Создайте новое виртуальное окружение Python и установите зависимости
На Windows:
```
python -m venv .venv
.venv\Scripts\pip.exe install -r requirements.txt
```
На Linux:
```
python3 -m venv .venv
.venv\bin\pip3 install -r requirements.txt
```
2. Скопируйте .env-example в .env и отредактируйте его
JWT_SECRET_KEY можно сгенерировать следующим способом
```
python -c "import secrets; print(secrets.token_hex(32))"
```
или
```
openssl rand -hex 32
```
TELEGRAM_BOT_TOKEN для Вашего Telegram-бота получите у BotFather
DATABASE_URL заполните в соответствии с требованиями sqlalchemy
3. Запустите db_init.py
```
.venv\bin\python db_init.py
```
4. Запустите приложение
```
.venv\bin\uvicorn app.main:app --reload
```
