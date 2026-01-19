@echo off
REM Runs all the checks (lint, type check, and tests) in sequence.

echo "Running all checks..."
call .\lint.bat
call .\type_check.bat
call .\run_tests.bat
echo "All checks completed."
pause
