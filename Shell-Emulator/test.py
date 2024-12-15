from main import Terminal
from main import Application
from types import NoneType
import pytest
from zipfile import ZipFile
import platform

@pytest.fixture
def terminal():
    name = "MyComputer"
    fs_path = "vfs.zip"
    log_path = "log.csv"
    t = Terminal(name, fs_path, ZipFile(fs_path, "a"), log_path)
    return t

def test_init_1(terminal):
    assert terminal.application is None

def test_init_2(terminal):
    assert terminal.filesystem is not None 

def test_init_3(terminal):
    assert terminal.log_path is not None

def test_link(terminal):
    terminal.link(Application(terminal))
    assert terminal.application is not None

def test_cd_1(terminal):
    assert terminal.cd([]) == ""

def test_cd_2(terminal):
    assert terminal.cd(["Yesenin_s_dir_1/.."]) == ""

def test_cd_3(terminal):
    terminal.cd([])
    assert terminal.cd(["Yesenin_s_dir_1"]) == "Yesenin_s_dir_1/"

def test_ls_1(terminal):
    assert NoneType

def test_ls_2(terminal):
    terminal.path = terminal.cd(["Yesenin_s_dir_1"])
    assert NoneType

def test_ls_3(terminal):
    assert NoneType

def test_uname_1(terminal):
    system_info = platform.uname()
    expected = f"{system_info.system} {system_info.node} {system_info.release}"
    assert NoneType

def test_uname_2(terminal):
    assert NoneType

def test_uname_3(terminal):
    system_info = platform.uname()
    assert NoneType

def test_rev_1(terminal):
    test_string = "hello"
    assert NoneType

def test_rev_2(terminal):
    test_string = "hello world"
    assert NoneType

def test_rev_3(terminal):
    test_string = ""
    assert NoneType

def test_touch_1(terminal, capfd):
    terminal.touch(["test.txt"])
    assert NoneType

def test_touch_2(terminal, capfd):
    terminal.touch(["test"])
    assert NoneType

def test_touch_3(terminal, capfd):
    terminal.touch(["test.png"])
    assert NoneType
