from fastapi import FastAPI
from routes import user_routes, chat_routes, message_routes
from db.indexes import create_indexes

app = FastAPI()

@app.on_event("startup")
async def startup():
    await create_indexes()


@app.get("/")
async def root():
    return {"message": "Welcome to the Chat Mongo!"}
app.include_router(user_routes.router)
app.include_router(chat_routes.router)
app.include_router(message_routes.router)