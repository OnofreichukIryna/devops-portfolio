#!/bin/bash

# --- НАЛАШТУВАННЯ ---
# Встав сюди свій вебхук (БЕЗ /github у кінці!)
DISCORD_WEBHOOK="https://discordapp.com/api/webhooks/1445883804957806678/0IBR-ustR0f4l2Ev8_foLkQvdWT6QAfdXhqCG_nrzc0PB7pzXWBLehjynOTfL_5qilKN"

# Пороги тривоги (у відсотках)
DISK_THRESHOLD=90
RAM_THRESHOLD=90
# --------------------

# Функція надсилання повідомлення в Discord
send_discord_alert() {
    local message=$1
    # Використовуємо curl для відправки JSON POST запиту
    curl -H "Content-Type: application/json" \
         -d "{\"content\": \"⚠️ **SYSTEM ALERT** ⚠️\n$message\"}" \
         "$DISCORD_WEBHOOK"
}

# 1. Перевірка дискового простору (беремо корінь /)
# df -h / | grep / | awk '{ print $5 }' бере відсоток, sed 's/%//' прибирає знак %
DISK_USAGE=$(df / | grep / | awk '{ print $5 }' | sed 's/%//')

if [ "$DISK_USAGE" -gt "$DISK_THRESHOLD" ]; then
    MSG="Disk usage is critical: ${DISK_USAGE}%"
    echo "$MSG"
    send_discord_alert "$MSG"
fi

# 2. Перевірка RAM
# free | grep Mem | awk '{print $3/$2 * 100.0}' рахує відсоток
RAM_USAGE=$(free | grep Mem | awk '{print $3/$2 * 100.0}' | awk '{print int($1)}')

if [ "$RAM_USAGE" -gt "$RAM_THRESHOLD" ]; then
    MSG="RAM usage is critical: ${RAM_USAGE}%"
    echo "$MSG"
    send_discord_alert "$MSG"
fi

echo "Check finished. Disk: ${DISK_USAGE}%, RAM: ${RAM_USAGE}%"