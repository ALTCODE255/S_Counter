export $(xargs <.env)
sqlite3 -markdown counter.db "SELECT * FROM S_Counter ORDER BY Date Desc" > S_Counter.md
new_content=$(sed ':a;N;$!ba;s/\n/\\n/g' S_Counter.md)
if [ "$(curl https://gist.githubusercontent.com/ALTCODE255/f674d02b89b93cdeb51ea782e03f06ff/raw/ 2>/dev/null | head -3)" != "$(head -3 S_Counter.md)" ]; then
    curl -L \
    -X PATCH \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer $GH_PAT" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    https://api.github.com/gists/f674d02b89b93cdeb51ea782e03f06ff \
    -d '{"description":"","files":{"S_Counter.md":{"content":"'"$new_content"'"}}}'
fi