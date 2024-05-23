@echo off
SET /P IMAGE_ID=chatgpt-server: 
docker rmi %IMAGE_ID%
if %ERRORLEVEL% == 0 (
    echo Image %IMAGE_ID% deleted successfully.
) else (
    echo Failed to delete image %IMAGE_ID%.
)
pause
