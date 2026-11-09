"""Инструмент для работы с GitHub через REST API.

Использование:
    python github_tool.py <команда> [аргументы...]

Примеры:
    python github_tool.py create-repo my-project
    python github_tool.py deploy-pages my-project
    python github_tool.py list-files my-project
"""

import json
import os
import sys
import urllib.request


def get_github_token():
    """Получает токен доступа из переменной окружения."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Ошибка: не найден GITHUB_TOKEN. Войдите в GitHub CLI:")
        print('  gh auth login')
        sys.exit(1)
    return token


def api_request(method, url, data=None):
    """Отправляет запрос к GitHub API."""
    headers = {
        "Authorization": f"Bearer {get_github_token()}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "github-tool/1.0",
    }

    req = urllib.request.Request(url, method=method)
    for k, v in headers.items():
        req.add_header(k, v)

    if data:
        body = json.dumps(data).encode()
        req.data = body
        req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read().decode()
    except urllib.error.HTTPError as e:
        error_data = e.read().decode()[:500]
        print(f"Ошибка API ({e.code}): {error_data}")
        sys.exit(1)


def create_repo(repo_name):
    """Создаёт репозиторий."""
    url = f"https://api.github.com/repos/{get_current_user()}/{repo_name}"
    data = {"name": repo_name, "private": False}
    result = api_request("POST", url, data)
    print(f"✅ Репозиторий создан: {result[:100]}")


def deploy_pages(repo_name):
    """Включает GitHub Pages для репозитория."""
    url = f"https://api.github.com/repos/{get_current_user()}/{repo_name}/pages"
    data = {"source": {"branch": "main", "folder": "/"}}
    result = api_request("PUT", url, data)
    print(f"✅ GitHub Pages включён: {result[:100]}")


def list_files(repo_name):
    """Показывает файлы в репозитории."""
    url = f"https://api.github.com/repos/{get_current_user()}/{repo_name}/contents/"
    result = api_request("GET", url)
    print(result[:2000])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python github_tool.py <команда> [аргументы...]")
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    if command == "create-repo":
        create_repo(args[0])
    elif command == "deploy-pages":
        deploy_pages(args[0])
    elif command == "list-files":
        list_files(args[0])
    else:
        print(f"Неизвестная команда: {command}")