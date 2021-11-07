# Автомотизируем получение резюме текста

Алгоритм ищет в тексте ключевые слова и фразы, составляет из него краткое резюме текста: алгоритм проходит по тексту, ранжируя фразы и слова по важности, а затем возвращает предложения наиболее релевантные основному смыслу.

На вход алгоритм получает текст из файла - <имя_файла>, на выходе возвращет резюме текста в файле <имя_файла>_summary.txt

Для работы необходимо:
1) Скопировать проект из GitHub и перейти в папку с проектом:
```bash
$ git clone git@github.com:ikazman/text_summary.git
```
```bash
$ cd text_summary
```
2) Развернуть виртуальное окружение:
```bash
$ python3 -m venv venv
```
3) Установить зависимости из файла requirements.txt:
```bash
$ pip install --upgrade pip
```
```bash
$ pip install -r requirements.txt
```
3) Поместить файлы с текстами в формате txt в папку texts_and_summaries
4) Создать файл .env в котором указать полный путь до папки texts_and_summaries
```bash
PATH_TO_FILE='/home/ikazman/Documents/GitHub/text_summary/texts_and_summaries' # пример
```
5) Запустить скрипт:
```bash
$ python text_summarization.py 
```

Результат будет в папке texts_and_summaries.
