import unittest
import constants
from commands import report

class TestReport(unittest.TestCase):
    def test_get_report_message_returns_text_with_form_link(self):
        message = report.get_report_message()
        self.assertIsInstance(message, str)
        self.assertGreater(len(message), 0)
        self.assertIn(constants.REPORT_FORM_URL, message)

if __name__ == '__main__':
    unittest.main()
