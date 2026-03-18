import os
import sys
import shutil
from pathlib import Path
from app.registry import register_command, Command

@register_command("exit")
class ExitCommand(Command):

    def execute(self, args: list[str], shell_state: Shell) -> None:
        sys.exit(0)
    
@register_command("echo")
class EchoCommand(Command):
    
    def execute(self, args: list[str], shell_state: Shell) -> None:
        sys.stdout.write(" ".join(args) + "\n")

@register_command("type")
class TypeCommand(Command):
    
    def execute(self, args: list[str], shell_state: Shell) -> None:
        cmd = args[0]
        if cmd in shell_state.BUILTINS:
            sys.stdout.write(f"{cmd} is a shell builtin\n")
        elif path := shutil.which(cmd):
            sys.stdout.write(f"{cmd} is {path}\n")
        else:
            sys.stdout.write(f"{cmd}: not found\n")

@register_command("pwd")
class PWDCommand(Command):
    
    def execute(self, args: list[str], shell_state: Shell) -> None:
        sys.stdout.write(str(shell_state.working_directory) + "\n")

@register_command("ls")
class LSCommand(Command):

    def execute(self, args: list[str], shell_state: Shell) -> None:
        if "-1" in args:
            for f in os.listdir(shell_state.working_directory):
                sys.stdout.write(str(f) + "\n")
        else:
            sys.stdout.write(str(os.listdir(shell_state.working_directory)) + "\n")

@register_command("cd")
class CDCommand(Command):

    def execute(self, args: list[str], shell_state: Shell) -> None:
        target = Path(args[0]).expanduser().resolve()
        if target.exists():
            shell_state.working_directory = target
            os.chdir(target)
        elif args[0] == "~":
            target = os.getenv('HOME')
            shell_state.working_directory = target
            os.chdir(target)
        else:
            sys.stdout.write(f"cd: {args[0]}: No such file or directory\n")
