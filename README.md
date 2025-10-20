<h2>🚀 Установка и запуск</h2>


<h4>
1. Создайте файл .env в корневой директории согласно .env.example:
</h4>

```requirements
PROJECT_NAME=
BASE_URL='http://127.0.0.1'
API_KEY={Статический API ключ}

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=db
DB_PORT=5432
```

<h4>
2. Запустите docker compose:
</h4>

```commandline
docker compose up --build -d
```


<h4>
3. Загрузите тестовые данные в БД:
</h4>

```commandline
docker exec -it {PROJECT_NAME из .env}_app python app/scripts/load_db.py
```



<b>
Готово!
<br>
Документация API: http://127.0.0.1/docs
</b>
