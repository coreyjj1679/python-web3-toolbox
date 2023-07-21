import requests as rq
import logging
import time
import json

extra = {"status_code": "", "dest": "", "method": ""}
MAX_ATTEMPT = 10

logging.basicConfig(
    filename="requests.log",
    level=logging.INFO,
    filemode="a",
    format="[%(method)s][%(dest)s][%(status_code)s] %(asctime)s -  %(message)s",
)


# Turn off logging
# logging.disable()


def get(endpoint, headers=None, dest=None):
    attempt = 0
    while attempt < MAX_ATTEMPT:
        attempt += 1
        try:
            res = rq.get(endpoint, headers=headers)
            logging.info(
                f"{endpoint}, attemp: {attempt}",
                extra={"status_code": res.status_code, "dest": dest, "method": "GET"},
            )
            if res.status_code == 200:
                return res.json()
            elif res.status_code == 429:
                print(
                    f'Too Many Requests, Retry after: {int(res.headers["Retry-After"])} s'
                )
                time.sleep(int(res.headers["Retry-After"]))
            else:
                time.sleep(2)
        except Exception as e:
            logging.exception(e, extra={"status_code": "Exception", "dest": dest})


def post(endpoint, query, variables, dest=None):
    attempt = 0
    while attempt < MAX_ATTEMPT:
        attempt += 1
        try:
            res = rq.post(endpoint, json={"query": query, "variables": variables})
            logging.info(
                f"{endpoint}, attemp: {attempt}",
                extra={"status_code": res.status_code, "dest": dest, "method": "POST"},
            )
            if res.status_code == 200:
                return json.loads(res.text)
            elif res.status_code == 429:
                time.sleep(int(res.headers["Retry-After"]))
            else:
                time.sleep(2)
        except Exception as e:
            logging.exception(e, extra={"status_code": "Exception", "dest": dest})
