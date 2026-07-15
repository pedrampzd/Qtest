import pytest

from factories import unique_user

pytestmark = pytest.mark.auth


def test_sign_up_success(client):
    user = unique_user()
    resp = client.sign_up(**user)
    assert resp.ok
    assert user["username"] in resp.message
    assert "successfully" in resp.message


def test_sign_up_duplicate_username_raises(client):
    user = unique_user()
    client.sign_up(**user)
    resp = client.sign_up(**user)
    assert not resp.ok
    assert resp.error is not None


def test_sign_in_success_tracks_online_user(client):
    user = unique_user()
    resp = client.register_and_login(**user)
    assert resp.ok
    assert client.is_online(user["username"])


def test_sign_in_wrong_password_raises(client):
    user = unique_user()
    client.sign_up(**user)
    resp = client.sign_in(user["username"], "wrong-password")
    assert not resp.ok
    assert "password is wrong" in str(resp.error)


def test_sign_in_unknown_user_raises(client):
    resp = client.sign_in("ghost", "nope")
    assert not resp.ok


def test_logout_removes_online_user(client):
    user = unique_user()
    client.register_and_login(**user)
    resp = client.logout(user["username"])
    assert resp.ok
    assert "signed out" in resp.message
    assert not client.is_online(user["username"])


def test_logout_without_sign_in_still_reports_success(client):
    resp = client.logout("never_logged_in")
    assert resp.ok
    assert "signed out successfully" in resp.message
