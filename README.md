```shell
docker build -t webconnechecker:0.0.1 .
docker run -itd --rm --name webconnechecker -p 8000:8000 webconnechecker:0.0.1
# use proxy
docker run -it --rm --name webconnechecker --network host --env HTTP_PROXY="http://127.0.0.1:9999" webconnechecker:0.0.1
```


Reference:

[HEAD requests with aiohttp is dog slow](https://stackoverflow.com/questions/55250990/head-requests-with-aiohttp-is-dog-slow)
