import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def test_get_client_list(admin_creation, client_creation):

    token = Token.objects.create(user=admin_creation)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    url = "/api/clients/"
    response = client.get(url)

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.data["total"] == 1
    assert len(response.data) == 2
