# Асинхронный парсер PEP

## Описание проекта

парсер документов PEP на базе фреймворка Scrapy.

-Сохранение всех PEP статусов Python в файл
-Сбор статистики о количестве статусов PEP Python и общем количестве
## Запуск проекта

1. Клонируйте репозиторий с проектом и перейдите в соответствующую директорию:

```
git clone <git@github.com:NikolayGerasimov495/scrapy_parser_pep.git>
```

2. Создайте и активируйте виртуальное окружение:

```
python3 -m venv venv
source venv/bin/activate  # for Mac/Linux
.venv\Scripts\activate.bat  # for Windows
```

3. Установите зависимости для проекта:

```
pip install --upgrade pip
pip install -r requirements.txt
```
4. Изучите проект и запустите парсер из командной строки с указанием имени spider:

```
scrapy crawl pep
```
5. Результат смотрите в папке result


## Автор
Николай Герасимов