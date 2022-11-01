from fastapi import FastAPI
from .checker import check_socket, add_scheme, get_status_code, HttpClient


app = FastAPI()
http_client = HttpClient()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.on_event("startup")
async def startup():
    http_client.start()


@app.get("/check_url/")
async def check_url(url: str):
    urls = add_scheme(url=url)
    port_status = check_socket(host='127.0.0.1', port=9999)
    if port_status:
        proxy = 'http://127.0.0.1:9999'
    else:
        proxy = None
    results = {}
    for i in urls:
        result = await get_status_code(session=http_client.session, url=i, proxy=proxy)
        results[i] = result
    print(results)
    # set http_scheme url as default derived_url
    derived_url = urls[1]
    url_status = 'unavailable'
    for v in results.values():
        if v[0] == 200:
            derived_url = str(v[2])
            url_status = 'available'
    return {
        'original_url': url,
        'derived_url': derived_url,
        'url_status': url_status
    }
