from mbc2.handlers import index


def setup_routes(app):
    app.router.add_get('/', index.handler, name='index')
