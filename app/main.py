import asyncio


async def handle_ping(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> None:
    while True:
        _ = await reader.read(1024)
        writer.write(b"+PONG\r\n")
        await writer.drain()


async def run_server() -> None:
    server = await asyncio.start_server(handle_ping, "localhost", 6379)
    async with server:
        await server.serve_forever()


def main():
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print()


if __name__ == "__main__":
    main()
