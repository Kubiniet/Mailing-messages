import pytest

from message_service.users.tests.factories import AdminFactory

from .factories import ClientFactory


@pytest.fixture
def admin_creation():
    return AdminFactory.create()


@pytest.fixture
def client_creation():
    return ClientFactory.create()
