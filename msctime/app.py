from datetime import datetime

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import requests

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get('/', response_class=HTMLResponse)
async def get_msc_time():
    response = requests.get('http://worldtimeapi.org/api/timezone/Europe/Moscow')
    if response.ok:
        date = datetime.strptime(response.json()['datetime'], "%Y-%m-%dT%H:%M:%S.%f%z")
        return templates.TemplateResponse('index.html', {'date': date})
    else:
        return templates.TemplateResponse('error.html', {'code': response.status_code})
