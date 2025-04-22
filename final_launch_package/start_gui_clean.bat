@echo off
setlocal ENABLEEXTENSIONS
cd /d %~dp0

:: One Button GUI Build + Launch + Interpreter + API
set ROOT=%cd%
set FRONTEND=%ROOT%\black-dashboard-django-master\frontend
set LIB=%FRONTEND%\lib
set PAGES=%FRONTEND%\pages

mkdir "%FRONTEND%" >nul 2>nul
mkdir "%LIB%" >nul 2>nul
mkdir "%PAGES%" >nul 2>nul

> "%FRONTEND%\package.json" echo {
>> "%FRONTEND%\package.json" echo   "name": "memory-gui",
>> "%FRONTEND%\package.json" echo   "version": "1.0.0",
>> "%FRONTEND%\package.json" echo   "scripts": {
>> "%FRONTEND%\package.json" echo     "dev": "next dev -p 3000",
>> "%FRONTEND%\package.json" echo     "build": "next build",
>> "%FRONTEND%\package.json" echo     "start": "next start -p 3000"
>> "%FRONTEND%\package.json" echo   },
>> "%FRONTEND%\package.json" echo   "dependencies": {
>> "%FRONTEND%\package.json" echo     "next": "13.5.6",
>> "%FRONTEND%\package.json" echo     "react": "18.2.0",
>> "%FRONTEND%\package.json" echo     "react-dom": "18.2.0"
>> "%FRONTEND%\package.json" echo   }
>> "%FRONTEND%\package.json" echo }

call npm install --prefix "%FRONTEND%"
start "" wscript.exe "%ROOT%\launch_api_hidden.vbs"
start "GUI" cmd /c "cd /d %FRONTEND% && npm run dev"
start "Interpreter" cmd /c "interpreter"

echo.
echo [✓] GUI + backend + Open Interpreter launched at http://localhost:3000
pause