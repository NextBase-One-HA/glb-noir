import asyncio
from fastapi import FastAPI, Request
from .router_core import handle_translate

app = FastAPI()


@app.get("/health")
def health():
    return {"ok": True, "service": "ai-router"}


@app.post("/translate")
async def translate(req: Request):
    data = await req.json()
    # Offload synchronous routing/HTTP work to a thread so the event loop is not blocked.
    return await asyncio.to_thread(handle_translate, data)


@app.post("/gateway")
async def gateway(req: Request):
    data = await req.json()
    return await asyncio.to_thread(handle_translate, data)
