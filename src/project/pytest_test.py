from project import hello


def test_hello_returns_value():
    """Test that hello function returns a value."""
    result = hello("world")
    assert result == "Hello, world"
