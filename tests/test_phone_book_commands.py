import pytest

from factories import unique_contact

pytestmark = pytest.mark.contacts


def test_add_phone_user_with_explanation(client):
    contact = unique_contact(explanation="colleague")
    client.add_contact(**contact)
    resp = client.by_name(contact["username"])
    assert resp.ok
    assert resp.data["name"] == contact["username"]
    assert contact["phone_number"] in resp.data["phone_numbers"]


def test_add_phone_user_without_explanation_defaults_empty(client):
    contact = unique_contact()
    contact.pop("explanation")
    client.add_contact(**contact)
    resp = client.all_contacts()
    match = [u for u in resp.data if u["name"] == contact["username"]][0]
    assert match["explanation"] == ""


def test_add_second_phone_number(client):
    contact = unique_contact()
    second_number = unique_contact()["phone_number"]
    client.add_contact(**contact)
    client.add_number(contact["username"], second_number)
    resp = client.by_name(contact["username"])
    assert sorted(resp.data["phone_numbers"]) == sorted(
        [contact["phone_number"], second_number]
    )


def test_edit_phone_user_rename_and_number(client):
    contact = unique_contact()
    new_username = contact["username"] + "_edited"
    new_number = unique_contact()["phone_number"]
    client.add_contact(**contact)
    client.edit_contact(
        contact["username"], contact["phone_number"], new_username, new_number
    )
    resp = client.by_name(new_username)
    assert resp.ok
    assert resp.data["phone_numbers"] == [new_number]


def test_get_all_phone_users_groups_numbers(client):
    contact_a = unique_contact()
    contact_b = unique_contact()
    extra_number = unique_contact()["phone_number"]
    client.add_contact(**contact_a)
    client.add_number(contact_a["username"], extra_number)
    client.add_contact(**contact_b)

    resp = client.all_contacts()
    by_name = {u["name"]: u for u in resp.data}
    assert sorted(by_name[contact_a["username"]]["phone_number"]) == sorted(
        [contact_a["phone_number"], extra_number]
    )
    assert by_name[contact_b["username"]]["phone_number"] == [contact_b["phone_number"]]


@pytest.mark.search
def test_get_phone_user_by_number(client):
    contact = unique_contact()
    client.add_contact(**contact)
    resp = client.by_number(contact["phone_number"])
    assert resp.data["name"] == contact["username"]
    assert contact["phone_number"] in resp.data["phone_numbers"]


def test_remove_phone_user(client):
    contact = unique_contact()
    client.add_contact(**contact)
    client.remove_contact(contact["username"])
    resp = client.by_name(contact["username"])
    assert not resp.ok


def test_duplicate_phone_number_rejected(client):
    first = unique_contact()
    client.add_contact(**first)
    duplicate = unique_contact(phone_number=first["phone_number"])
    resp = client.add_contact(**duplicate)
    assert not resp.ok


@pytest.mark.search
def test_get_by_name_missing_user_raises(client):
    resp = client.by_name("missing")
    assert not resp.ok


def test_phone_book_operations_do_not_require_auth(client):
    contact = unique_contact(explanation="no auth")
    resp = client.add_contact(**contact)
    assert resp.ok
    assert "successfully" in resp.message
