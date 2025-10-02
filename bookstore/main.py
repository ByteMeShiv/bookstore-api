from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import book

app = FastAPI(title="BookStore API")


origins = ["https://bookstore-frontend-rust-ten.vercel.app/"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(book.router)
