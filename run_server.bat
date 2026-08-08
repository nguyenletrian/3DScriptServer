@echo off

cd /d D:\ConnectVBS

call venv\Scripts\activate

uvicorn main:app --reload

pause