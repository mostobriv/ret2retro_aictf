#!/usr/bin/env python
import logging
import argparse
import asyncio
import uvloop
import jinja2
import aiohttp_jinja2

from aiohttp import web

from ret2retro.config import TEMPLATES_PATH, STATIC_PATH, IS_PRODUCTION
from ret2retro.handlers import index, transform_image, redirect_to_main, glitched_image
from ret2retro.middlewares import setup_error_middlewares


CONSOLE_LOG_FORMAT = '%(asctime)-10s : %(levelname)-8s : %(message)s'
CLIENT_MAX_SIZE = (1024 ** 2) * 10


def main():
    parser = argparse.ArgumentParser(description='Ret2Retro web')
    parser.add_argument('--host', dest='host', type=str, default='0.0.0.0')
    parser.add_argument('-p', '--port', dest='port', type=int, default=80)
    args = parser.parse_args()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    app = web.Application(client_max_size=CLIENT_MAX_SIZE)
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(TEMPLATES_PATH))
    app.add_routes([
        web.post('/', transform_image),
        web.get('/result', glitched_image),
        web.get('/', index),
    ])
    if not IS_PRODUCTION:
        app.router.add_static('/static/', STATIC_PATH)
    else:
        app.router.add_route('GET', '/{path:.*}', redirect_to_main)

    setup_logger()
    setup_error_middlewares(app)

    web.run_app(app, host=args.host, port=args.port)


def setup_logger():
    formatter = logging.Formatter(CONSOLE_LOG_FORMAT)

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    for logger_name in ['aiohttp']:
        logger = logging.getLogger(logger_name)
        logger.addHandler(console)
        logger.setLevel(logging.INFO)

if __name__ == '__main__':
    main()
