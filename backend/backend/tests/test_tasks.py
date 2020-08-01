import pytest
from django_redis import get_redis_connection


pytestmark = pytest.mark.django_db


def test_redis_connection():
    assert get_redis_connection()
