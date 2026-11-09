"""Простой вебхук-сервер без внешних зависимостей (Python stdlib).

Получает POST /webhook с JSON, сохраняет сообщения в log и отдаёт ответ.
GET /webhook — показывает историю полученных сообщений.

Запуск:  python webhook_server.py
"""

import json
import os
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

LOG_FILE = "webhook_messages.jsonl"


def load_messages():
    """Читает историю сообщений из JSONL-файла."""
    messages = []
    if not os.path.exists(LOG_FILE):
        return messages
    with open(LOG_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    messages.append(json.loads(line))
                except json.JSONDecodeError:
                    pass  # пропускаем повреждённые строки
    return messages


class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", "0") or "0")
        if content_length > 1024 * 1024:
            self.send_response(413)
            self.end_headers()
            return

        body = self.rfile.read(content_length)
        try:
            data = json.loads(body.decode("utf-8")) if body else {}
        except (json.JSONDecodeError, UnicodeDecodeError):
            data = {"error": "Некорректный формат JSON"}

        messages = load_messages()
        message_id = len(messages) + 1
        entry = {
            "id": message_id,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "data": data,
        }
        messages.append(entry)

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        response = {
            "ok": True,
            "message_id": message_id,
            "received_at": entry["timestamp"],
            "echo": data,
        }
        self.send_response(200)
        content_type = "application/json"
        self.send_header("Content-Type", content_type)
        self.end_headers()
        response_body = json.dumps(response, ensure_ascii=False).encode("utf-8")
        self.wfile.write(response_body)

    def do_GET(self):
        if self.path != "/webhook":
            self.do_POST()  # GET к /webhook тоже показывает историю
            return

        messages = load_messages()
        response = {
            "ok": True,
            "count": len(messages),
            "messages": messages[-10:],  # последние 10 сообщений
        }
        self.send_response(200)
        content_type = "application/json"
        self.send_header("Content-Type", content_type)
        self.end_headers()
        response_body = json.dumps(response, ensure_ascii=False).encode("utf-8")
        self.wfile.write(response_body)

    def log_message(self, format, *args):
        # Подавляем стандартный лог Python
        pass


if __name__ == "__main__":
    print(f"Вебхук запущен: http://localhost:8000/webhook")
    print("Отправляй POST-запросы с JSON в тело.")
    try:
        ThreadingHTTPServer(("0.0.0.0", 8000), WebhookHandler).serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")