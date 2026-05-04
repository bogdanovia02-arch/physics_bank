from fastapi import FastAPI

app = FastAPI()

@app.post("/register")
def register(user: dict):
    return user