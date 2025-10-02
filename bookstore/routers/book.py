from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from config.db import collection
from models.book import Book, UpdateBook
from utils.helpers import serialize_book

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", status_code=status.HTTP_200_OK)
def list_books():
    books = [serialize_book(b) for b in collection.find()]
    message = "No books found" if not books else "Books retrieved"
    return {"success": True, "message": message, "data": books}

@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_book(id: str):
    try:
        book = collection.find_one({"_id": ObjectId(id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid book ID format")
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"success": True, "message": "Book retrieved", "data": serialize_book(book)}

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_book(book: Book):
    try:
        result = collection.insert_one(jsonable_encoder(book))
        created_book = collection.find_one({"_id": result.inserted_id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"success": True, "message": "Book created", "data": serialize_book(created_book)}

@router.patch("/{id}", status_code=status.HTTP_200_OK)
def update_book(id: str, update: UpdateBook):
    try:
        book = collection.find_one({"_id": ObjectId(id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid book ID format")
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    update_data = {k: v for k, v in update.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    result = collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.modified_count == 0:
        return {"success": True, "message": "No changes made", "data": serialize_book(book)}

    updated_book = collection.find_one({"_id": ObjectId(id)})
    return {"success": True, "message": "Book updated", "data": serialize_book(updated_book)}

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_book(id: str):
    try:
        result = collection.delete_one({"_id": ObjectId(id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid book ID format")
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"success": True, "message": "Book deleted", "data": None}
