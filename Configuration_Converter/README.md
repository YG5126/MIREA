# Общее описание
### Задание
Разработать инструмент командной строки для учебного конфигурационного языка, синтаксис которого приведен далее. Этот инструмент преобразует текст из 
входного формата в выходной. Синтаксические ошибки выявляются с выдачей сообщений. 

Входной текст на **учебном конфигурационном языке** принимается из стандартного ввода. Выходной текст на **языке yaml** попадает в файл, путь к которому задан ключом командной строки. 
### Синтаксис учебного конфигурационного языка
Массивы:
```
#( значение значение значение ... )
```
Имена:
```
[_a-zA-Z]+
```
Значения:
```
• Числа.
• Строки.
• Массивы.
```
Строки:
```
[[Это строка]]
```
Объявление константы на этапе трансляции:
```
set имя = значение
```
Вычисление константного выражения на этапе трансляции (префиксная
форма), пример:
```
$+ имя 1$
```
Результатом вычисления константного выражения является значение.
Для константных вычислений определены операции и функции:
```
1. Сложение.
2. chr().
3. mod().
```
Все конструкции учебного конфигурационного языка (с учетом их возможной вложенности) должны быть покрыты тестами. Необходимо показать 2 примера описания конфигураций из разных предметных областей.
# Реализованный функционал
### grammar
Определяет синтаксические правила:

 - Комментарии
 - Структуры конфигурации
 - Объявление констант
 - Массивы
 - Поддерживаемые операции

### ConfigTransformer
 - Преобразует синтаксическое дерево в словарь Python
 - Управляет объявлениями и вычислениями констант
 - Поддерживает операции:

	• Сложение констант
	• Преобразование числа в символ
	• Вычисление модуля
### parse_config
 - Конвертирует входной текст конфигурации в YAML
 - Обрабатывает синтаксические ошибки
 - Записывает результат в указанный файл
### main
Выполняется парсинг аргументов командной строки. Считывается конфигурация на учебном конфигурационном языке из стандартного потока ввода. Вызываются поочередно функции получения строки на языке yaml и получения отформатированной строки на языке yaml. Отформатированная строка записывается в файл, указанный ключом командной строки.
# Сборка и запуск проекта
1. Загрузка репозитория на компьютер
```
git clone https://github.com/YG5126/MIREA/tree/main/Configuration_Converter
```
2. Преход в директорию репозитория
```
cd Configuration_Converter
```
3. Установка библиотеки парсинга Lark
```
pip install PyYAML
```
4. Запустить main.py с указанием имени yaml файла
```
py main.py test.yaml
```
5. Ввод конфигурации в командную строку. Для завершения ввода использовать ctrl + Z
# Примеры работы программы
### Конфигурация сетевой службы
**Входные данные:**
```
***> Network Service Configuration
set PORT = 8080
set MAX_CONNECTIONS = 1010

NetworkService {
    host = [[localhost]],
    port = $+ PORT 0$,
    max_connections = $mod(1010,3)$,
    allowed_protocols = #([[http]] [[https]]),
    description = [[Primary Web Service]]
}
```
**Выходные данные (YAML):**
```
NetworkService:
  host: localhost
  port: 8080
  max_connections: 2
  allowed_protocols:
  - http
  - https
  description: Primary Web Service
```
### Конфигурация игрового персонажа
**Входные данные:**
```
***> RPG Character Configuration
set BASE_HEALTH = 100
set STRENGTH_MODIFIER = 50

GameCharacter {
    name = [[Warrior]],
    health = $+ BASE_HEALTH 0$,
    strength = $+ STRENGTH_MODIFIER 5$,
    skills = #([[sword_fighting archery]]),
    race = [[Human]],
    special_ability = [[Critical Strike]]
}
```
**Выходные данные (YAML):**
```
GameCharacter:
  name: Warrior
  health: 100
  strength: 55
  skills:
  - sword_fighting archery
  race: Human
  special_ability: Critical Strike
```
### Конфигурация научного эксперимента
**Входные данные:**
```
***> Experimental Setup
set SAMPLE_SIZE = 50
set TEMPERATURE = 20

ExperimentConfig {
    experiment_type = [[Chemical Reaction]],
    sample_count = $+ SAMPLE_SIZE 0$,
    temperature = $+ TEMPERATURE 20$,
    chemicals = #([[hydrogen]] [[oxygen]] [[nitrogen]]),
    safety_level = [[High]],
    notes = [[Precise measurements required]]
}
```
**Выходные данные (YAML):**
```
ExperimentConfig:
  experiment_type: Chemical Reaction
  sample_count: 50
  temperature: 40
  chemicals:
  - hydrogen
  - oxygen
  - nitrogen
  safety_level: High
  notes: Precise measurements required
```
# Общие тесты
![image](https://github.com/YG5126/MIREA/blob/main/Configuration_Converter/Common_test.png)
