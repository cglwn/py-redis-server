import asyncio

class Parser:
    def __init__(self, data: str):
        self._data = data
        self._current = 0

    def to_python(self) -> str:
        """Turns an RESP encoded data string to Python primitives."""
        if self._data[self._current] == ord("$"):
            self._current += 1
            return self._parse_bulk_string()
        elif self._data[self._current] == ord("*"):
            self._current += 1
            return self._parse_array()

    def _parse_length(self) -> int:
        """Parses the length of byte-encoded integers."""
        length = 0
        while self._data[self._current] != ord("\r"):
            length = (length * 10) + (self._data[self._current] - ord("0"))
            self._current += 1
        self._current += 2 # Consume the \r\n
        return length

    def _parse_array(self):
        arr = []
        for _ in range(self._parse_length()):
            arr.append(self.to_python())
        return arr

    def _parse_data(self, length) -> str:
        data = ""
        for _ in range(length):
            data += chr(self._data[self._current])
            self._current += 1
        return data

    def _parse_bulk_string(self):
        length = self._parse_length()
        bulk_string = self._parse_data(length)
        self._current += 2
        return bulk_string

async def handle_ping(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> None:
    while data is not None:
        data = await reader.read(1024)
        print(f"{data=}")
        cmd, *args = Parser(data).to_python()
        print(f"{cmd=}")
        if cmd == "PING":
            writer.write(b"+PONG\r\n")
        elif cmd == "ECHO":
            writer.write(b"+" + bytes(args[0], "utf-8") + b"\r\n")
        await writer.drain()
    writer.close()
    await writer.wait_closed()


async def run_server() -> None:
    server = await asyncio.start_server(handle_ping, "localhost", 6379)
    async with server:
        await server.serve_forever()


def main():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run_server())


if __name__ == "__main__":
    main()
