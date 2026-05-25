import pytest
from utils.savanna_client import SavannaClient


@pytest.fixture(scope="session")
def client():
    return SavannaClient()