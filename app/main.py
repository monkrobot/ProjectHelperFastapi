from fastapi import FastAPI

import uvicorn

from tasks.router import router as tasks_router
from shopping.router import router as shopping_router


app = FastAPI()

app.include_router(tasks_router)
app.include_router(shopping_router)


@app.router.get("/")
def initial_page():
    return {"msg": "initial page"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
