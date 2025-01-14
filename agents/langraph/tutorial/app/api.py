from app.agents import graph
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return graph.invoke({"customer_name": "John", "my_var":"indio"})