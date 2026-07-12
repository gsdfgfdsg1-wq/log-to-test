import unittest
from log_to_test import cluster, generate


class LogToTestTests(unittest.TestCase):
    def test_clusters_identical_root_causes(self):
        cases = cluster([{ "exception": "Timeout", "operation": "fetch" }, { "exception": "Timeout", "operation": "fetch" }])
        self.assertEqual(cases[0]["count"], 2)

    def test_redacts_context_secrets(self):
        case = cluster([{ "context": "token=abc", "exception": "X", "operation": "y" }])[0]
        self.assertEqual(case["example"], "token=[REDACTED]")

    def test_generates_unittest_method(self):
        code = generate({"exception": "ValueError", "operation": "parse"})
        self.assertIn("def test_parse_valueerror", code)
        self.assertIn("assertRaises", code)


if __name__ == "__main__":
    unittest.main()
