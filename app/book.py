import json
import xml.etree.ElementTree as ET
from typing import Protocol


class DisplayStrategy(Protocol):
    def display(self, content: str) -> None:
        ...


class ConsoleDisplay(DisplayStrategy):
    def display(self, content: str) -> None:
        print(content)


class ReverseDisplay(DisplayStrategy):
    def display(self, content: str) -> None:
        print(content[::-1])


class PrintStrategy(Protocol):
    def print(self, title: str, content: str) -> None:
        ...


class ConsolePrint(PrintStrategy):
    def print(self, title: str, content: str) -> None:
        print(f"Printing the book: {title}...")
        print(content)


class ReversePrint(PrintStrategy):
    def print(self, title: str, content: str) -> None:
        print(f"Printing the book in reverse: {title}...")
        print(content[::-1])


class SerializeStrategy(Protocol):
    def serialize(self, title: str, content: str) -> str:
        ...


class JSONSerialize(SerializeStrategy):
    def serialize(self, title: str, content: str) -> str:
        return json.dumps({"title": title, "content": content})


class XMLSerialize(SerializeStrategy):
    def serialize(self, title: str, content: str) -> str:
        root = ET.Element("book")
        title_elem = ET.SubElement(root, "title")
        title_elem.text = title
        content_elem = ET.SubElement(root, "content")
        content_elem.text = content
        return ET.tostring(root, encoding="unicode")


class Book:
    def __init__(self, title: str, content: str) -> None:
        self.title = title
        self.content = content

    def display(self, strategy: DisplayStrategy) -> None:
        strategy.display(self.content)

    def print_book(self, strategy: PrintStrategy) -> None:
        strategy.print(self.title, self.content)

    def serialize(self, strategy: SerializeStrategy) -> str:
        return strategy.serialize(self.title, self.content)


class CommandHandler:
    def __init__(self, book: Book) -> None:
        self.book = book
        self.display_strategies = {
            "console": ConsoleDisplay(),
            "reverse": ReverseDisplay(),
        }
        self.print_strategies = {
            "console": ConsolePrint(),
            "reverse": ReversePrint(),
        }
        self.serialize_strategies = {
            "json": JSONSerialize(),
            "xml": XMLSerialize(),
        }

    def execute(self, command: str, method_type: str) -> str | None:
        if command == "display" and method_type in self.display_strategies:
            self.book.display(self.display_strategies[method_type])
        elif command == "print" and method_type in self.print_strategies:
            self.book.print_book(self.print_strategies[method_type])
        elif (command == "serialize" and method_type
              in self.serialize_strategies):
            return self.book.serialize(self.serialize_strategies[method_type])
        else:
            raise ValueError(
                f"Unknown command or method type: {command}, {method_type}"
            )
