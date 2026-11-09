-- Создайте таблицу для сообщений в Supabase

CREATE TABLE IF NOT EXISTS messages (
    id BIGSERIAL PRIMARY KEY,
    message TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Разрешаем чтение и запись через REST API (anon)
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

CREATE POLICY "public read/write" ON messages
    FOR ALL
    USING (true)
    WITH CHECK (true);