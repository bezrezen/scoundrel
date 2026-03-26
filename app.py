from fastapi import FastAPI


app = FastAPI(debug=True)


@app.get("/")
def index():
    return {"message":"Hello world"}

@app.get("/scoundrel")
def default():
    pass