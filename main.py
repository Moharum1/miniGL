from fastapi import FastAPI

app = FastAPI()


@app.get("/welcome/{name}")
def Welcome(name : str) -> dict:
    return {
        "message": f"Welcome, {name}!"
    }
