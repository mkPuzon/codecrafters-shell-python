import os
import sys
import shlex
import shutil
import subprocess
from pathlib import Path, PurePath
from contextlib import redirect_stdout, redirect_stderr, ExitStack

import app.builtins 
from app.registry import BUILTIN_COMMANDS

class Shell:
    
    def __init__(self) -> None:
        self.working_directory: Path = Path.cwd()
        self.BUILTINS = BUILTIN_COMMANDS

    def __parse_input(self, user_input: list[str]) -> tuple[str, list[str], str | None, str | None]:
        cmd: str = user_input[0]
        args: list[str] = []
        stdout_file = None
        stderr_file = None
        redirect_mode = None 

        i = 1
        while i < len(user_input):
            token = user_input[i]
            if token in (">", "1>"):
                stdout_file = user_input[i + 1]
                redirect_mode = "w"
                break
            elif token == "2>":
                stderr_file = user_input[i + 1]
                redirect_mode = "w"
                break
            elif token == ">>":
                pass
            else:
                args.append(token)
            i += 1

        # ensure the stdout & stderr files exist
        if stdout_file: 
            Path(stdout_file).parent.mkdir(parents=True, exist_ok=True)
        if stderr_file: 
            Path(stderr_file).parent.mkdir(parents=True, exist_ok=True)
        
        return cmd, args, stdout_file, stderr_file, redirect_mode 

    def __run_external(self, path: str, args: list[str], stdout_file=None, stderr_file=None) -> None:
        try:
            cmd = PurePath(path).name
            subprocess.run([cmd, *args], stdout=stdout_file, stderr=stderr_file)
        except Exception as e:
            err_msg = f"Error executing {path}: {e}\n"
            if stderr_file:
                stderr_file.write(err_msg)
            else:
                sys.stderr.write(err_msg)

    def __run_command(self, cmd: str, args: list[str], stdout_file=None, stderr_file=None) -> None:
        # check if a custom builtin command
        if cmd in self.BUILTINS:

            with ExitStack() as stack:
                if stdout_file:
                    stack.enter_context(redirect_stdout(stdout_file))
                if stderr_file:
                    stack.enter_context(redirect_stderr(stderr_file))

                self.BUILTINS[cmd].execute(args, self)

        # check if a path to this program exists
        elif path := shutil.which(cmd):
            self.__run_external(path=path, args=args, stdout_file=stdout_file, stderr_file=stderr_file)

        # program is not a builtin and not on the machine's path
        else:
            err_msg = f"{cmd}: command not found\n"
            if stderr_file:
                stderr_file.write(err_msg)
            else:
                sys.stderr.write(err_msg)
        
    def run(self):
        """Main shell REPL loop."""
        while True:
            sys.stdout.write("$ ")
            sys.stdout.flush()
            
            try: # get user input
                user_input: list[str] = shlex.split(input()) 
                if not user_input:
                    continue

                cmd, args, stdout_path, stderr_path, redirect_mode = self.__parse_input(user_input=user_input)
            except KeyboardInterrupt: # ctrl + c
                sys.stdout.write("\n")
                sys.exit(0)
            except ValueError as e: # usually unmatched quotations around args
                sys.stderr.write(f"Invalid argument: {e}\n")
                continue
                
            with ExitStack() as stack:
                stdout_f = stack.enter_context(open(stdout_path, redirect_mode)) if stdout_path else None
                stderr_f = stack.enter_context(open(stderr_path, redirect_mode)) if stderr_path else None

                self.__run_command(cmd=cmd, args=args, stdout_file=stdout_f, stderr_file=stderr_f)