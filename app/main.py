import sys

def main():
    while True:
        sys.stdout.write("$ ")

        command = input()
        if command == "exit":
            break
        elif command[:4] == "type":
            if command[5:] in ["echo", "type", "exit"]:
                print(f"{command[5:]} is a shell builtin")
            else:
                print(f"{command[5:]}: not found")
        elif command[:4] == "echo":
            print(command[5:])
        else:
            print(f"{command}: command not found")

if __name__ == "__main__":
    main()
