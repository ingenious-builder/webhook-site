# Веб-сайт на Supabase

Веб-приложение для отправки сообщений через Supabase. Работает с любого устройства — телефона, компьютера и т.д.

## Что нужно сделать в Supabase

1. **Создайте проект** в [supabase.com](https://supabase.com)
2. **Откройте SQL Editor** (в левой панели → SQL Editor)
3. **Выполните файл** `sql/messages.sql` — создаст таблицу для сообщений
4. **Получите API ключи:**
   - Откройте [Project Settings](https://supabase.com/dashboard/project/_settings/api)
   - В разделе "API" найдите:
     - **anon public key** (для клиентов/браузера)
     - **service role key** (только для сервера, не нужен здесь)

## Как запустить сайт

1. Откройте [index.html](index.html) в браузере
2. В коде найдите строки:
   ```javascript
   const URL = "https://<project-ref>.supabase.co";
   const TABLE = "messages";
   ```
3. Замените `<project-ref>` на идентификатор вашего проекта (он виден в адресе Supabase)
4. Замените `"<API_KEY>"` на **anon public key** из настроек Supabase

## Пример готового кода

```javascript
const URL = "https://abc123def456.supabase.co";  // ваш проект
const TABLE = "messages";                         // таблица сообщений
// API key в заголовках запросов
```

## Как отправить сообщение с iPhone

1. Откройте сайт в Safari на телефоне
2. Напишите текст сообщения
3. Нажмите «Отправить»
4. Сообщение сохранится в таблице Supabase!

## Структура файлов

| Файл | Назначение |
|------|------------|
| `index.html` | Веб-приложение для отправки сообщений |
| `sql/messages.sql` | SQL-скрипт для создания таблицы |
| `README.md` | Эта инструкция |