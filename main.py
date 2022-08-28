from command import listen_command, do_command


def main() -> None:
    while True:
        command = listen_command()
        do_command(command)


if __name__ == "__main__":
    main()