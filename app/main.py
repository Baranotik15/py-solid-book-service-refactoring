import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod


class DisplayType(ABC):

    @abstractmethod
    def display(self) -> None:
        pass


class ConsoleDisplayType(DisplayType):
    def __init__(self, content):
        self.content = content

    def display(self) -> None:
        print(self.content)


class ReverseDisplayType(DisplayType):
    def __init__(self, content):
        self.content = content[::-1]

    def display(self) -> None:
        print(self.content)


class PrintType(ABC):

    @abstractmethod
    def print_book(self, title: str, content: str) -> None:
        pass


class PrintConsoleType(PrintType):
    def print_book(self, title: str, content: str) -> None:
        print(f"Printing the book: {title}...")
        print(content)


class PrintDisplayType(PrintType):
    def print_book(self, title: str, content: str) -> None:
        print(f"Printing the book in reverse: {title}...")
        print(content[::-1])



class Book:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    @staticmethod
    def display(display_type: DisplayType) -> None:
        display_type.display()

    def print_book(self, print_type: PrintType) -> None:
        print_type.print_book(self.title, self.content)

    def serialize(self, serialize_type: str) -> str:
        if serialize_type == "json":
            return json.dumps({"title": self.title, "content": self.content})
        elif serialize_type == "xml":
            root = ET.Element("book")
            title = ET.SubElement(root, "title")
            title.text = self.title
            content = ET.SubElement(root, "content")
            content.text = self.content
            return ET.tostring(root, encoding="unicode")
        else:
            raise ValueError(f"Unknown serialize type: {serialize_type}")


def main(book: Book, commands: list[tuple[str, str]]) -> None | str:
    for cmd, method_type in commands:

        if cmd == "display":
            if method_type == "console":
                book.display(ConsoleDisplayType(book.content))
            elif method_type == "reverse":
                book.display(ReverseDisplayType(book.content))
            else:
                raise ValueError(f"Unknown display type: {method_type}")

        elif cmd == "print":
            if method_type == "console":
                book.print_book(PrintConsoleType())
            elif method_type == "reverse":
                book.print_book(PrintDisplayType())
            else:
                raise ValueError(f"Unknown print type: {method_type}")


        elif cmd == "serialize":
            return book.serialize(method_type)


if __name__ == "__main__":
    sample_book = Book("Sample Book", "This is some sample content.")
    print(main(sample_book, [("display", "reverse"), ("serialize", "xml")]))
