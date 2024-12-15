import os
import sys
import json
import urllib.request
import subprocess

def get_dependencies(package_path, repository_url, dependencies=None, visited=None):
    if dependencies is None:
        dependencies = {}
    if visited is None:
        visited = set()

    with open(package_path, 'r') as file:
        package_data = json.load(file)
        
        package_name = package_data.get('name', '')
        package_version = package_data.get('version', '')
        package_id = f"{package_name}@{package_version}"
        
        dependencies[package_id] = []

        deps = package_data.get('dependencies', {})
        
        if package_id not in visited:
            visited.add(package_id)

            for dep_name, dep_version in deps.items():
                clean_version = dep_version.replace('^', '').replace('~', '')
                dep_id = f"{dep_name}@{clean_version}"
                
                if dep_id not in dependencies[package_id]:
                    dependencies[package_id].append(dep_id)

                if dep_id not in visited:
                    temp_dir = f"temp_{dep_name}"
                    os.makedirs(temp_dir, exist_ok=True)
                    
                    try:
                        url = f"{repository_url.rstrip('/')}/{dep_name}/{clean_version}"
                        with urllib.request.urlopen(url) as response:
                            pkg_data = json.loads(response.read())
                            
                        with open(f"{temp_dir}/package.json", 'w') as f:
                            json.dump(pkg_data, f)

                        get_dependencies(f"{temp_dir}/package.json", repository_url, dependencies, visited)

                    except Exception as e:
                        print(f"Ошибка при получении зависимостей для {dep_name}: {str(e)}")
                        dependencies[package_id].remove(dep_id)
                    
                    finally:
                        import shutil
                        shutil.rmtree(temp_dir, ignore_errors=True)

    return dependencies

def generate_plantuml_graph(dependencies):
    plantuml_code = "@startuml\n"
    plantuml_code += "skinparam defaultTextAlignment center\n"
    plantuml_code += "skinparam componentStyle uml2\n\n"

    for package, deps in dependencies.items():
        for dep in deps:
            plantuml_code += f'[{package}] --> [{dep}]\n'

    plantuml_code += "@enduml"
    return plantuml_code

def show_graph(image_path):
    if sys.platform == "win32":
        os.startfile(image_path)
    elif sys.platform == "darwin":
        subprocess.run(["open", image_path])
    else:
        subprocess.run(["xdg-open", image_path])

def visualize_dependencies(plantuml_path, package_path, repository_url):
    dependencies = get_dependencies(package_path, repository_url)
    plantuml_code = generate_plantuml_graph(dependencies)

    temp_puml = "dependency_graph.puml"
    output_png = "dependency_graph.png"
    
    with open(temp_puml, "w") as f:
        f.write(plantuml_code)

    try:
        result = subprocess.run(['java', '-jar', plantuml_path, temp_puml], 
                              capture_output=True, 
                              text=True)
        
        if result.returncode != 0:
            print(f"Ошибка при генерации графа: {result.stderr}")
            sys.exit(1)

        if not os.path.exists(output_png):
            print("Ошибка: файл графа не был создан")
            sys.exit(1)

        print(f"График сохранен в файл: {output_png}")
        show_graph(output_png)

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        sys.exit(1)
    finally:
        if os.path.exists(temp_puml):
            os.remove(temp_puml)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Использование: {sys.argv[0]} <путь_к_plantuml.jar> <путь_к_package.json> <URL_репозитория>")
        sys.exit(1)

    plantuml_path = sys.argv[1]
    package_path = sys.argv[2]
    repository_url = sys.argv[3]

    visualize_dependencies(plantuml_path, package_path, repository_url)
