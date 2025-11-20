# Furniture Bot (Aiogram 3.x)
Простая заготовка чат-бота мебельного магазина (Aiogram 3.x).

Инструкции:
1. Создайте виртуальное окружение и установите зависимости:
   ```
   pip install -r requirements.txt
   ```
2. Вставьте токен бота в `data/config.py` (BOT_TOKEN).
3. При необходимости установите MANAGER_CHAT_ID и ADMIN_IDS в `data/config.py`.
4. Инициализируйте БД:
   ```
   python init_db.py
   ```
5. Запустить бота:
   ```
   python main.py
   ```
