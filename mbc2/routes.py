from mbc2.handlers.ajax import calculate
from mbc2.handlers.web import index
from mbc2.handlers.web import party_calc


def setup_routes(app):
    app.router.add_get('/', index.handler, name='index')
    app.router.add_get('/party-calc', party_calc.handler, name='party_calc')

    app.router.add_post(
        '/party-calc/calculate',
        calculate.handler,
        name='party_calc_calculate',
    )
