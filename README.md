# django_sprint4

## 🚀 Полный запуск с нуля (для Git Bash)

Скопируй и вставь эти команды одну за другой:

```bash
# 1. Перейти в папку проекта
cd ~/Desktop/Dev/django-sprint4

# 2. Создать виртуальное окружение (если его нет)
python -m venv venv

# 3. Активировать виртуальное окружение
source venv/Scripts/activate

# 4. Установить зависимости из requirements.txt
pip install -r requirements.txt

# 5. Перейти в папку с manage.py
cd blogicum

# 6. Создать миграции
python manage.py makemigrations

# 7. Применить миграции
python manage.py migrate

# 8. Загрузить тестовые данные из фикстур (по желанию)
python manage.py loaddata db.json

# 9. Создать суперпользователя (придумай логин и пароль)
python manage.py createsuperuser

# 10. Запустить сервер
python manage.py runserver
