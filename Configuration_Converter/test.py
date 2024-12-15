import pytest
from main import parse_config

def test_simple_config():
    input_text = '''root {
        number = 13
    }'''
    expected_output = {'root': {'number': 13}}
    assert parse_config(input_text) == expected_output

def test_array():
    input_text = '''root {
        numbers = #(1 2 3)
    }'''
    expected_output = {'root': {'numbers': [1, 2, 3]}}
    assert parse_config(input_text) == expected_output

def test_string():
    input_text = '''root {
        text = [[Привет, мир!]]
    }'''
    expected_output = {'root': {'text': 'Привет, мир!'}}
    assert parse_config(input_text) == expected_output

def test_constant():
    input_text = '''set x = 5
    root {
        value = $+ x 3$
    }'''
    expected_output = {'root': {'value': 8}}
    assert parse_config(input_text) == expected_output

def test_chr_operation():
    input_text = '''root {
        letter = $chr(65)$
    }'''
    expected_output = {'root': {'letter': 'A'}}
    assert parse_config(input_text) == expected_output

def test_mod_operation():
    input_text = '''root {
        remainder = $mod(7,3)$
    }'''
    expected_output = {'root': {'remainder': 1}}
    assert parse_config(input_text) == expected_output

def test_comment():
    input_text = '''***> Это комментарий
    root {
        number = 10
    }'''
    expected_output = {'root': {'number': 10}}
    assert parse_config(input_text) == expected_output

def test_complex_config():
    input_text = '''set base = 5
    root {
        numbers = #(1 2 3),
        text = [[Hello]],
        calc = $+ base 3$,
        letter = $chr(66)$,
        mod = $mod(8,3)$
    }'''
    expected_output = {
        'root': {
            'numbers': [1, 2, 3],
            'text': 'Hello',
            'calc': 8,
            'letter': 'B',
            'mod': 2
        }
    }
    assert parse_config(input_text) == expected_output

def test_syntax_error():
    input_text = '''root {
        value = unknown_value
    }'''
    result = parse_config(input_text)
    assert "Ошибка в синтаксисе" in result

def test_undefined_constant_error():
    input_text = '''root {
        value = $+ undefined_constant 1$
    }'''
    result = parse_config(input_text)
    assert "Неизвестная константа" in result

def test_duplicate_constant_error():
    input_text = '''set x = 5
    set x = 10
    root {
        value = $+ x 1$
    }'''
    result = parse_config(input_text)
    assert "Константа x уже объявлена" in result
