from fastapi import FastAPI
import httpx
import time
import logging as log
from deta import App, Deta
from furl import furl

app = App(FastAPI())

log.basicConfig(level=log.INFO)

deta = Deta()
db = deta.Base("echoes")
database_items = db.fetch()

cleanup_tolerance = 240

def sub_params(echo):
    parsed = echo.replace("*", "&")
    return parsed


async def request_data(tolerance, echo):
    start_time = time.time()
    parse_url = furl(echo)
    params = parse_url.args
    url = echo.split('?')[0]
    echo_cache = db.get(echo)

    try:
        time_buffer = echo_cache["timestamp"] + tolerance
        time_check = start_time - time_buffer
    except:
        log.warning(f"Echo - {echo} - No Timestamp Found")
        time_check = 1

    if db is None or time_check > 0:
        request = httpx.get(url, params=params)
        response_data = request.json()

        db.put({'key': echo, 'timestamp': start_time, 'value': response_data})
        log.info(f"Fetched - {time.time() - start_time}")
        return request.json()

    else:
        log.info(f"Cached - {time.time() - start_time} - {echo}")
        return echo_cache['value']


def cleanup():
    database_items = db.fetch()
    for items in database_items:
        for item in items:
            try:
                print(item['timestamp'])
                current_timestamp = time.time()
                time_buffer = item['timestamp'] + cleanup_tolerance
                time_check = current_timestamp - time_buffer
                if time_check > 0:
                    db.delete(item['key'])
            except:
                db.delete(item['key'])


@app.get("/")
async def root(tolerance: int, echo: str):
    prepped_echo = sub_params(echo)
    data = await request_data(tolerance, prepped_echo)
    return data


@app.get("/clear")
async def clear():
    cleanup()
    return "Cache Cleared!"


@app.lib.cron()
def cron_job(event):
    cleanup()