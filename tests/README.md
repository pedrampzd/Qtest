# Automated tests — Graph Q-Test

Python automated tests for the phone book SUT (`src/phon_book/`).

## Approach

- **Command-layer tests** (`test_auth_commands.py`, `test_phone_book_commands.py`): call `core.factory_command.call_func` directly — same path the ZMQ server uses. Fast, deterministic, fresh `sab.db` per test. These assert on the bare command result; the `{command_name, result}` response envelope is out of scope here because it is built by `server.py`, not `call_func`.
- **Transport-layer tests** (`test_zmq_protocol.py`): spawn `server.py` as a subprocess and send JSON over ZeroMQ with the SUT’s inverted pairing (**client binds REQ**, **server connects REP**). This is the only layer where the `{command_name, result}` envelope is observable (`test_zmq_happy_path_sign_up_and_add_contact` asserts it).

## Environment

Tested on **Python 3.11.7** (macOS).

## Setup

```bash
cd phon_book
python3 -m venv .venv
source .venv/bin/activate
pip install -r tests/requirements.txt
```

## Run

```bash
cd phon_book && source .venv/bin/activate
pytest tests -v
```

Each test deletes `sab.db` before/after and clears `server.online_users`.

## Reviewer deliverables (`output/`)

| File | Description |
|------|-------------|
| [01-test-cases.pdf](./output/01-test-cases.pdf) | Test cases |
| [02-test-scenarios.pdf](./output/02-test-scenarios.pdf) | Test scenarios |
| [03-manual-test-cases.pdf](./output/03-manual-test-cases.pdf) | Manual test cases |
| [04-manual-execution.mp4](./output/04-manual-execution.mp4) | Screen recording of manual test execution (~16 min, 15 July 2026) |
| [`tests/`](./) | Automated test suite (pytest) |
| [05-test-report-openui.html](./output/05-test-report-openui.html) | Interactive OpenUI report (offline; uses `output/openui-assets/`) |

## Files

| File | Purpose |
|------|---------|
| `conftest.py` | DB isolation, `call` fixture |
| `helpers.py` | ZMQ client harness, auth helper |
| `test_auth_commands.py` | sign_up / sign_in / logout |
| `test_phone_book_commands.py` | contacts CRUD + search |
| `test_zmq_protocol.py` | end-to-end ZMQ + double-encoding check |
