async def test_calculate(web_app_client):
    # TODO: move to separate folder (ajax)
    response = await web_app_client.post(
        '/party-calc/calculate',
        json={
            'test': 'pest',
            'members': [
                {
                    'name': 'vasya',
                    'paid': 123.1,
                },
            ],
        },
    )
    body = await response.json()
    assert response.status == 200
    assert body
