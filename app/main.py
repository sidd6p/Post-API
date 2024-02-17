from fastapi import FastAPI, status
from . import models, database
from .routers import posts, users


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Hello World!"}


app.include_router(posts.router)
app.include_router(users.router)
