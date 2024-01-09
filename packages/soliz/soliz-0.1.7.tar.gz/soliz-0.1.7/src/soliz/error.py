from .tokens import Span


class ErrorContext:
    def __init__(self, expected: list[str], found: str) -> None:
        """
        Instantiates an ErrorContext.

        :param expected: the expected characters, rules, or events
        :param found: the present character or event
        """
        if expected is None or found is None:
            raise ValueError("Arguments cannot be None")

        self.expected = expected
        self.found = found

    def __str__(self) -> str:
        expected = map(lambda x: "'" + x + "'", self.expected)
        return "Expected: " + ' | '.join(expected) + f", found '{self.found}'"


class Error(Exception):
    def __init__(self, message: str, span: Span, ctx: ErrorContext | None = None) -> None:
        if message is None or span is None:
            raise ValueError("Arguments cannot be None")

        self.message = message
        self.span = span
        self.ctx = ctx

    def pretty_print(self, text: str) -> None:
        """
        Prints the error with human-readable debugging information.

        :param text: the text content of the source file
        """
        print("Error: " + self.message)

        lines = text.splitlines()

        if self.span.ln <= len(lines):
            # ln should always be one or more
            print(lines[self.span.ln - 1])

        if self.span.cs > 1:
            print(' ' * (self.span.cs - 1), end='')

        print('^' * max(1, self.span.ce - self.span.cs))

        if self.ctx:
            print(self.ctx)

        print(f"Occurs at: {self.span}")


class BuiltinErrors:
    """
    Builtin error messages.
    """
    UNEXPECTED_CHARACTER = "Unexpected character"
    UNTERMINATED_STRING = "Basic strings cannot contain newline characters"
    UNEXPECTED_EOI = "Unexpected end of input"
    UNSUPPORTED_ESCAPE = "Unsupported escape sequence"
