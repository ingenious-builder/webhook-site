// Простой вебхук-сервер без внешних зависимостей (Node.js).
// Запуск:  node webhook_server.js

const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 8000;
const LOG_FILE = 'webhook_messages.jsonl';

function loadMessages() {
    try {
        return JSON.parse(fs.readFileSync(LOG_FILE, 'utf-8'));
    } catch (e) {
        return [];
    }
}

function saveMessage(data) {
    const messages = loadMessages();
    const entry = {
        id: messages.length + 1,
        timestamp: new Date().toISOString(),
        data
    };
    messages.push(entry);
    fs.writeFileSync(LOG_FILE, JSON.stringify(messages, null, 2));
    return entry;
}

function sendJSON(res, statusCode, obj) {
    const body = JSON.stringify(obj);
    res.writeHead(statusCode, { 'Content-Type': 'application/json' });
    res.end(body);
}

const server = http.createServer((req, res) => {
    if (req.method === 'GET') {
        // GET /webhook — показывает историю сообщений
        const messages = loadMessages();
        sendJSON(res, 200, { ok: true, count: messages.length, messages: messages.slice(-10) });
        return;
    }

    if (req.method !== 'POST') {
        sendJSON(res, 405, { error: 'Method not allowed' });
        return;
    }

    const chunks = [];
    req.on('data', chunk => chunks.push(chunk));
    req.on('end', () => {
        let data = {};
        try {
            const body = Buffer.concat(chunks).toString('utf-8');
            if (body.trim()) data = JSON.parse(body);
        } catch (e) {
            data = { error: 'Некорректный формат JSON' };
        }

        const entry = saveMessage(data);
        sendJSON(res, 200, { ok: true, message_id: entry.id, received_at: entry.timestamp, echo: data });
    });
});

server.listen(PORT, () => {
    console.log(`Вебхук запущен: http://localhost:${PORT}/webhook`);
});