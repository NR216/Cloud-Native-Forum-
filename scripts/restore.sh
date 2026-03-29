#!/bin/bash
# Database restore script for PostgreSQL
# Usage: ./restore.sh <backup_file>

set -e

if [ -z "$1" ]; then
    echo "Usage: ./restore.sh <backup_file>"
    echo ""
    echo "Available backups:"
    ls -lh /backups/forum_*.sql.gz 2>/dev/null || echo "  No backups found."
    exit 1
fi

BACKUP_FILE="$1"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "ERROR: Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "WARNING: This will overwrite the current database!"
echo "Backup file: $BACKUP_FILE"
echo "Target: ${PGDATABASE}@${PGHOST}"
echo ""
echo "Press Ctrl+C to cancel, or wait 5 seconds to continue..."
sleep 5

echo "[$(date)] Starting database restore from $BACKUP_FILE..."

# Drop and recreate the database schema
gunzip -c "$BACKUP_FILE" | psql -h "$PGHOST" -U "$PGUSER" -d "$PGDATABASE" --no-password

if [ $? -eq 0 ]; then
    echo "[$(date)] Restore completed successfully!"
else
    echo "[$(date)] ERROR: Restore failed!"
    exit 1
fi
