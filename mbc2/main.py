from aiohttp import web

from mbc2 import routes


def create_app() -> web.Application:
    app = web.Application()
    routes.setup_routes(app)
    return app


def main() -> None:
    app = create_app()
    web.run_app(app)


if __name__ == '__main__':
    main()
