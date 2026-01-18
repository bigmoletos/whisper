@echo off
:: Script ultra-simple pour tester
setlocal enabledelayedexpansion

cd /d "%~dp0.."

echo Test config_checker avec py -3.12
py -3.12 scripts\config_checker.py
echo ERRORLEVEL: !ERRORLEVEL!
pause

echo Test config_checker avec py
py scripts\config_checker.py
echo ERRORLEVEL: !ERRORLEVEL!
pause

echo Test config_checker avec python
python scripts\config_checker.py
echo ERRORLEVEL: !ERRORLEVEL!
pause
