import argparse
import yaml

class Assembler:
    def __init__(self, path_to_code, path_to_binary_file, path_to_log):
        self.binary_file_path = path_to_binary_file
        self.code_path = path_to_code
        self.log_path = path_to_log

        self.bytes = []
        self.log_entries = []

    def encode_instruction(self, A, B, C, D=None):
        """
        Кодирование инструкции в 3 байта
        A - код операции (3 бита)
        B - первый регистр (3 бита)
        C - второй регистр или константа (18 бит)
        D - дополнительный регистр для некоторых инструкций (опционально)
        """
        # Проверяем корректность параметров
        if not (0 <= A < 8):
            raise ValueError(f"Недопустимый код операции A: {A}")
        if not (0 <= B < 8):
            raise ValueError(f"Недопустимый адрес регистра B: {B}")
        if not (0 <= C < (1 << 18)):
            raise ValueError(f"Недопустимое значение константы C: {C}")
        
        if D is not None:
            # Для инструкций с 4 параметрами (READ_MEMORY)
            if not (0 <= D < 8):
                raise ValueError(f"Недопустимый адрес регистра D: {D}")
            bits = (D << 12) | (C << 6) | (B << 3) | A
        else:
            # Для инструкций с 3 параметрами
            bits = (C << 6) | (B << 3) | A
        
        # Преобразуем в 3 байта с учетом little-endian
        return bits.to_bytes(3, byteorder="little")

    def assemble(self):
        with open(self.code_path, "rt", encoding='utf-8') as code:
            for line_num, line in enumerate(code, 1):
                # Удаление комментариев и лишних пробелов
                line = line.split('#')[0].strip()
                
                # Пропуск пустых строк
                if not line: 
                    continue

                try:
                    command, *args = line.split()

                    match command:
                        case "LOAD_CONSTANT":
                            if len(args) != 3:
                                raise SyntaxError(
                                    f"Строка {line_num}: У операции загрузки константы должно быть 3 аргумента")
                            self.bytes.append(self.load_constant(int(args[0]), int(args[1]), int(args[2])))

                        case "READ_MEMORY":
                            if len(args) != 4:
                                raise SyntaxError(
                                    f"Строка {line_num}: У операции чтения из памяти должно быть 4 аргумента")
                            self.bytes.append(self.read_memory(int(args[0]), int(args[1]), int(args[2]), int(args[3])))

                        case "WRITE_MEMORY":
                            if len(args) != 3:
                                raise SyntaxError(
                                    f"Строка {line_num}: У операции записи в память должно быть 3 аргумента")
                            self.bytes.append(self.write_memory(int(args[0]), int(args[1]), int(args[2])))

                        case "UNARY_MINUS":
                            if len(args) != 3:
                                raise SyntaxError(
                                    f"Строка {line_num}: У операции унарного минуса должно быть 3 аргумента")
                            self.bytes.append(self.unary_minus(int(args[0]), int(args[1]), int(args[2])))

                        case _:
                            raise SyntaxError(f"Строка {line_num}: Неизвестная команда: {line}")

                except (ValueError, SyntaxError) as e:
                    print(f"Ошибка при ассемблировании: {e}")
                    return

        self.to_binary_file()
        self.to_yaml_log()

    def load_constant(self, A, B, C):
        if A != 1:
            raise ValueError("Параметр А должен быть равен 1")
        if not (0 <= B < 8):
            raise ValueError("Адрес B должен быть в пределах от 0 до 7")
        if not (0 <= C < (1 << 18)):
            raise ValueError("Константа C должна быть в пределах от 0 до 2^18-1")

        bits_bytes = self.encode_instruction(A, B, C)

        self.log_entries.append({
            'instruction': 'LOAD_CONSTANT',
            'A': A, 'B': B, 'C': C,
            'hex': bits_bytes.hex()
        })

        return bits_bytes

    def read_memory(self, A, B, C, D):
        if A != 7:
            raise ValueError("Параметр А должен быть равен 7")
        if not (0 <= B < 8):
            raise ValueError("Адрес B должен быть в пределах от 0 до 7")
        if not (0 <= C < 64):
            raise ValueError("Смещение C должно быть в пределах от 0 до 63")
        if not (0 <= D < 8):
            raise ValueError("Адрес D должен быть в пределах от 0 до 7")

        bits_bytes = self.encode_instruction(A, B, C, D)

        self.log_entries.append({
            'instruction': 'READ_MEMORY',
            'A': A, 'B': B, 'C': C, 'D': D,
            'hex': bits_bytes.hex()
        })

        return bits_bytes

    def write_memory(self, A, B, C):
        if A != 3:
            raise ValueError("Параметр А должен быть равен 3")
        if not (0 <= B < 8):
            raise ValueError("Адрес B должен быть в пределах от 0 до 7")
        if not (0 <= C < 8):
            raise ValueError("Адрес C должен быть в пределах от 0 до 7")

        bits_bytes = self.encode_instruction(A, B, C)

        self.log_entries.append({
            'instruction': 'WRITE_MEMORY',
            'A': A, 'B': B, 'C': C,
            'hex': bits_bytes.hex()
        })

        return bits_bytes

    def unary_minus(self, A, B, C):
        if A != 5:
            raise ValueError("Параметр А должен быть равен 5")
        if not (0 <= B < 8):
            raise ValueError("Адрес B должен быть в пределах от 0 до 7")
        if not (0 <= C < 8):
            raise ValueError("Адрес C должен быть в пределах от 0 до 7")

        bits_bytes = self.encode_instruction(A, B, C)

        self.log_entries.append({
            'instruction': 'UNARY_MINUS',
            'A': A, 'B': B, 'C': C,
            'hex': bits_bytes.hex()
        })

        return bits_bytes

    def to_binary_file(self):
        with open(self.binary_file_path, "wb") as binary:
            for byte in self.bytes:
                binary.write(byte)

    def to_yaml_log(self):
        # Если лог-файл не указан, не создаем его
        if not self.log_path:
            return

        # Проверяем, есть ли записи в логе
        if not self.log_entries:
            print("Предупреждение: Нет записей для логирования")
            return

        try:
            with open(self.log_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(self.log_entries, f, allow_unicode=True, default_flow_style=False)
            print(f"Лог-файл успешно создан: {self.log_path}")
        except Exception as e:
            print(f"Ошибка при создании лог-файла: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Входной файл (.asm)")
    parser.add_argument("output", help="Выходной файл (.bin)")
    parser.add_argument("-l", "--log", help="Файл лога (.yaml)", default=None)
    args = parser.parse_args()

    assembler = Assembler(args.input, args.output, args.log)
    try:
        assembler.assemble()
    except ValueError as e:
        print(e)
    print(f"Ассемблирование выполнено успешно. Выходной файл: {args.output}")