# **Задание №1**
Разработать эмулятор для языка оболочки ОС. Необходимо сделать работу эмулятора как можно более похожей на сеанс shell в UNIX-подобной ОС. Эмулятор должен запускаться из реальной командной строки, а файл с виртуальной файловой системой не нужно распаковывать у пользователя. Эмулятор принимает образ виртуальной файловой системы в виде файла формата **zip**. Эмулятор должен работать в режиме **GUI**.

Конфигурационный файл имеет формат **csv** и содержит:
- Имя компьютера для показа в приглашении к вводу.
- Путь к архиву виртуальной файловой системы.
- Путь к лог-файлу.

Необходимо поддержать в эмуляторе команды ls, cd и exit, а также следующие команды:
1. uname.
2. rev.
3. touch.

Все функции эмулятора должны быть покрыты тестами, а для каждой из поддерживаемых команд необходимо написать 3 теста.
# Установка
Перед началом работы с программой требуется скачать репозиторий и необходимую библиотеку для тестов. Для этого можно воспользоваться командами ниже.
```Bash
git clone https://github.com/YG5126/MIREA/tree/main/Shell-Emulator
```
```Bash
pip install -U pytest
```
# Запуск
Перед запуском необходимо клонировать репозиторий в среду разработки.

Обязательно прописать путь к файловой системе в config.csv.

Переход в директорию Shell-Emulator:
```Bash
cd Shell-Emulator
```
Запуск main.py:
```Bash
py main.py config.csv
```
Запуск тестов
```Bash
pytest test.py -v
```
# Команды

``` ls <path> ``` - Список файлов и директорий

``` cd <path> ``` - Смена директории

``` exit ``` - Выход из эмулятора

``` uname ``` - Отображение информации о системе

``` rev <text> ``` - Обратный порядок символов в тексте

``` touch <name> ``` - Создание файла

# Тесты
## ls
![](https://github.com/YG5126/MIREA/tree/main/Shell-Emulator/Test/Test_ls.png)
## cd
![](https://github.com/YG5126/MIREA/tree/main/Shell-Emulator/Test/Test_cd.png)
## exit
![](https://github.com/YG5126/MIREA/tree/main/Shell-Emulator/Test/Test_exit.png)
## uname
![](https://github.com/YG5126/MIREA/tree/main/Shell-Emulator/Test/Test_uname.png)
## rev
![](https://github.com/YG5126/MIREA/tree/main/Shell-Emulator/Test/Test_rev.png)
## touch
![](https://github.com/YG5126/MIREA/tree/main/Shell-Emulator/Test/Test_touch.png)
## Общие тесты через pytest
![](https://github.com/YG5126/MIREA/tree/main/Shell-Emulator/Test/Test_common.png)
