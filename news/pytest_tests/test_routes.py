import pytest
from pytest_django.asserts import assertRedirects
from http import HTTPStatus


not_author_client = pytest.lazy_fixture('not_author_client')
author_client = pytest.lazy_fixture('author_client')
not_auth_client = pytest.lazy_fixture('not_auth_client')
EDIT_URL = pytest.lazy_fixture('edit_url')
DELETE_URL = pytest.lazy_fixture('delete_url')
HOME_URL = pytest.lazy_fixture('home_url')
LOGIN_URL = pytest.lazy_fixture('login_url')
LOGOUT_URL = pytest.lazy_fixture('logout_url')
SINGUP_URL = pytest.lazy_fixture('signup_url')
EDIT_REDIRECT = pytest.lazy_fixture('edit_redirect')
DELETE_REDIRECT = pytest.lazy_fixture('delete_redirect')


@pytest.mark.parametrize(
    'name, user, expected_status',
    (
        (EDIT_URL, author_client, HTTPStatus.OK),
        (EDIT_URL, not_author_client,
         HTTPStatus.NOT_FOUND),
        (DELETE_URL, not_author_client,
         HTTPStatus.NOT_FOUND),
        (DELETE_URL, author_client, HTTPStatus.OK),
        (HOME_URL, not_auth_client, HTTPStatus.OK),
        (LOGIN_URL, not_auth_client, HTTPStatus.OK),
        (LOGOUT_URL, not_auth_client, HTTPStatus.OK),
        (SINGUP_URL, not_auth_client, HTTPStatus.OK),
    ),
)
def test_pages_availability_for_different_users(
        name, user, expected_status
):
    response = user.get(name)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url, expected_url',
    (
        (EDIT_URL, EDIT_REDIRECT),
        (DELETE_URL, DELETE_REDIRECT),
    ),
)
def test_redirects(client, url, expected_url):
    response = client.get(url)
    assertRedirects(response, expected_url)
