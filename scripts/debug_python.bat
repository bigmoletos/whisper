@echo off
setlocal enabledelayedexpansion

echo ============================================
echo   Debug Detection Python
echo ============================================
echo.

echo Test 1: py -3.12
py -3.12 --version
echo ERRORLEVEL: !ERRORLEVEL!
echo.

echo Test 2: py -3.11
py -3.11 --version
echo ERRORLEVEL: !ERRORLEVEL!
echo.

echo Test 3: python
python --version
echo ERRORLEVEL: !ERRORLEVEL!
echo.

echo Test 4: py
py --version
echo ERRORLEVEL: !ERRORLEVEL!
echo.

echo Test 5: set variable et utiliser
set "TEST_CMD=py -3.12"
echo Variable: !TEST_CMD!
!TEST_CMD! --version
echo ERRORLEVEL: !ERRORLEVEL!
echo.

pause
