# Общее описание
## Задание
Разработать ассемблер и интерпретатор для учебной виртуальной машины (УВМ). Система команд УВМ представлена далее.

Для ассемблера необходимо разработать читаемое представление команд УВМ. Ассемблер принимает на вход файл с текстом исходной программы, путь к которой задается из командной строки. Результатом работы ассемблера является бинарный файл в виде последовательности байт, путь к которому задается из командной строки. Дополнительный ключ командной строки задает путь к файлу-логу, в котором хранятся ассемблированные инструкции в духе списков “ключ=значение”, как в приведенных далее тестах.

Интерпретатор принимает на вход бинарный файл, выполняет команды УВМ и сохраняет в файле-результате значения из диапазона памяти УВМ. Диапазон также указывается из командной строки.
# Команды ассемблера
## Загрузка константы
| A | B | C |
| :---: | :---: | :---: |
| Биты 0-2 | Биты 3-5 | Биты 6-23 |
| 1 | Адрес | Константа |

Размер команды: 3 байт.

Операнд: поле C.

Результат: регистр по адресу, которым является поле B.
```
LOAD_CONSTANT 1 1 637
```
Байт-код для примера выше:
```0x49, 0x9F, 0x00 ```
## Чтение значения из памяти
| A | B | C | D |
| :---: | :---: | :---: | :---: |
| Биты 0-2 | Биты 3-5 | Биты 6-11 | Биты 12-14 |
| 7 | Адрес | Смещение | Адрес |

Размер команды: 3 байт.

Операнд: ячейка памяти по адресу, которым является сумма адреса (регистр по адресу, которым является поле B) и смещения (поле C).

Результат: регистр по адресу, которым является поле D.
```
READ_MEMORY 7 5 52 4
```
Байт-код для примера выше:
```0x2F, 0x4D, 0x00 ```
## Запись в память
| A | B | C |
| :---: | :---: | :---: |
| Биты 0-2 | Биты 3-5 | Биты 6-8 |
| 3 | Адрес | Адрес |

Размер команды: 3 байт.

Операнд: регистр по адресу, которым является поле B.

Результат: ячейка памяти по адресу, которым является регистр по адресу,
которым является поле C.
```
WRITE_MEMORY 25 48 919
```
Байт-код для примера выше:
```0x73, 0x00, 0x00 ```
## Бинарная операция: унарный минус
| A | B | C |
| :---: | :---: | :---: |
| Биты 0-2 | Биты 3-5 | Биты 6-8 |
| 5 | Адрес | Адрес |

Размер команды: 3 байт.

Операнд: регистр по адресу, которым является поле B.

Результат: регистр по адресу, которым является поле C.
```
UNARY_MINUS 5 6 6
```
Байт-код для примера выше:
```0xB5, 0x01, 0x00 ```
# Сборка и запуск проекта
1. Загрузить репозиторий на компьютер
```
git clone https://github.com/YG5126/MIREA/tree/main/Assembler_interpreter
```
2. Прейдите в директорию репозитория
```
cd Assembler_interpreter
```
3. Запустить assembler.py с указанием исполняемой программы, бинарного файла вывода и лог-файла
```
python assembler.py input.asm output.bin -l log.yaml
```
4. Запустить interpreter.py с указанием бинарного файла данных, файла с результатами и диапазона памяти
```
python interpreter.py output.bin output.yaml -lb 0 -rb 8
```
# Примеры работы программы
### Задание для тестовой программы
Выполнить поэлементно операцию умножение над вектором длины 6 и числом 128. Результат записать в новый вектор. 
### Тестовая программа
```
LOAD_CONSTANT 1 0 42
LOAD_CONSTANT 1 1 100
LOAD_CONSTANT 1 2 50

UNARY_MINUS 5 0 3
UNARY_MINUS 5 1 4

WRITE_MEMORY 3 0 5
WRITE_MEMORY 3 1 6

READ_MEMORY 7 0 10 7
READ_MEMORY 7 1 20 6
```
### Данные, записанные в лог-файл
```
- A: 1
  B: 0
  C: 42
  hex: 810a00
  instruction: LOAD_CONSTANT
- A: 1
  B: 1
  C: 100
  hex: 091900
  instruction: LOAD_CONSTANT
- A: 1
  B: 2
  C: 50
  hex: 910c00
  instruction: LOAD_CONSTANT
- A: 5
  B: 0
  C: 3
  hex: c50000
  instruction: UNARY_MINUS
- A: 5
  B: 1
  C: 4
  hex: 0d0100
  instruction: UNARY_MINUS
- A: 3
  B: 0
  C: 5
  hex: '430100'
  instruction: WRITE_MEMORY
- A: 3
  B: 1
  C: 6
  hex: 8b0100
  instruction: WRITE_MEMORY
- A: 7
  B: 0
  C: 10
  D: 7
  hex: '877200'
  instruction: READ_MEMORY
- A: 7
  B: 1
  C: 20
  D: 6
  hex: 0f6500
  instruction: READ_MEMORY
```
### Данные, записанные в файл-результат
```
- address: 0
  value: 42
- address: 1
  value: 100
- address: 2
  value: 50
- address: 3
  value: -42
- address: 4
  value: -100
- address: 5
  value: 42
- address: 6
  value: 120
- address: 7
  value: 52
```
# Результаты тестирования
## Ассемблер
### Тест базовой функции импорта ассемблера
```
def test_assembler_class_import():
    assert Assembler is not None
    
    test_assembler = Assembler(
        path_to_code='input.asm', 
        path_to_binary_file='output.bin', 
        path_to_log='log.yaml'
    )
    assert test_assembler is not None
```
### Тест декодирования команд ассемблера
```
def test_assembler_methods():
    test_assembler = Assembler(
        path_to_code='input.asm', 
        path_to_binary_file='output.bin', 
        path_to_log='log.yaml'
    )

    encoded = test_assembler.encode_instruction(1, 0, 42)
    assert encoded is not None
    assert len(encoded) == 3
```
## Интерпретатор
### Тест базовой функции импорта интерпретатора
```
def test_interpreter_class_import():
    assert Interpreter is not None

    test_interpreter = Interpreter(
        path_to_binary_file='output.bin', 
        left_boundary=0, 
        right_boundary=8, 
        path_to_result_file='output.yaml'
    )
    assert test_interpreter is not None
```
### Тест декодирования команд интерпретатора
```
def test_interpreter_methods():
    test_interpreter = Interpreter(
        path_to_binary_file='output.bin', 
        left_boundary=0, 
        right_boundary=8, 
        path_to_result_file='output.yaml'
    )
    
    assert hasattr(test_interpreter, 'interpret')
    assert hasattr(test_interpreter, 'make_result')
```
### Тест общей работы программы
```
    assembler = Assembler(
        path_to_code='input.asm', 
        path_to_binary_file='output.bin', 
        path_to_log='log.yaml'
    )
    assembler.assemble()
    
    assert os.path.exists('output.bin')
    
    interpreter = Interpreter(
        path_to_binary_file='output.bin', 
        left_boundary=0, 
        right_boundary=8, 
        path_to_result_file='output.yaml'
    )
    interpreter.interpret()
    
    assert os.path.exists('output.yaml')
```
## Результаты тестирования
![image](https://github.com/YG5126/MIREA/blob/main/Assembler_interpreter/common_test.png)
