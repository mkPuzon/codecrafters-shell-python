import sys
import shlex
import shutil
import subprocess
from pathlib import Path

import app.builtins 
from app.registry import BUILTIN_COMMANDS

class Shell:
    
    def __init__(self) -> None:
        
        self.working_directory: Path = Path.cwd()
        self.BUILTINS = BUILTIN_COMMANDS


    # def type(self, args: list[str]) -> None:
    #     cmd = args[0]
    #     if cmd in self.builtin_commands:
    #         print(f"{cmd} is a shell builtin")
    #     elif path := shutil.which(cmd):
    #         print(f"{cmd} is {path}")
    #     else:
    #         print(f"{cmd}: not found")
    
    # def pwd(self, args: list[str]):
    #     print(self.working_directory)

    # def cd(self, args: list[str]):
    #     target = Path(args[0])
    #     if target.exists():
    #         if target.is_absolute():
    #             self.working_directory = target
    #         else:
    #             self.working_directory = os.path.join(self.working_directory, target)
    #         os.chdir(target) # match os path to shell's state
    #     else:
    #         print(f"cd: {args[0]}: No such file or directory")

    # def ls(self, args: list[str]):
    #     print(os.listdir(self.working_directory))

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
            
            try: # get user input
                user_input: list[str] = shlex.split(input()) 
                cmd = user_input[0]
                args = user_input[1:]
            except KeyboardInterrupt: # ctrl + c
                sys.exit(0)
            except ValueError as e: # usually unmatched quotations around args
                print(f"Invalid argument: {e}")
                continue
                
            # ignore empty lines
            if not user_input:
                continue

            # check if a custom builtin command
            if cmd in self.BUILTINS:
                self.BUILTINS[cmd].execute(args, self)

            # check if a path to this program exists
            elif path := shutil.which(cmd):
                self.__run_external(path=path, args=args)

            # program is not a builtin and not on the machine's path
            else:
                print(f"{cmd}: command not found")