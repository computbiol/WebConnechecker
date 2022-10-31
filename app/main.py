from typing import Union
from fastapi import FastAPI
import urllib.parse
from .checker import check_socket, site_is_online_async


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/check_url/{url}")  # url parameter should be quoted: urllib.parse.quote('http://www.google.com', safe='')
async def check_url(url: str):
    url = urllib.parse.unquote(url).strip()
    print(url)
    port_status = check_socket(host='127.0.0.1', port=9999)
    if port_status:
        proxy = 'http://127.0.0.1:9999'
    else:
        proxy = None
    print(proxy)
    try:
        result = await site_is_online_async(url, proxy)
    except Exception:
        result = False
    return {url: result}
