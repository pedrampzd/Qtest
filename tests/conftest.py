import sys
from pathlib import Path

import pytest

PHON_BOOK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PHON_BOOK_ROOT))


@pytest.fixture(autouse=True)
def isolated_phon_book_db(monkeypatch):
    import server
    from core.models import create_database_tables, db

    monkeypatch.chdir(PHON_BOOK_ROOT)
    db.close()
    (PHON_BOOK_ROOT / "sab.db").unlink(missing_ok=True)
    create_database_tables()
    server.online_users.clear()


@pytest.fixture
def client():
    from phonebook_client import PhoneBookClient

    return PhoneBookClient()
