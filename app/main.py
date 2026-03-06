import sys
import shutil
        
def main():
    builtin_commands = ["echo", "type", "exit"]
    while True:
        sys.stdout.write("$ ")
        command = input()

        if command == "exit":
            break

        elif command.startswith("echo "):
            print(command[5:])

        elif command.startswith("type "):
            cmd_arg = command[5:]
            if cmd_arg in builtin_commands:
                print(f"{command[5:]} is a shell builtin")
            elif path := shutil.which(cmd_arg):
                print(f"{cmd_arg} is {path}")
            else:
                print(f"{command[5:]}: not found")


        else:
            print(f"{command}: command not found")

if __name__ == "__main__":
    main()
