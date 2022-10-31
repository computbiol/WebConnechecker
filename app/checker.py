import asyncio
from http.client import HTTPConnection
from urllib.parse import urlparse
import aiohttp
import socket
from contextlib import closing


def check_socket(host, port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((host, port)) == 0:
            print("Port is open")
            return True
        else:
            print("Port is not open")
            return False


# Source: Leodanis Pozo Ramos - Email: leodanis@realpython.com
def site_is_online(url, timeout=2):
    """Return True if the target URL is online.

    Raise an exception otherwise.
    """
    error = Exception("unknown error")
    parser = urlparse(url)
    host = parser.netloc or parser.path.split("/")[0]
    for port in (80, 443):
        connection = HTTPConnection(host=host, port=port, timeout=timeout)
        try:
            connection.request("HEAD", "/")
            return True
        except Exception as e:
            error = e
        finally:
            connection.close()
    raise error


# Source: Modified from Leodanis Pozo Ramos - Email: leodanis@realpython.com
async def site_is_online_async(url, proxy=None, timeout=2):
    """Return True if the target URL is online.

    Raise an exception otherwise.
    """
    error = Exception("unknown error")
    parser = urlparse(url)
    host = parser.netloc or parser.path.split("/")[0]
    for scheme in ("http", "https"):
        target_url = scheme + "://" + host
        async with aiohttp.ClientSession() as session:
            try:
                await session.head(target_url, allow_redirects=True, timeout=timeout, proxy=proxy)
                return True
            except asyncio.TimeoutError:
                error = Exception("timed out")
            except Exception as e:
                error = e
    raise error
