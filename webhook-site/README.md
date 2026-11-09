# Веб-сайт на Supabase + GitHub Pages

Веб-приложение для отправки сообщений через Supabase. Работает с любого устройства — телефона, компьютера и т.д.

## Как запустить на GitHub Pages (автоматически)

1. Установите [GitHub CLI](https://cli.github.com/)
2. Войдите в свой аккаунт:
   ```bash
   gh auth login
   ```
3. Запустите скрипт:
   ```powershell
   powershell.exe -ExecutionPolicy Bypass -File webhook-site/deploy.ps1
   ```

Скрипт сам создаст репозиторий, загрузит файлы и включит GitHub Pages!

## Настройка Supabase

1. **Создайте проект** в [supabase.com](https://supabase.com)
2. **Откройте SQL Editor** → выполните `sql/messages.sql`
3. **Получите API key:** Project Settings → API → раздел "anon public"

## Настройка сайта

1. Откройте `index.html`
2. Замените:
   ```javascript
   const URL = "https://<project-ref>.supabase.co";  // ваш проект
   const TABLE = "messages";                          // таблица
   ```
3. Замените `"<API_KEY>"` на **anon public key** из Supabase

## Как отправить сообщение с iPhone 📱

1. Откройте сайт в Safari на телефоне (например: `https://ваш-пользователь.github.io`)
2. Введите email и пароль
3. Напишите текст сообщения
4. Нажмите «Отправить»
5. Сообщение сохранится в таблице Supabase!

## Структура файлов

| Файл | Назначение |
|------|------------|
| `index.html` | Веб-приложение для отправки сообщений |
| `sql/messages.sql` | SQL-скрипт для создания таблицы |
| `deploy.ps1` | Скрипт автоматической загрузки на GitHub Pages |
| `github_tool.py` | Инструмент для работы с GitHub через API |
| `README.md` | Эта инструкция |