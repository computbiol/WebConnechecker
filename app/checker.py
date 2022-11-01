import asyncio
import aiohttp
import logging
from typing import Tuple
from socket import gaierror
from aiohttp.client_exceptions import TooManyRedirects
import socket
from contextlib import closing


HEADERS = {
    'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/45.0.2454.101 Safari/537.36'),
}


class HttpClient:
    session: aiohttp.ClientSession = None

    def start(self):
        self.session = aiohttp.ClientSession()

    async def stop(self):
        await self.session.close()
        self.session = None

    def __call__(self) -> aiohttp.ClientSession:
        assert self.session is not None
        return self.session


def check_socket(host, port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((host, port)) == 0:
            print("Port is open")
            return True
        else:
            print("Port is not open")
            return False


def add_scheme(url: str):
    urls = []
    if url.startswith("https://"):
        https_url = url
        http_url = url.replace('https://', 'http://')
        urls.append(https_url)
        urls.append(http_url)
    elif url.startswith("http://"):
        https_url = url.replace('http://', 'https://')
        http_url = url
        urls.append(https_url)
        urls.append(http_url)
    else:
        https_url = f"https://{url}"
        http_url = f"http://{url}"
        urls.append(https_url)
        urls.append(http_url)
    return urls


async def get_status_code(session: aiohttp.ClientSession, url: str, proxy: str) -> Tuple[int, str]:
    try:
        # A HEAD request is quicker than a GET request
        resp = await session.head(url, allow_redirects=True, proxy=proxy, ssl=False, headers=HEADERS)
        async with resp:
            status = resp.status
            reason = resp.reason
            real_url = resp.real_url
        if status == 405:
            # HEAD request not allowed, fall back on GET
            resp = await session.get(url=url, allow_redirects=True, proxy=proxy, ssl=False, headers=HEADERS)
            async with resp:
                status = resp.status
                reason = resp.reason
                real_url = resp.real_url
        return (status, reason, real_url)
    except aiohttp.InvalidURL as e:
        return (900, str(e), url)
    except aiohttp.ClientConnectorError:
        return (901, "Unreachable", url)
    except gaierror as e:
        return (902, str(e), url)
    except aiohttp.ServerDisconnectedError as e:
        return (903, str(e), url)
    except aiohttp.ClientOSError as e:
        return (904, str(e), url)
    except TooManyRedirects as e:
        return (905, str(e), url)
    except aiohttp.ClientResponseError as e:
        return (906, str(e), url)
    except aiohttp.ServerTimeoutError:
        return (907, "Connection timeout", url)
    except asyncio.TimeoutError:
        return (908, "Connection timeout", url)
