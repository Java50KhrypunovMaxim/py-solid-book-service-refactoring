from app.book import Book, CommandHandler


def main(book: Book, commands: list[tuple[str, str]]) -> None | str:
    handler = CommandHandler(book)
    result = None
    for cmd, method_type in commands:
        output = handler.execute(cmd, method_type)
        if output:
            result = output
    return result


if __name__ == "__main__":
    sample_book = Book("Sample Book", "This is some sample content.")
    print(main(sample_book, [("display", "reverse"), ("serialize", "xml")]))
