@echo off
cd /d "%~dp0"
if not exist node_modules (
  echo Installing project dependencies...
  call npm ci
  if errorlevel 1 exit /b 1
)
echo Site: http://localhost:4321
echo CMS:  http://localhost:4321/admin/
call npm start
