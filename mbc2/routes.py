import os.path

from mbc2.handlers.ajax import calculate
from mbc2.handlers.web import index
from mbc2.handlers.web import party_calc


CURRENT_FOLDER = os.path.dirname(__file__)


def setup_routes(app):
    app.router.add_get('/', index.handler, name='index')
    app.router.add_get('/party-calc', party_calc.handler, name='party_calc')

    app.router.add_post(
        '/party-calc/calculate',
        calculate.handler,
        name='party_calc_calculate',
    )
    # probably, it shouldn't be called on production
    setup_static_routes(app)


def setup_static_routes(app):
    app.router.add_static(
        '/static/',
        path=os.path.join(CURRENT_FOLDER, 'static'),
        name='static',
    )
