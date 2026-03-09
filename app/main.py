import os
import sys
import shutil
import subprocess
from pathlib import Path

class Shell:
    
    def __init__(self) -> None:
        
        self.working_directory: Path = Path.cwd()
        self.builtin_commands = {
            "echo": self.echo,
            "exit": self.exit,
            "type": self.type,
            "pwd": self.pwd,
            "cd": self.cd,
            "ls": self.ls
            }

    def exit(self, args: list[str]) -> None:
        sys.exit(0)

    def echo(self, args: list[str]) -> None:
        print(" ".join(args))

    def type(self, args: list[str]) -> None:
        cmd = args[0]
        if cmd in self.builtin_commands:
            print(f"{cmd} is a shell builtin")
        elif path := shutil.which(cmd):
            print(f"{cmd} is {path}")
        else:
            print(f"{cmd}: not found")
    
    def pwd(self, args: list[str]):
        print(self.working_directory)

    def cd(self, args: list[str]):
        if target := Path(args[0]):
            if target.is_absolute():
                self.working_directory = target
            else:
                self.working_directory = os.path.join(self.working_directory, target)
        else:
            print(f"cd: {args[0]}: No such file or directory.")

    def ls(self, args: list[str]):
        print(os.listdir(self.working_directory))

    def __run_external(self, path: str, args: list[str]):
        try:
            cmd = path.split("/")[-1]
            subprocess.run([cmd] + args)
        except Exception as e:
            print(f"Error executing {path}: {e}")
        
    def run(self):
        """Main shell REPL loop."""
        while True:
            sys.stdout.write("$ ")
            sys.stdout.flush()
            
            user_input = input().strip()
            if not user_input:
                continue

            cmd_args = user_input.split(" ")
            cmd = cmd_args[0]
            args = cmd_args[1:]

            if cmd in self.builtin_commands:
                self.builtin_commands[cmd](args)

            elif path := shutil.which(cmd):
                self.__run_external(path, args)
                
            else:
                print(f"{cmd}: command not found")
            
def main():
    s = Shell()
    s.run()

if __name__ == "__main__":
    main()
