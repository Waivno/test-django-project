# Django Educational Platform API

Django REST API для платформы онлайн-обучения с системой продуктов и уроков.

## 📋 Функционал

- **Продукты** - образовательные курсы/продукты
- **Доступ к продуктам** - система управления доступом пользователей к продуктам
- **Уроки** - учебные материалы, привязанные к продуктам
- **Статусы просмотра** - отслеживание прогресса просмотра уроков
- **Статистика** - аналитика по продуктам (количество студентов, просмотры, время просмотра)

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка переменных окружения

Скопируйте `.env.example` в `.env` и настройте значения:

```bash
cp .env.example .env
```

### 3. Миграции

```bash
python manage.py migrate
```

### 4. Запуск сервера

```bash
python manage.py runserver
```

## 📡 API Endpoints

### Продукты и статистика

| Метод | URL | Описание | Права доступа |
|-------|-----|----------|---------------|
| GET | `/myapp/api/products-stats/` | Статистика по продуктам | Только staff |

### Уроки

| Метод | URL | Описание | Права доступа |
|-------|-----|----------|---------------|
| GET | `/mystu/api/lessons/` | Все доступные уроки пользователя | Authenticated |
| GET | `/mystu/api/lessons/product/<product_id>/` | Уроки конкретного продукта | Authenticated + доступ к продукту |

## 🔐 Аутентификация

API использует session authentication Django. Для доступа к защищённым endpoint'ам необходимо быть аутентифицированным пользователем.

## 🏗️ Структура проекта

```
/workspace/
├── b_test/                 # Основной проект Django
│   ├── settings.py         # Настройки проекта
│   └── urls.py             # Корневые URL
├── myapp/                  # Приложение продуктов
│   ├── models.py           # Модели Product, ProductAccess
│   ├── views.py            # API Views
│   ├── serializers.py      # DRF Serializers
│   ├── admin.py            # Админ-панель
│   └── tests.py            # Тесты
├── mystu/                  # Приложение уроков
│   ├── models.py           # Модели Lesson, LessonViewStatus
│   ├── views.py            # API Views
│   ├── serializers.py      # DRF Serializers
│   ├── admin.py            # Админ-панель
│   └── tests.py            # Тесты
├── requirements.txt        # Зависимости
├── .env.example           # Пример переменных окружения
└── manage.py
```

## 🧪 Тестирование

```bash
python manage.py test myapp.tests mystu.tests
```

## 🔧 Переменные окружения

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `SECRET_KEY` | Секретный ключ Django | (встроенный dev ключ) |
| `DEBUG` | Режим отладки | `True` |
| `ALLOWED_HOSTS` | Разрешённые хосты | `localhost` |
| `DB_ENGINE` | Движок БД | `django.db.backends.sqlite3` |
| `DB_NAME` | Имя базы данных | `db.sqlite3` |
| `DB_USER` | Пользователь БД | `` |
| `DB_PASSWORD` | Пароль БД | `` |
| `DB_HOST` | Хост БД | `localhost` |
| `DB_PORT` | Порт БД | `5432` |

## 📊 Модели данных

### Product
- `name` - название продукта
- `description` - описание
- `owner` - владелец (User)
- `created_at`, `updated_at` - временные метки

### ProductAccess
- `product` - связь с продуктом
- `user` - пользователь
- `is_valid` - действителен ли доступ
- `created_at` - дата предоставления доступа

### Lesson
- `name` - название урока
- `video_url` - ссылка на видео
- `duration` - длительность (сек)
- `products` - продукты, к которым привязан урок
- `created_at`, `updated_at` - временные метки

### LessonViewStatus
- `user` - пользователь
- `lesson` - урок
- `status` - статус (VIEWED/NOT_VIEWED)
- `view_time` - время просмотра (сек)
- `created_at`, `updated_at` - временные метки

## ⚙️ Особенности реализации

- ✅ Исправлены относительные импорты на абсолютные
- ✅ Добавлены `permission_classes` ко всем API View
- ✅ Оптимизированы запросы с `select_related` и `prefetch_related`
- ✅ Проверка `ProductAccess.is_valid` во всех queries
- ✅ Добавлено поле `created_at` в `LessonViewStatus`
- ✅ Настроены переменные окружения для SECRET_KEY и DATABASE
- ✅ Зарегистрированы модели в admin.py
- ✅ Добавлены `__str__` методы в модели
- ✅ Написаны тесты для критического функционала

## 📝 Лицензия

MIT
