# tmxConverter #
*tmxConverter* конвертирует файлы TMX (Translation Memory Exchange) в формат Excel.

## Usage ##
Готовые исполняемые файлы находятся в папке `dist`.

### Building ###
Сборка исполняемого файла производится в той ОС для которой он собирается. Для успешной сборки необходимо
активировать `venv` и установить все зависимости из `requirements.txt`.

Процесс сборки:

Активируем venv

`venv\Scripts\activate`

Устанавливаем зависимости

`pip install -r requiremets.txt`

Собираем исполняемый файл

`pyinstaller.exe tmxConverter.spec`
