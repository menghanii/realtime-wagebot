from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from calc import calculate

class Item(BaseModel):
    wage: str
    the_day: str
    the_time: str
    start: str
    end: str

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory=".")


@app.get("/", response_class=HTMLResponse)
async def get_item(request:Request):
    return templates.TemplateResponse("pre.html", {"request": request})


@app.get("/mywage", response_class=HTMLResponse)
async def main(request: Request, wage, the_day, start, end):
    mywage = calculate(int(wage), int(the_day), int(start), int(end))
    return templates.TemplateResponse("index.html", {"request":request,
                                                     "mywage": mywage})