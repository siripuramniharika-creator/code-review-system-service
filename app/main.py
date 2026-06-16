from fastapi import FastAPI
from app.routes.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from app.routes.review import router as review_router
from app.models.user import User
from app.models.review import Review
from app.database.base import Base
from app.database.db import engine

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
@app.get("/")
def test():
    return {"message": "Backend working"}

app.include_router(
    review_router,
    prefix="/api",
    tags=["AI Code Review"]
)
for route in app.routes:
    print(route.path)
