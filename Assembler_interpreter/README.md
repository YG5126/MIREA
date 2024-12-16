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
python assembler.py input.asm output.bin -l log.yaml
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
### Тест загрузки константы
```
def test_load_const(self):
        filename = 'test_file.asm'
        binary_file = 'test_bin.bin'
        log_file = 'test_log.xml'

        with open(filename, 'w') as f:
            f.write("LOAD_CONSTANT 36 32 12")

        assembler = Assembler(filename, binary_file, log_file)
        assembler.assemble()

        os.remove(filename)
        os.remove(binary_file)
        os.remove(log_file)

        self.assertEqual(assembler.bytes[0].hex(), "241003000000")
```
### Тест чтения из памяти
```
def test_read_memory(self):
        filename = 'test_file.asm'
        binary_file = 'test_bin.bin'
        log_file = 'test_log.xml'

        with open(filename, 'w') as f:
            f.write("READ_MEMORY 58 26 198")

        assembler = Assembler(filename, binary_file, log_file)
        assembler.assemble()

        os.remove(filename)
        os.remove(binary_file)
        os.remove(log_file)

        self.assertEqual(assembler.bytes[0].hex(), "3a8d31000000")
```
### Тест записи в память
```
def test_write_memory(self):
        filename = 'test_file.asm'
        binary_file = 'test_bin.bin'
        log_file = 'test_log.xml'

        with open(filename, 'w') as f:
            f.write("WRITE_MEMORY 25 48 919")

        assembler = Assembler(filename, binary_file, log_file)
        assembler.assemble()

        os.remove(filename)
        os.remove(binary_file)
        os.remove(log_file)

        self.assertEqual(assembler.bytes[0].hex(), "19d8e5000000")
```
### Тест бинарной операции умножения
```
def test_multiply(self):
        filename = 'test_file.asm'
        binary_file = 'test_bin.bin'
        log_file = 'test_log.xml'

        with open(filename, 'w') as f:
            f.write("MUL 32 68 90 15")

        assembler = Assembler(filename, binary_file, log_file)
        assembler.assemble()

        os.remove(filename)
        os.remove(binary_file)
        os.remove(log_file)

        self.assertEqual(assembler.bytes[0].hex(), "20a2f6010000")
```
### Тест ошибки аргумента команды
```
def test_value_error(self):
        filename = 'test_file.asm'
        binary_file = 'test_bin.bin'
        log_file = 'test_log.xml'

        with open(filename, 'w') as f:
            f.write("LOAD_CONSTANT 10 10 10")

        assembler = Assembler(filename, binary_file, log_file)
        with self.assertRaisesRegex(ValueError, "Параметр А должен быть равен 36"):
            assembler.assemble()

        os.remove(filename)
```
### Тест ошибки определения команды
```
def test_syntax_error(self):
        filename = 'test_file.asm'
        binary_file = 'test_bin.bin'
        log_file = 'test_log.xml'

        with open(filename, 'w') as f:
            f.write("MOV 50")

        assembler = Assembler(filename, binary_file, log_file)
        with self.assertRaisesRegex(SyntaxError, "Неизвестная команда"):
            assembler.assemble()

        os.remove(filename)
```
## Интерпретатор
### Тест загрузки константы
```
def test_load_const(self):
        filename = 'test_file.bin'
        result_file = 'test_result.xml'

        with open(filename, 'wb') as f:
            f.write(b"\x24\x10\x03\x00\x00\x00")

        interpreter = Interpreter(filename, 0, 9181, result_file)
        interpreter.interpret()

        os.remove(filename)
        os.remove(result_file)

        self.assertEqual(interpreter.registers[32], 12)
```
### Тест чтения из памяти
```
def test_read_memory(self):
        filename = 'test_file.bin'
        result_file = 'test_result.xml'

        with open(filename, 'wb') as f:
            f.write(b"\x3a\x8d\x31\x00\x00\x00")

        interpreter = Interpreter(filename, 0, 9181, result_file)
        interpreter.interpret()

        os.remove(filename)
        os.remove(result_file)

        self.assertEqual(interpreter.registers[26], 0)
```
### Тест записи в память
```
def test_write_memory(self):
        filename = 'test_file.bin'
        result_file = 'test_result.xml'

        with open(filename, 'wb') as f:
            f.write(b"\x19\xd8\xe5\x00\x00\x00")

        interpreter = Interpreter(filename, 0, 9181, result_file)
        interpreter.interpret()

        os.remove(filename)
        os.remove(result_file)

        self.assertEqual(interpreter.registers[919], 0)
```
### Тест бинарной операции умножения
```
def test_multiply(self):
        filename = 'test_file.bin'
        result_file = 'test_result.xml'

        with open(filename, 'wb') as f:
            f.write(b"\x20\xa2\xf6\x01\x00\x00")

        interpreter = Interpreter(filename, 0, 9181, result_file)
        interpreter.interpret()

        os.remove(filename)
        os.remove(result_file)

        self.assertEqual(interpreter.registers[68], 0)
```
### Тест ошибки определения команды/аргумента
```
def test_value_error(self):
        filename = 'test_file.bin'
        result_file = 'test_result.xml'

        with open(filename, 'wb') as f:
            f.write(b"\x01\x00\x00\x00\x00\x00")

        interpreter = Interpreter(filename, 0, 9181, result_file)
        with self.assertRaisesRegex(ValueError, "В бинарном файле содержатся невалидные данные: неверный байт-код"):
            interpreter.interpret()

        os.remove(filename)

        self.assertEqual(interpreter.registers[919], 0)
```
## Результаты тестирования
![image](https://github.com/user-attachments/assets/12f47803-d419-4a91-bfa9-e5fdb387e9c1)
