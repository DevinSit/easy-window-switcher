from click.testing import CliRunner
from utils.helpers_test import CustomTestCase
from easywindowswitcher import main


class TestCli(CustomTestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.cli = main.cli

    def test_short_help_option_enabled(self):
        result = self.runner.invoke(self.cli, ["-h"])
        self.assert_result_ok(result)
