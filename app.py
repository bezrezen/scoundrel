from fastapi import FastAPI


app = FastAPI(debug=True)


@app.get("/")
def index():
    return {"message":"Hello world"}

https://127.0.0.1:8000/

@app.get("/scoundrel")
def default():
    pass