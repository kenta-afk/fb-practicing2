import uvicorn
from fastapi import FastAPI
from routers import router

app = FastAPI()


@app.get("/")
def health():
    return "working!"

app.include_router(router.router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", reload=True)