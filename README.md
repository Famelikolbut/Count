# Инструкция для запуска проекта

1. Клонирование репозитория

```
git clone <URL репозитория>
cd <название репозитория>
```

2. Создание виртуального окружения и установка зависимостей

```
python3 -m venv venv / python -m venv venv    
source venv/bin/activate  # venv\Scripts\Activate
pip install -r requirements.txt
```

3. Запуск Docker Compose

```
docker-compose up -d --build
```

4. Миграция базы данных и создание суперпользователя

```
docker exec -it my_web_app bash
python manage.py migrate / alembic upgrade head 
python manage.py createsuperuser
```

