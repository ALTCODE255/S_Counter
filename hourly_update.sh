#!/bin/bash
cd "$(dirname "$0")"
export $(xargs < .env)
new_content=$(sqlite3 -markdown counter.db "SELECT * FROM S_Counter ORDER BY Date Desc")
echo "$new_content" | gh gist edit f674d02b89b93cdeb51ea782e03f06ff -f S_Counter.md -
