import tkinter as tk
from zipfile import ZipFile
import csv
from datetime import datetime
import platform
from sys import argv, exit

class Application:
    def __init__(self, terminal):
        self.root = tk.Tk()
        self.root.title("Гнесь Я.Э.")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#000000")
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 0))
        self.output = tk.Text(frame, wrap=tk.WORD, bg="#000000", fg="#FFCC00", font=("Consolas", 10), state=tk.DISABLED)
        self.output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.output.tag_configure("input", foreground="#FFCC00")
        self.output.tag_configure("command", foreground="#FFCC00")
        self.output.tag_configure("error", foreground="#FF0000")
        self.input = tk.Entry(self.root, bg="#000000", fg="#FFCC00", font=("Consolas", 10))
        self.input.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=10)
        self.input.bind("<Return>", self.read)
        self.terminal = terminal
        self.terminal.link(self)

    def read(self, event):
        line = self.input.get().strip()
        self.input.delete(0, tk.END)
        if line:
            self.print(' ' + line, "input")
            self.terminal.command_dispatcher(line)
        else:
            self.print("", "input")

    def print(self, text, type):
        color_tag = "input" if type == "input" else "command" if type == "command" else "error"
        self.output.config(state=tk.NORMAL)
        if type == "input":
            self.output.insert(tk.END, f"{self.terminal.username}:~{self.terminal.path}${text}\n", color_tag)
        else:
            self.output.insert(tk.END, f"{text}\n", color_tag)
        self.output.config(state=tk.DISABLED)
        self.output.see(tk.END)

    def run(self):
        self.root.mainloop()

    def exit(self):
        self.root.destroy()
        exit()

class Terminal:
    def __init__(self, name, fs_path, file_system: ZipFile, log_path):
        self.username = name
        self.fs_path = fs_path
        self.filesystem = file_system
        self.log_path = log_path
        self.path = ""
        self.application = None

    def link(self, app: Application):
        self.application = app

    def log_command(self, command):
        with open(self.log_path, 'a', newline='') as log_file:
            writer = csv.writer(log_file)
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), command])

    def command_dispatcher(self, string):
        self.log_command(string)
        line = string.split()
        if line[0] == "exit":
            self.application.exit()
        elif line[0] == "ls":
            self.ls(line[1:])
        elif line[0] == "cd":
            temp_dir = self.cd(line[1:])
            if temp_dir is not None:
                self.path = temp_dir
        elif line[0] == "uname":
            self.uname()
        elif line[0] == "rev":
            self.rev(line[1:])
        elif line[0] == "touch":
            self.touch(line[1:])
        else:
            self.application.print("Работа данной команды не предусмотрена в данном эмуляторе.", "error")

    def ls(self, args):
        work_dir = self.path
        if len(args) > 0:
            work_dir = self.cd(args[-1])
            if work_dir is None:
                self.application.print("", "command")
        items = set()
        for item in self.filesystem.namelist():
            if item.startswith(work_dir):
                ls_name = item[len(work_dir):]
                if "/" in ls_name:
                    ls_name = ls_name[:ls_name.index("/")]
                items.add(ls_name)
        self.application.print('\n'.join(sorted(filter(lambda x: len(x) > 0, items))), "command")

    def cd(self, args):
        if len(args) == 0:
            return ""
        directory = args[-1]
        directory = directory.strip('/')
        directory = directory.split('/')
        new_dir = self.path[:-1].split('/')
        if new_dir == [""]:
            new_dir = []
        for arg in directory:
            if arg == "..":
                if len(new_dir) > 0:
                    new_dir.pop()
                else:
                    self.application.print("Некорректный путь к директории.", "error")
                    return
            else:
                new_dir.append(arg)
        new_path = "/".join(new_dir) + "/"
        if new_path == "/":
            return ""
        for file in self.filesystem.namelist():
            if file.startswith(new_path):
                return new_path
        self.application.print("Директория с таким названием отсутствует.", "error")

    def uname(self):
        system_info = platform.uname()
        self.application.print(f"{system_info.system} {system_info.node} {system_info.release}", "command")

    def rev(self, args):
        if len(args) > 0:
            text = " ".join(args)
            self.application.print(text[::-1], "command")
        else:
            self.application.print("Не указан текст для разворота.", "error")

    def touch(self, args):
        if len(args) > 0:
            filename = args[-1]
            unique_filename = filename
            counter = 1
            while f"{self.path}{unique_filename}" in self.filesystem.namelist():
                unique_filename = f"{filename.split('.')[0]}_{counter}.{filename.split('.')[-1]}"
                counter += 1
            try:
                self.filesystem.writestr(f"{self.path}{unique_filename}", "")
            except:
                self.application.print("Не удалось создать файл.", "error")
        else:
            self.application.print("Не указано имя файла.", "error")

def main():
    if len(argv) > 1:
        config_file = argv[1]
        try:
            with open(config_file, "r", encoding="UTF-8") as file:
                csv_reader = csv.reader(file)
                username = next(csv_reader)[0]
                filesystem_path = next(csv_reader)[0]
                log_path = next(csv_reader)[0]
                with ZipFile(filesystem_path, 'a') as file_system:
                    Application(Terminal(username, filesystem_path, file_system, log_path)).run()
        except FileNotFoundError:
            print(f"Файл {config_file} не найден.")
    else:
        print("Аргументы не были переданы.")

if __name__ == "__main__":
    main()
