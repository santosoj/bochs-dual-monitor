import os
import select
import sys

from cp437 import cp437_to_utf8


ANSI_CURSOR_HOME = "\33[0;0H"
ANSI_ATTR_RESET = "\33[0m"


def main() -> int:
    mda_pipe = os.getenv("MDA_PIPE")
    if not mda_pipe:
        print("Environment variable MDA_PIPE must contain path to named pipe. Aborting.")
        return 1

    fifo = os.open(mda_pipe, os.O_RDONLY | os.O_NONBLOCK)
    poll = select.poll()
    poll.register(fifo, select.POLLIN)
    while True:
        try:
            if (fifo, select.POLLIN) in poll.poll(1000 // 12):
                data = os.read(fifo, 49_152)
                print(ANSI_CURSOR_HOME + cp437_to_utf8(data), end="")
        except KeyboardInterrupt:
            print(ANSI_ATTR_RESET)
            return 0


if __name__ == "__main__":
    sys.exit(main())
