import os
import pytest
import sys

from assembler import Assembler
from interpreter import Interpreter

def test_assembler_class_import():
    """Test that Assembler class can be imported and instantiated"""
    assert Assembler is not None, "Assembler class could not be imported"
    
    # Test basic instantiation
    test_assembler = Assembler(
        path_to_code='input.asm', 
        path_to_binary_file='output.bin', 
        path_to_log='log.yaml'
    )
    assert test_assembler is not None, "Could not create Assembler instance"

def test_interpreter_class_import():
    """Test that Interpreter class can be imported and instantiated"""
    assert Interpreter is not None, "Interpreter class could not be imported"
    
    # Test basic instantiation
    test_interpreter = Interpreter(
        path_to_binary_file='output.bin', 
        left_boundary=0, 
        right_boundary=8, 
        path_to_result_file='output.yaml'
    )
    assert test_interpreter is not None, "Could not create Interpreter instance"

def test_assembler_methods():
    """Test key methods of Assembler class"""
    test_assembler = Assembler(
        path_to_code='input.asm', 
        path_to_binary_file='output.bin', 
        path_to_log='log.yaml'
    )
    
    # Test encode_instruction method
    encoded = test_assembler.encode_instruction(1, 0, 42)
    assert encoded is not None, "encode_instruction failed"
    assert len(encoded) == 3, "Encoded instruction should be 3 bytes"

def test_interpreter_methods():
    """Test key methods of Interpreter class"""
    test_interpreter = Interpreter(
        path_to_binary_file='output.bin', 
        left_boundary=0, 
        right_boundary=8, 
        path_to_result_file='output.yaml'
    )
    
    # Ensure interpret method exists
    assert hasattr(test_interpreter, 'interpret'), "Interpreter missing interpret method"
    assert hasattr(test_interpreter, 'make_result'), "Interpreter missing make_result method"

def test_workflow():
    """Test basic workflow of assembler and interpreter"""
    # Assembler step
    assembler = Assembler(
        path_to_code='input.asm', 
        path_to_binary_file='output.bin', 
        path_to_log='log.yaml'
    )
    assembler.assemble()
    
    # Verify binary file was created
    assert os.path.exists('output.bin'), "Binary file not created"
    
    # Interpreter step
    interpreter = Interpreter(
        path_to_binary_file='output.bin', 
        left_boundary=0, 
        right_boundary=8, 
        path_to_result_file='output.yaml'
    )
    interpreter.interpret()
    
    # Verify result file was created
    assert os.path.exists('output.yaml'), "Result file not created"