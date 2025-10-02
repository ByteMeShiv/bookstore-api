def serialize_book(book: dict) -> dict:
    book["id"] = str(book["_id"])
    del book["_id"]
    return book
