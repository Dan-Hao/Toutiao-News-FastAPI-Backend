from fastapi import FastAPI
from routers import news, users, favorite_news, history
from fastapi.middleware.cors import CORSMiddleware

from utils.exception_handler import register_exception_handler

app = FastAPI()
#注册异常处理
register_exception_handler(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",  # 也可能用到
        "http://127.0.0.1:3000",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite_news.router)
app.include_router(history.router)
@app.get("/")
async def root():
    return {"message": "Hello World"}
