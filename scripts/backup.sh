#!/bin/bash
# Database backup script for PostgreSQL
# Runs inside the backup container, executed every hour

set -e

BACKUP_DIR="/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/forum_${TIMESTAMP}.sql.gz"
RETENTION_DAYS=7

mkdir -p "$BACKUP_DIR"

echo "[$(date)] ===== Starting database backup ====="

# Perform the backup using pg_dump and compress with gzip
pg_dump -h "$PGHOST" -U "$PGUSER" -d "$PGDATABASE" --no-password | gzip > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    FILE_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "[$(date)] Backup successful: $BACKUP_FILE ($FILE_SIZE)"
else
    echo "[$(date)] ERROR: Backup failed!"
    rm -f "$BACKUP_FILE"
    exit 1
fi

# Verify backup integrity
if gunzip -t "$BACKUP_FILE" 2>/dev/null; then
    echo "[$(date)] Backup integrity check: PASSED"
else
    echo "[$(date)] ERROR: Backup integrity check FAILED!"
    exit 1
fi

# Rotate old backups - delete backups older than RETENTION_DAYS
echo "[$(date)] Cleaning backups older than ${RETENTION_DAYS} days..."
DELETED=$(find "$BACKUP_DIR" -name "forum_*.sql.gz" -mtime +$RETENTION_DAYS -print -delete | wc -l)
echo "[$(date)] Deleted $DELETED old backup(s)"

# List remaining backups
REMAINING=$(ls -1 ${BACKUP_DIR}/forum_*.sql.gz 2>/dev/null | wc -l)
TOTAL_SIZE=$(du -sh "$BACKUP_DIR" 2>/dev/null | cut -f1)
echo "[$(date)] Remaining backups: $REMAINING (Total size: $TOTAL_SIZE)"
echo "[$(date)] ===== Backup completed ====="
