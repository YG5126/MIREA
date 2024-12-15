import pytest
import json
import os
from unittest.mock import patch, mock_open, MagicMock
from main import (
    get_dependencies,
    generate_plantuml_graph,
    show_graph,
    visualize_dependencies
)

@pytest.fixture
def sample_package_json():
    return {
        "name": "test-package",
        "version": "1.0.0",
        "dependencies": {
            "dep1": "^1.0.0",
            "dep2": "~2.0.0"
        }
    }

@pytest.fixture
def sample_dependencies():
    return {
        "test-package@1.0.0": ["dep1@1.0.0", "dep2@2.0.0"]
    }

def test_get_dependencies_empty_deps():
    """Тест функции get_dependencies с пустым списком зависимостей"""
    mock_data = {
        "name": "test-package",
        "version": "1.0.0",
        "dependencies": {}
    }
    
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        result = get_dependencies("fake_path.json", "https://registry.npmjs.org")
        assert result == {"test-package@1.0.0": []}

def test_get_dependencies_with_network_error(sample_package_json):
    """Тест функции get_dependencies при ошибке сети"""
    with patch("builtins.open", mock_open(read_data=json.dumps(sample_package_json))):
        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_urlopen.side_effect = Exception("Network error")
            
            result = get_dependencies("fake_path.json", "https://registry.npmjs.org")
            assert result == {"test-package@1.0.0": []}

def test_generate_plantuml_graph_empty():
    """Тест генерации пустого PlantUML графа"""
    result = generate_plantuml_graph({})
    assert "@startuml" in result
    assert "@enduml" in result
    assert "skinparam" in result

def test_generate_plantuml_graph_with_deps(sample_dependencies):
    """Тест генерации PlantUML графа с зависимостями"""
    result = generate_plantuml_graph(sample_dependencies)
    assert "[test-package@1.0.0] --> [dep1@1.0.0]" in result
    assert "[test-package@1.0.0] --> [dep2@2.0.0]" in result

@pytest.mark.parametrize("platform,expected_command", [
    ("win32", "os.startfile"),
    ("darwin", ["open"]),
    ("linux", ["xdg-open"])
])
def test_show_graph(platform, expected_command):
    """Тест функции show_graph для разных платформ"""
    with patch("sys.platform", platform):
        if platform == "win32":
            with patch("os.startfile") as mock_startfile:
                show_graph("test.png")
                mock_startfile.assert_called_once_with("test.png")
        else:
            with patch("subprocess.run") as mock_run:
                show_graph("test.png")
                expected_cmd = ["open"] if platform == "darwin" else ["xdg-open"]
                mock_run.assert_called_once_with(expected_cmd + ["test.png"])

def test_visualize_dependencies_plantuml_error(sample_dependencies):
    """Тест обработки ошибки PlantUML"""
    with patch("main.get_dependencies") as mock_get_deps:
        with patch("subprocess.run") as mock_run:
            mock_get_deps.return_value = sample_dependencies
            mock_run.return_value.returncode = 1
            mock_run.return_value.stderr = "PlantUML error"
            
            with patch("builtins.open", mock_open()):
                with pytest.raises(SystemExit):
                    visualize_dependencies("plantuml.jar", "package.json", "https://registry.npmjs.org")

def test_visualize_dependencies_no_output_file(sample_dependencies):
    """Тест обработки отсутствия выходного файла"""
    with patch("main.get_dependencies") as mock_get_deps:
        with patch("subprocess.run") as mock_run:
            with patch("os.path.exists") as mock_exists:
                mock_get_deps.return_value = sample_dependencies
                mock_run.return_value.returncode = 0
                mock_exists.return_value = False
                
                with patch("builtins.open", mock_open()):
                    with pytest.raises(SystemExit):
                        visualize_dependencies("plantuml.jar", "package.json", "https://registry.npmjs.org")
