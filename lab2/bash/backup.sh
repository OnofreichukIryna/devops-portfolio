#!/bin/bash

# Налаштування (зміни ці шляхи під себе при потребі)
SOURCE_DIR="../../"   # Що бекапимо (наш проект)
BACKUP_DIR="$HOME/backups"            # Куди кладемо бекапи
LOG_FILE="$BACKUP_DIR/backup.log"     # Де лежить лог
DATE=$(date +%Y-%m-%d_%H-%M-%S)       # Поточна дата для назви
BACKUP_NAME="backup_$DATE.tar.gz"

# 1. Створюємо папку для бекапів, якщо її немає
mkdir -p "$BACKUP_DIR"

# 2. Функція для запису в лог
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

log_message "Початок резервного копіювання: $SOURCE_DIR"

# 3. Створення архіву (tar -c: create, -z: gzip, -f: file)
# 2> /dev/null приховує помилки "file changed as we read it", які бувають на живих системах
tar -czf "$BACKUP_DIR/$BACKUP_NAME" "$SOURCE_DIR" 2> /dev/null

# Перевірка, чи створився файл
if [ $? -eq 0 ]; then
    log_message "Успішно створено: $BACKUP_NAME"
    echo "Backup created: $BACKUP_NAME"
else
    log_message "ПОМИЛКА при створенні бекапу!"
    echo "Error creating backup!"
    exit 1
fi

# 4. Очищення старих бекапів (залишаємо тільки 5 найсвіжіших)
# ls -t (сортує за часом), tail -n +6 (бере всі, починаючи з 6-го), xargs rm (видаляє їх)
cd "$BACKUP_DIR"
ls -t backup_*.tar.gz | tail -n +6 | xargs -r rm --

log_message "Очищення завершено. Залишено останні 5 копій."
echo "Cleanup done."