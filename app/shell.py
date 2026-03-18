import sys
import shlex
import shutil
import subprocess
from pathlib import Path, PurePath
from contextlib import redirect_stdout

import app.builtins 
from app.registry import BUILTIN_COMMANDS

class Shell:
    
    def __init__(self) -> None:
        self.working_directory: Path = Path.cwd()
        self.BUILTINS = BUILTIN_COMMANDS

    def __parse_input(self, user_input: list[str]) -> tuple[str, list[str], str | None, str | None]:
        cmd: str = user_input[0]
        args: list[str] = []
        redirect_file = None
        redirect_mode = None

        i = 1
        while i < len(user_input):
            token = user_input[i]
            if token in (">", "1>"):
                redirect_mode = "w"
                redirect_file = user_input[i + 1]
                break
            elif token == ">>":
                pass
            else:
                args.append(token)
            i += 1
        
        return cmd, args, redirect_file, redirect_mode

    def __run_external(self, path: str, args: list[str], stdout_file=None) -> None:
        try:
            cmd = PurePath(path).name
            subprocess.run([cmd, *args], stdout=stdout_file)
        except Exception as e:
            sys.stderr.write(f"Error executing {path}: {e}\n")

    def __run_command(self, cmd: str, args: list[str], stdout_file=None) -> None:
        # check if a custom builtin command
        if cmd in self.BUILTINS:
            if stdout_file:
                with redirect_stdout(stdout_file):
                    self.BUILTINS[cmd].execute(args, self)
            else:
                self.BUILTINS[cmd].execute(args, self)

        # check if a path to this program exists
        elif path := shutil.which(cmd):
            self.__run_external(path=path, args=args, stdout_file=stdout_file)

        # program is not a builtin and not on the machine's path
        else:
            sys.stderr.write(f"{cmd}: command not found\n")
        
    def run(self):
        """Main shell REPL loop."""
        while True:
            sys.stdout.write("$ ")
            sys.stdout.flush()
            
            try: # get user input
                user_input: list[str] = shlex.split(input()) 
                if not user_input:
                    continue

                cmd, args, redirect_file, redirect_mode = self.__parse_input(user_input=user_input)
            except KeyboardInterrupt: # ctrl + c
                sys.stdout.write("\n")
                sys.exit(0)
            except ValueError as e: # usually unmatched quotations around args
                sys.stderr.write(f"Invalid argument: {e}\n")
                continue
                
            if redirect_file:
                with open(redirect_file, redirect_mode) as f:
                    self.__run_command(cmd=cmd, args=args, stdout_file=f)
            else:
                self.__run_command(cmd=cmd, args=args)

            # restore stdout to terminal
            sys.stdout = sys.__stdout__