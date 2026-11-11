@echo off
set "ROOT=%~dp0..\..\..\.."
if not exist "%ROOT%\.agentlab\venv\Scripts\python.exe" (
  echo Please run the AgentLab setup first. / Once AgentLab kurulumunu calistirin.
  pause
  exit /b 1
)
"%ROOT%\.agentlab\venv\Scripts\python.exe" "%~dp0app.py"
if errorlevel 1 pause
