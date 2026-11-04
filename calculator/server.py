import json
import logging
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from calculator.calc import CalculationError, calculate

logger = logging.getLogger(__name__)


def _debug_user_info(payload):
    if not isinstance(payload, dict):
        logger.debug("calculate user info missing")
        return
    logger.debug(
        "calculate user info operation=%s a=%s b=%s",
        payload.get("operation"),
        payload.get("a"),
        payload.get("b"),
    )


def outcome(payload):
    if not isinstance(payload, dict) or "a" not in payload or "b" not in payload:
        return 400, {"error": "a number is missing or is not a number"}
    try:
        result = calculate(payload.get("operation"), payload.get("a"), payload.get("b"))
    except CalculationError as error:
        return 400, {"error": str(error)}
    return 200, {"result": result}


class CalculatorHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/calculate":
            self._send(404, {"error": "unknown operation"})
            return
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b""
        try:
            payload = json.loads(raw.decode() or "null")
        except json.JSONDecodeError:
            logger.debug("calculate user info unreadable")
            self._send(400, {"error": "a number is missing or is not a number"})
            return
        _debug_user_info(payload)
        status, body = outcome(payload)
        self._send(status, body)

    def log_message(self, fmt, *args):
        return

    def _send(self, status, body):
        encoded = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def serve(host, port):
    return ThreadingHTTPServer((host, port), CalculatorHandler)


def main():
    server = serve("127.0.0.1", 8000)
    print("calculator listening on http://127.0.0.1:8000/calculate")
    server.serve_forever()


if __name__ == "__main__":
    main()
