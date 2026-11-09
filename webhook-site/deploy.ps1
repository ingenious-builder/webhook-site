# Скрипт автоматической загрузки сайта на GitHub Pages
# Запуск: powershell.exe -ExecutionPolicy Bypass -File webhook-site/deploy.ps1

Write-Host "🚀 Начинаем загрузку сайта..." -ForegroundColor Green

# 1. Создаём репозиторий (если ещё не создан)
$repoName = "webhook-site"
gh repo create $repoName --public --source=. --push --disallow-others

Write-Host "✅ Репозиторий создан: https://github.com/$($env:USER)/$repoName" -ForegroundColor Green

# 2. Включаем GitHub Pages
gh api repos/$($env:USER)/$repoName/pages \
  --method PUT \
  --input '{ "source": { "branch": "main", "folder": "/" } }' \
  | Out-Null

Write-Host "✅ GitHub Pages включён" -ForegroundColor Green

# Ждём публикации (до 5 минут)
$deadline = Get-Date -Add Minutes 5
while ((Get-Date).Compare($deadline) -lt 0) {
    $status = gh api repos/$($env:USER)/$repoName/pages/status \
      | ConvertFrom-Json | Select-Object -ExpandProperty state

    if ($status -eq "ready") { break }
    Start-Sleep -Seconds 15
}

Write-Host "✅ Сайт опубликован!" -ForegroundColor Green
Write-Host "`n📱 Откройте сайт в Safari на iPhone:" -ForegroundColor Cyan
Write-Host "https://$($env:USER).github.io" -ForegroundColor Yellow