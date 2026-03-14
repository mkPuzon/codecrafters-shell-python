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
        print(" ".join(args))

@register_command("type")
class TypeCommand(Command):
    
    def execute(self, args: list[str], shell_state: Shell) -> None:
        cmd = args[0]
        if cmd in shell_state.BUILTINS:
            print(f"{cmd} is a shell builtin")
        elif path := shutil.which(cmd):
            print(f"{cmd} is {path}")
        else:
            print(f"{cmd}: not found")

@register_command("pwd")
class PWDCommand(Command):
    
    def execute(self, args: list[str], shell_state: Shell) -> None:
        print(shell_state.working_directory)

@register_command("ls")
class LSCommand(Command):

    def execute(self, args: list[str], shell_state: Shell) -> None:
        print(os.listdir(shell_state.working_directory))

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
            print(f"cd: {args[0]}: No such file or directory")
