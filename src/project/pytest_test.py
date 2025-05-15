from project import hello

# filepath: /workspaces/python-uv/src/project/test_hello.py


def test_hello_returns_value():
    """Test that hello function returns a value."""
    result = hello()
    assert result == "Hello from python-uv!"
