@echo off

set "scriptDirectory=%~dp0"

set "adbExecutable=%scriptDirectory%tools\adb\adb.exe"

call "%adbExecutable%" kill-server

echo "KILL ADB SERVER SUCCESSFULLY"

pause