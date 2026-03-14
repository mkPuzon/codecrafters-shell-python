BUILTIN_COMMANDS = {}

def register_command(name: str):
    """A decorator that registers a command class in BUILTIN_COMMANDS"""
    def decorator(cls):
        BUILTIN_COMMANDS[name] = cls()
        return cls
    return decorator

class Command:
    """Base interface for all builtin commands."""
    def execute(self, args: list[str], shell_state) -> None:
        raise NotImplementedError 