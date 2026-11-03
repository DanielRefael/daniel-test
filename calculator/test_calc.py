import json
import threading
import unittest
import urllib.error
import urllib.request

from calculator.calc import CalculationError, calculate
from calculator.server import serve


class CalculateTests(unittest.TestCase):
    def test_add_returns_the_sum(self):
        self.assertEqual(calculate("add", 2, 3), 5)

    def test_subtract_returns_the_difference(self):
        self.assertEqual(calculate("subtract", 10, 4), 6)

    def test_multiply_returns_the_product(self):
        self.assertEqual(calculate("multiply", 6, 7), 42)

    def test_divide_returns_the_quotient(self):
        self.assertEqual(calculate("divide", 8, 2), 4)

    def test_divide_by_zero_fails(self):
        with self.assertRaises(CalculationError):
            calculate("divide", 1, 0)

    def test_missing_number_fails(self):
        with self.assertRaises(CalculationError):
            calculate("add", None, 1)

    def test_non_number_fails(self):
        with self.assertRaises(CalculationError):
            calculate("add", "2", 1)

    def test_unknown_operation_fails(self):
        with self.assertRaises(CalculationError):
            calculate("power", 2, 3)


class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = serve("127.0.0.1", 0)
        cls.url = "http://127.0.0.1:%s/plus" % cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join(timeout=2)

    def post(self, payload):
        data = json.dumps(payload).encode()
        request = urllib.request.Request(
            self.url, data=data, headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(request) as response:
                return response.status, json.loads(response.read().decode())
        except urllib.error.HTTPError as error:
            with error:
                return error.code, json.loads(error.read().decode())

    def test_one_calculation_returns_one_result(self):
        status, body = self.post({"operation": "add", "a": 1, "b": 2})
        self.assertEqual(status, 200)
        self.assertEqual(body, {"result": 3})

    def test_bad_request_has_an_error_and_no_result(self):
        status, body = self.post({"operation": "divide", "a": 1, "b": 0})
        self.assertEqual(status, 400)
        self.assertIn("error", body)
        self.assertNotIn("result", body)

    def test_missing_number_has_an_error_and_no_result(self):
        status, body = self.post({"operation": "add", "a": 1})
        self.assertEqual(status, 400)
        self.assertNotIn("result", body)

    def test_unknown_operation_has_an_error_and_no_result(self):
        status, body = self.post({"operation": "power", "a": 2, "b": 3})
        self.assertEqual(status, 400)
        self.assertNotIn("result", body)

    def test_plus_logs_user_info_at_debug(self):
        with self.assertLogs("calculator.server", level="DEBUG") as captured:
            status, body = self.post({"operation": "add", "a": 1, "b": 2})
        self.assertEqual(status, 200)
        self.assertEqual(body, {"result": 3})
        self.assertTrue(
            any(
                "user info" in line and "operation=add" in line and "a=1" in line and "b=2" in line
                for line in captured.output
            )
        )

    def test_plus_logs_unreadable_user_info_and_keeps_the_error(self):
        data = b"not-json"
        request = urllib.request.Request(
            self.url, data=data, headers={"Content-Type": "application/json"}
        )
        with self.assertLogs("calculator.server", level="DEBUG") as captured:
            try:
                with urllib.request.urlopen(request) as response:
                    status, body = response.status, json.loads(response.read().decode())
            except urllib.error.HTTPError as error:
                with error:
                    status, body = error.code, json.loads(error.read().decode())
        self.assertEqual(status, 400)
        self.assertNotIn("result", body)
        self.assertTrue(any("user info unreadable" in line for line in captured.output))


if __name__ == "__main__":
    unittest.main()
