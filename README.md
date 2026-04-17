# goit-pythonweb-hw-06

# 🚀 Проєкт: Запуск та використання

Цей проєкт використовує Docker та Alembic для керування базою даних.

## 📦 Вимоги

Перед початком переконайтесь, що у вас встановлено:

- Docker
- Docker Compose
- Python 3.10+
- pip

## 📥 Встановлення залежностей

```bash
pip install -r requirements.txt
```

---

## ⚙️ Запуск проєкту

```bash
make run
```

## ⏹️ Зупинка

```bash
make stop
```

## 🧹 Видалення

```bash
make down
```

---

## 🧼 Повне очищення

```bash
make clean
```

---

## 🗄️ Робота з базою даних

### Створити міграцію
```bash
make makemigrations
# або
make mm
```

### Застосувати міграції
```bash
make migrate
# або
make m
```

### Наповнити БД
```bash
make seed
```

### Ініціалізація БД
```bash
make db_init
```

### Повний ресет БД
```bash
make db_reset
```

---

## 🖥️ CLI

```bash
make cli
```
