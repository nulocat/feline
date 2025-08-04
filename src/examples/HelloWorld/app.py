from feline import Feline
from feline.http.request import Request

app = Feline()


@app.get("/")
def hello_world(request: Request):
    return f"Hello World, from {request.host}"


app.run(__name__, debug=True)
