import argparse
import yaml

class Interpreter:
    def __init__(self, path_to_binary_file, left_boundary, right_boundary, path_to_result_file):
        self.result_path = path_to_result_file
        self.boundaries = (left_boundary, right_boundary)
        self.registers = [0] * (right_boundary - left_boundary + 1)

        with open(path_to_binary_file, 'rb') as binary_file:
            self.byte_code = binary_file.read()
            self.byte_code_index = 0

    def interpret(self):
        while self.byte_code_index < len(self.byte_code):
            if self.byte_code_index + 3 > len(self.byte_code):
                break

            instruction_bytes = self.byte_code[self.byte_code_index:self.byte_code_index + 3]
            self.byte_code_index += 3

            instruction = int.from_bytes(instruction_bytes, byteorder="little")

            a = instruction & 0b111
            
            if a == 1:  # LOAD_CONSTANT
                B = (instruction >> 3) & 0b111
                C = (instruction >> 6) & 0b111111111111111111
                if self.boundaries[0] <= B <= self.boundaries[1]:
                    self.registers[B - self.boundaries[0]] = C
                    
            elif a == 7:  # READ_MEMORY
                B = (instruction >> 3) & 0b111
                C = (instruction >> 6) & 0b111111
                D = (instruction >> 12) & 0b111
                if all(self.boundaries[0] <= reg <= self.boundaries[1] for reg in [B, D]):
                    self.registers[D - self.boundaries[0]] = self.registers[B - self.boundaries[0]] + C

            elif a == 3:  # WRITE_MEMORY
                B = (instruction >> 3) & 0b111
                C = (instruction >> 6) & 0b111
                if all(self.boundaries[0] <= reg <= self.boundaries[1] for reg in [B, C]):
                    self.registers[C - self.boundaries[0]] = self.registers[B - self.boundaries[0]]

            elif a == 5:  # UNARY_MINUS
                B = (instruction >> 3) & 0b111
                C = (instruction >> 6) & 0b111
                if all(self.boundaries[0] <= reg <= self.boundaries[1] for reg in [B, C]):
                    self.registers[C - self.boundaries[0]] = -self.registers[B - self.boundaries[0]]

        self.make_result()

    def make_result(self):
        result_entries = [
            {'address': pos, 'value': register} 
            for pos, register in enumerate(self.registers, self.boundaries[0]) 
            if register != 0
        ]

        with open(self.result_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(result_entries, f, allow_unicode=True, default_flow_style=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Входной бинарный файл")
    parser.add_argument("output", help="Выходной YAML файл")
    parser.add_argument("-lb", "--left_boundary", help="Левая граница памяти", default=0, type=int)
    parser.add_argument("-rb", "--right_boundary", help="Правая граница памяти", default=8, type=int)
    args = parser.parse_args()

    interpreter = Interpreter(args.input, args.left_boundary, args.right_boundary, args.output)
    try:
        interpreter.interpret()
    except Exception as e:
        print(f"Ошибка при интерпретации: {e}")
    print(f"Интерпретация выполнена. Результаты сохранены в {args.output}")