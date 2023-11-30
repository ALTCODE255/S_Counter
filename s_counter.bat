@ECHO OFF
:ping
ping 1.2.3.4 -n 1 -w 1000 > nul
set target=www.google.com
ping %target% -n 1 | find "TTL=" > nul
if errorlevel==1 goto ping
start "" pythonw bg_script.pyw > nul