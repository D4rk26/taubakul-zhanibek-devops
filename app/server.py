#!/usr/bin/env python3
"""Minimal HTTP application for the DevOps Docker laboratory."""

from __future__ import annotations

import os
import signal
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Mapping
from urllib.parse import urlsplit


STUDENT_FIELDS = (
    ("Name", "STUDENT_NAME", "Zhanibek"),
    ("Surname", "STUDENT_SURNAME", "Taubakul"),
    ("Group", "STUDENT_GROUP", "IT2-2302"),
    ("Student ID", "STUDENT_ID", "37650"),
)


def load_student_info(environ: Mapping[str, str] | None = None) -> dict[str, str]:
    """Load validated student information from environment variables."""
    source = os.environ if environ is None else environ
    result: dict[str, str] = {}
    for label, variable, default in STUDENT_FIELDS:
        value = source.get(variable, default).strip()
        if not value:
            raise ValueError(f"{variable} must not be empty")
        if "\n" in value or "\r" in value:
            raise ValueError(f"{variable} must not contain line breaks")
        result[label] = value
    return result


def render_student_info(student: Mapping[str, str]) -> str:
    """Render the personalized output required by Task 11."""
    return "\n".join(
        (
            "================================",
            "DevOps Student Application",
            "================================",
            "",
            f"Name: {student['Name']}",
            f"Surname: {student['Surname']}",
            f"Group: {student['Group']}",
            f"Student ID: {student['Student ID']}",
            "",
            "Application is running successfully!",
            "",
        )
    )


class StudentRequestHandler(BaseHTTPRequestHandler):
    """Serve the student page and a lightweight health endpoint."""

    student_info: Mapping[str, str] = {}
    server_version = "TaubakulDevOps/1.0"
    sys_version = ""

    def _respond(self, status: int, body: str) -> None:
        encoded = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        path = urlsplit(self.path).path
        if path == "/":
            self._respond(200, render_student_info(self.student_info))
        elif path == "/health":
            self._respond(200, "OK\n")
        else:
            self._respond(404, "Not Found\n")

    def log_message(self, message_format: str, *args: object) -> None:
        message = message_format % args
        print(f"INFO request client={self.client_address[0]} {message}", flush=True)


def parse_port(environ: Mapping[str, str] | None = None) -> int:
    """Return a validated TCP port."""
    source = os.environ if environ is None else environ
    raw_port = source.get("PORT", "8080")
    try:
        port = int(raw_port)
    except ValueError as error:
        raise ValueError("PORT must be an integer") from error
    if not 1 <= port <= 65535:
        raise ValueError("PORT must be between 1 and 65535")
    return port


def main() -> int:
    """Validate configuration and run the HTTP server."""
    try:
        student = load_student_info()
        port = parse_port()
    except ValueError as error:
        print(f"ERROR configuration: {error}", file=sys.stderr, flush=True)
        return 2

    StudentRequestHandler.student_info = student
    print(render_student_info(student), end="", flush=True)
    print(f"INFO server listening on 0.0.0.0:{port}", flush=True)
    server = ThreadingHTTPServer(("0.0.0.0", port), StudentRequestHandler)

    def handle_termination(signum: int, _frame: object) -> None:
        print(f"INFO server received signal {signum}", flush=True)
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, handle_termination)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("INFO server interrupted", flush=True)
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
