@echo off
:while
(
   cls
   python ProcessJSON.py
   timeout /t 5 /nobreak
   goto :while
)