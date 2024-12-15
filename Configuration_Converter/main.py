import sys
import yaml
from lark import Lark, Transformer, exceptions, LarkError, Tree

# Грамматика конфигурационного языка
grammar = """
start: (const_decl | COMMENT)* config

COMMENT: "***>" /.+/

config: NAME conf
conf: "{" [pair ("," pair)*] "}"

const_decl: "set" NAME "=" value
const_eval: "$" operation "$"

operation: "+" NAME NUMBER -> add_op
        | "chr" "(" NUMBER ")" -> chr_op
        | "mod" "(" NUMBER "," NUMBER ")" -> mod_op

value: NUMBER | STRING | array | const_eval

array: "#(" [value*] ")"
pair: NAME "=" value

NAME: /[_a-zA-Z]+/
STRING: "[[" /[^\\[\\]]*/ "]]"

%import common.NUMBER
%import common.WS
%ignore WS
%ignore COMMENT
"""

# Инициализация Lark парсера
config_parser = Lark(grammar)

class ConfigTransformer(Transformer):
    def __init__(self):
        super().__init__()
        self.constants = {}  # Хранилище для констант

    def start(self, value):
        return value[-1]

    def const_decl(self, tupl):
        name, value = tupl
        if name in self.constants:
            raise LarkError(f"Константа {name} уже объявлена")
        self.constants[name] = value
        return None

    def add_op(self, items):
        name, number = items
        if name not in self.constants:
            raise ValueError(f"Неизвестная константа {name}")
        return self.constants[name] + int(number)

    def chr_op(self, items):
        number = int(items[0])
        return chr(number)

    def mod_op(self, items):
        a, b = int(items[0]), int(items[1])
        return a % b

    def const_eval(self, items):
        return items[0]

    def config(self, value):
        name, conf = value
        return {name: conf}

    def pair(self, value):
        key, val = value
        return (key, val)

    def array(self, items):
        return [item for item in items if item is not None]

    def STRING(self, token):
        return str(token)[2:-2]

    def NUMBER(self, token):
        return int(token)

    def NAME(self, token):
        return str(token)

    def value(self, tupl):
        val = tupl[0]
        if isinstance(val, Tree):
            return self.transform(val)
        return val

    def conf(self, items):
        result = {}
        for item in items:
            if item is not None:
                key, value = item
                result[key] = value
        return result

# Функция для парсинга и обработки ошибок
def parse_config(input_text):
    try:
        # Парсинг входного текста
        tree = config_parser.parse(input_text)

        # Преобразование дерева в словарь
        transformer = ConfigTransformer()
        yaml_dict = transformer.transform(tree)
        return yaml_dict
    except exceptions.UnexpectedCharacters as uc:
        return f"Ошибка в синтаксисе:\n{str(uc)}"
    except exceptions.LarkError as le:
        return f"Ошибка при обработке:\n{str(le)}"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python config_converter.py <выходной_файл.yaml>")
        sys.exit(1)
    output_filename = sys.argv[1]
    input_text = sys.stdin.read()
    yaml_dict = parse_config(input_text)
    
    # Записываем результат в YAML файл
    with open(output_filename, 'w', encoding='utf-8') as f:
        yaml.dump(yaml_dict, f, allow_unicode=True, sort_keys=False)
