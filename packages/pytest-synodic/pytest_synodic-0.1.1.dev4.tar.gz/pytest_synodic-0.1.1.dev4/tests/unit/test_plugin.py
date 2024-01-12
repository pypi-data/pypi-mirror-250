"""Verifies the plugin utilities work as expected"""

from pytest_synodic.plugin import IntegrationTests, UnitTests


class TestPluginUtilities:
    """Verifies the plugin utilities work as expected"""

    def test_unit_tests(self):
        """Verifies the unit test class works as expected"""
        assert UnitTests

    def test_integration_tests(self):
        """Verifies the integration test class works as expected"""
        assert IntegrationTests
