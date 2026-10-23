
import pytest


@pytest.fixture
def sample_users():
    """Reusable sample API user data."""
    return [
        {
            "id": 1,
            "name": "Leanne Graham",
            "email": "leanne@example.com",
        },
        {
            "id": 2,
            "name": "Ervin Howell",
            "email": "ervin@example.com",
        },
    ]


@pytest.fixture
def empty_users():
    """Reusable empty API response."""
    return []


@pytest.fixture
def valid_page_sizes():
    """Valid minimum, typical, and maximum page sizes."""
    return [1, 10, 100]


@pytest.fixture
def invalid_page_sizes():
    """Invalid page sizes for boundary testing."""
    return [0, -1, 101]
