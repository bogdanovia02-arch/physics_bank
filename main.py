from fastapi import FastAPI

app = FastAPI(title="Physics Task Bank")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Physics Task Bank API!"}