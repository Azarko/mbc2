import http


async def test_index(web_app_client):
    response = await web_app_client.get('/')
    assert response.status == http.HTTPStatus.OK
    body = await response.text()
    assert 'Hello, world!' in body
