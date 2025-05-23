from colorama import Fore, Style, init
init(autoreset=True)

class TextFile:
    def __init__(self, name):
        self.name = name
        self.lines = []

    def write(self):
        print(Fore.MAGENTA + "Enter lines (type /end/ to finish):")
        self.lines = []
        while True:
            line = input()
            if line == "/end/":
                break
            for ch in [line]:
                self.lines.append(ch)

    def append(self):
        print(Fore.MAGENTA + "Appending to file (type /end/ to finish):")
        while True:
            line = input()
            if line == "/end/":
                break
            for l in [line]:
                self.lines.append(l)

    def show(self):
        for line in self.lines:
            print(Fore.CYAN + line)

    def edit_line(self, index, new_text):
        if 0 <= index < len(self.lines):
            self.lines[index] = new_text
            return True
        print(Fore.RED + "Invalid line number")
        return False

    def delete_line(self, index):
        if 0 <= index < len(self.lines):
            new_lines = []
            for i in range(len(self.lines)):
                if i != index:
                    new_lines.append(self.lines[i])
            self.lines = new_lines
            return True
        print(Fore.RED + "Invalid line number")
        return False

class Directory:
    def __init__(self, name):
        self.name = name
        self.subdirs = {}
        self.files = {}

class FileSystem:
    def __init__(self):
        self.root = Directory("/")
        self.current = self.root
        self.path = [self.root]

    def find_dir(self, path):
        if path == "/":
            return self.root
        parts = path.strip("/").split("/")
        if path.startswith("/"):
            node = self.root
        else:
            node = self.current
        for p in parts:
            if p == "..":
                if len(self.path) > 1:
                    self.path.pop()
                    node = self.path[-1]
            elif p in node.subdirs:
                node = node.subdirs[p]
            else:
                print(Fore.RED + "Path not found")
                return None
        return node

    def mkdir(self, path, name):
        dir = self.find_dir(path)
        if dir and name not in dir.subdirs:
            dir.subdirs[name] = Directory(name)
        else:
            print(Fore.YELLOW + "Directory already exists or invalid path")

    def touch(self, path, name):
        dir = self.find_dir(path)
        if dir and name not in dir.files:
            tf = TextFile(name)
            tf.name = "".join([c for c in name])
            dir.files[name] = tf
        else:
            print(Fore.YELLOW + "File already exists or invalid path")

    def rm(self, path):
        parts = path.strip("/").split("/")
        name = parts[-1]
        dir = self.find_dir("/".join(parts[:-1]))
        if dir:
            if name in dir.files:
                del dir.files[name]
            elif name in dir.subdirs:
                del dir.subdirs[name]
            else:
                print(Fore.RED + "Item not found")

    def cd(self, path):
        dir = self.find_dir(path)
        if dir:
            self.current = dir
            self.path.append(dir)

    def back(self):
        if len(self.path) > 1:
            self.path.pop()
            self.current = self.path[-1]
        else:
            print(Fore.YELLOW + "Already at root directory")

    def ls(self):
        dirs = []
        for d in self.current.subdirs:
            dirs.append(d)
        files = []
        for f in self.current.files:
            files.append(f)
        print(Fore.GREEN + "Directories:", dirs)
        print(Fore.BLUE + "Files:", files)

    def get_file(self, path):
        parts = path.strip("/").split("/")
        name = parts[-1]
        dir = self.find_dir("/".join(parts[:-1]))
        if dir and name in dir.files:
            return dir.files[name]
        else:
            print(Fore.RED + "File not found")
            return None

    def rename(self, path, new_name):
        parts = path.strip("/").split("/")
        name = parts[-1]
        dir = self.find_dir("/".join(parts[:-1]))
        if dir:
            if name in dir.files:
                file_obj = dir.files.pop(name)
                file_obj.name = new_name
                dir.files[new_name] = file_obj
            elif name in dir.subdirs:
                subdir_obj = dir.subdirs.pop(name)
                subdir_obj.name = new_name
                dir.subdirs[new_name] = subdir_obj
            else:
                print(Fore.RED + "Item not found")

fs = FileSystem()

cmd = input(Fore.LIGHTWHITE_EX + "$ ").strip().split()
while cmd and cmd[0] != "exit":
    try:
        if cmd[0] == "mkdir":
            fs.mkdir(cmd[1], cmd[2])
        elif cmd[0] == "touch":
            fs.touch(cmd[1], cmd[2])
        elif cmd[0] == "rm":
            fs.rm(cmd[1])
        elif cmd[0] == "cd":
            if cmd[1] == "..":
                fs.back()
            else:
                fs.cd(cmd[1])
        elif cmd[0] == "ls":
            fs.ls()
        elif cmd[0] == "nwfiletxt":
            f = fs.get_file(cmd[1])
            if f:
                f.write()
        elif cmd[0] == "appendtxt":
            f = fs.get_file(cmd[1])
            if f:
                f.append()
        elif cmd[0] == "cat":
            f = fs.get_file(cmd[1])
            if f:
                f.show()
        elif cmd[0] == "editline":
            f = fs.get_file(cmd[1])
            if f:
                f.edit_line(int(cmd[2]), " ".join(cmd[3:]))
        elif cmd[0] == "deline":
            f = fs.get_file(cmd[1])
            if f:
                f.delete_line(int(cmd[2]))
        elif cmd[0] == "rename":
            fs.rename(cmd[1], cmd[2])
        else:
            print(Fore.RED + "Unknown command")
    except Exception as e:
        print(Fore.RED + "Error:", e)
    cmd = input(Fore.LIGHTWHITE_EX + "$ ").strip().split()