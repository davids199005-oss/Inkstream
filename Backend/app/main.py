from fastapi import FastAPI

app = FastAPI(
    title="Inkstream",
    description="Inkstream is a ChatGPT style chat platform.",
)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Inkstream is a ChatGPT style chat platform Live now."}