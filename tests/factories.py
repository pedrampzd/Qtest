import itertools

_counter = itertools.count(1)


def unique_user(**overrides):
    n = next(_counter)
    return {
        "username": f"user_{n}",
        "password": "pass123",
        "email": f"user_{n}@example.com",
        **overrides,
    }


def unique_contact(**overrides):
    n = next(_counter)
    return {
        "username": f"contact_{n}",
        "phone_number": str(1_000_000 + n),
        "explanation": "test contact",
        **overrides,
    }
