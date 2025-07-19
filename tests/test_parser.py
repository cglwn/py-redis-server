def split(data: str):
    """Splits the bytes into parts by \r\n.

    >>> split(b'$4\r\n')
    [b'$4']
    """
    parts = data.split(b"\r\n")
    return parts[:-1]


def parse(data: str):
    parts = split(data)


class Parser:
    def __init__(self, data: str):
        self._data = data
        self._current = 0

    def to_python(self) -> str:
        """Turns an RESP encoded data string to Python primitives."""
        print(f"{self._data[self._current]=}")
        print(f"{(self._data[self._current] == b"$")=}")
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
        print("_parse_data")
        data = ""
        for _ in range(length):
            data += chr(self._data[self._current])
            self._current += 1
        return data

    def _parse_bulk_string(self):
        print("_parse_bulk_string")
        length = self._parse_length()
        bulk_string = self._parse_data(length)
        self._current += 2
        return bulk_string

def t2est_false():
    # An array of two elements [ECHO", "hey"]
    received_data = b"*2\r\n$4\r\nECHO\r\n$3\r\nhey\r\n"
    Parser(received_data).to_python() == ["ECHO", "hey"]

def test_can_parse_sinmple_string():
    received_data = b"+PING"
    assert Parser(b"+PING").to_python() == "PING"

def test_can_parse_echo_cmd():
    received_data = b"$4\r\nECHO\r\n"
    assert Parser(received_data).to_python() == "ECHO"

def test_can_parse_echo_cmd():
    received_data = b"$4\r\nECHO\r\n"
    assert Parser(received_data).to_python() == "ECHO"


def t2est_can_parse_number():
    received_data = b"$3\r\nhey\r\n"
