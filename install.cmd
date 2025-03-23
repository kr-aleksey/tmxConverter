set APP_NAME=tmcConverter
set TARGET_DIR=%USERPROFILE%\AppData\Roaming\%APP_NAME%
set SHORTCUT_PATH=%USERPROFILE%\Desktop\%APP_NAME%.lnk
set PYTHON_EXECUTABLE=python.exe

:: Создаем папку назначения, если её нет
if not exist "%TARGET_DIR%" mkdir "%TARGET_DIR%"

:: Копируем файлы приложения
xcopy "%SOURCE_DIR%" "%TARGET_DIR%" /E /I /Y

:: Определяем путь до Python (если установлен через PATH)
for /f "tokens=*" %%i in ('where %PYTHON_EXECUTABLE%') do set PYTHON_PATH=%%i

:: Создаем VBS-скрипт для генерации ярлыка
echo Set objShell = CreateObject("WScript.Shell") > create_shortcut.vbs
echo Set objShortcut = objShell.CreateShortcut("%SHORTCUT_PATH%") >> create_shortcut.vbs
echo objShortcut.TargetPath = "%PYTHON_PATH%" >> create_shortcut.vbs
echo objShortcut.Arguments = "\"%TARGET_DIR%\main.py\"" >> create_shortcut.vbs
echo objShortcut.WorkingDirectory = "%TARGET_DIR%" >> create_shortcut.vbs
echo objShortcut.Save >> create_shortcut.vbs

:: Запускаем VBS-скрипт для создания ярлыка
cscript //nologo create_shortcut.vbs

:: Удаляем временный VBS-скрипт
del create_shortcut.vbs

echo Готово! Ярлык создан на рабочем столе.
pause