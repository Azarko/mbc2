import logging
import os.path

from aiohttp import web
import aiohttp_jinja2
import jinja2

from mbc2 import middlewares
from mbc2 import routes

BASE_PATH = os.path.dirname(__file__)
TEMPLATES_DIR = os.path.join(BASE_PATH, 'templates')
TEMPLATES_LOADER = jinja2.FileSystemLoader(TEMPLATES_DIR)


async def create_app() -> web.Application:
    logging.basicConfig(level=logging.INFO)
    app = web.Application(middlewares=[middlewares.catch_validation_error])
    aiohttp_jinja2.setup(app, enable_async=True, loader=TEMPLATES_LOADER)
    routes.setup_routes(app)
    return app


def main() -> None:
    app = create_app()
    web.run_app(app)


if __name__ == '__main__':
    main()
