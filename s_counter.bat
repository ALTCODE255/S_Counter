:ping
ping 1.2.3.4 -n 1 -w 1000 > nul
set target=www.google.com
ping %target% -n 1 | find "TTL="
if errorlevel==1 goto ping
taskkill /f /IM pythonw3.11.exe
start "" pythonw s_counter.pyw