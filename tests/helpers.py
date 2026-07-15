import json
import subprocess
import sys
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import zmq

PHON_BOOK_ROOT = Path(__file__).resolve().parents[1]


@dataclass
class ZmqResult:
    first_decode: Any
    parsed: Any
    double_encoded: bool


def _decode(raw: bytes) -> ZmqResult:
    first = json.loads(raw)
    if isinstance(first, str):
        try:
            return ZmqResult(first, json.loads(first), True)
        except json.JSONDecodeError:
            pass
    return ZmqResult(first, first, False)


@contextmanager
def zmq_client(ip: str = "127.0.0.1", timeout_ms: int = 5000):
    ctx = zmq.Context()
    socket = ctx.socket(zmq.REQ)
    socket.setsockopt(zmq.RCVTIMEO, timeout_ms)
    socket.setsockopt(zmq.SNDTIMEO, timeout_ms)
    port = socket.bind_to_random_port(f"tcp://{ip}", min_port=9100, max_port=9998)

    server = subprocess.Popen(
        [sys.executable, "server.py", "--ip", ip, "--port", str(port)],
        cwd=PHON_BOOK_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(0.5)

    def send(commands) -> ZmqResult:
        socket.send_json(commands)
        return _decode(socket.recv())

    try:
        yield SimpleNamespace(send=send)
    finally:
        socket.close()
        ctx.term()
        server.terminate()
        try:
            server.wait(timeout=3)
        except subprocess.TimeoutExpired:
            server.kill()
