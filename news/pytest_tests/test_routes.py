from http import HTTPStatus

import pytest
from pytest_lazyfixture import lazy_fixture
from pytest_django.asserts import assertRedirects


AUTHOR_CLIENT = lazy_fixture('author_client')
AUTH_USER_CLIENT = lazy_fixture('auth_user_client')
ANONYMOUS_CLIENT = lazy_fixture('client')


@pytest.mark.parametrize(
    'name, client_type, method, expected_status',
    (
        ('home', ANONYMOUS_CLIENT, 'get', HTTPStatus.OK),
        ('detail', ANONYMOUS_CLIENT, 'get', HTTPStatus.OK),
        ('login', ANONYMOUS_CLIENT, 'get', HTTPStatus.OK),
        ('signup', ANONYMOUS_CLIENT, 'get', HTTPStatus.OK),
        ('logout', ANONYMOUS_CLIENT, 'post', HTTPStatus.OK),
        ('edit', AUTHOR_CLIENT, 'get', HTTPStatus.OK),
        ('delete', AUTHOR_CLIENT, 'get', HTTPStatus.OK),
        ('edit', AUTH_USER_CLIENT, 'get', HTTPStatus.NOT_FOUND),
        ('delete', AUTH_USER_CLIENT, 'get', HTTPStatus.NOT_FOUND),
    )
)
def test_pages_availability(
    name, client_type, method, expected_status, url_paths
):
    """Тестирование доступности страниц."""
    if method == 'post':
        response = client_type.post(url_paths[name])
    else:
        response = client_type.get(url_paths[name])
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name',
    ('edit', 'delete')
)
def test_redirect_for_anonymous_user(client, name, url_paths):
    """Тестирование перенаправления анонимного пользователя."""
    expected_url = f'{url_paths['login']}?next={url_paths[name]}'
    response = client.get(url_paths[name])
    assertRedirects(response, expected_url)
