from fastapi import FastAPI
from contextlib import asynccontextmanager
from rich import print, panel


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(panel.Panel("Server Started...", title="Server Status", border_style="green"))
    yield
    print(panel.Panel("...stopped!", title="Server Status", border_style="red"))


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"detail": "Server is running"}
