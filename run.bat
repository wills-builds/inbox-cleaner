@echo off
echo ================================
echo Gmail Unsubscriber
echo ================================
echo.
echo Scanning your Gmail for unsubscribe links...
echo This may take a few minutes.
echo.

python unsubscriber.py

echo.
echo ================================
echo Done! Check unsubscribe_list.txt
echo ================================
echo.
pause
