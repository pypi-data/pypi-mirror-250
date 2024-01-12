"""Implementation of plugin utilities for pytest extensions"""

from abc import ABCMeta
from importlib.metadata import entry_points
from typing import LiteralString

import pytest
from synodic_utilities.utility import canonicalize_type


class BaseTests[PluginT](metaclass=ABCMeta):
    """Shared testing information for all plugin test classes."""

    @pytest.fixture(name="plugin_type", scope="session")
    def fixture_plugin_type(self) -> type[PluginT]:
        """A required testing hook that allows type generation. The user should override this fixture and return their custom plugin type"""

        raise NotImplementedError("Override this fixture in the plugin module")

    @pytest.fixture(name="plugin_group_name", scope="session")
    def fixture_plugin_group_name(self) -> LiteralString:
        """A required testing hook that provides identifying information. The user should override this fixture and return the base group name for their plugin type"""

        raise NotImplementedError("Override this fixture in the base test class")


class IntegrationTests[PluginT](metaclass=ABCMeta):
    """Integration testing information for all plugin test classes"""

    def test_entry_point(self, plugin_type: type[PluginT], plugin_group_name: LiteralString) -> None:
        """Verify that the plugin was registered

        Args:
            plugin_type: The type to register
            plugin_group_name: The group name for the plugin type
        """
        group = canonicalize_type(plugin_type).group

        types = []
        for entry in list(entry_points(group=f"{plugin_group_name}.{group}")):
            types.append(entry.load())

        assert plugin_type in types

    def test_name(self, plugin_type: type[PluginT]) -> None:
        """Verifies the the class name allows name extraction

        Args:
            plugin_type: The type to register
        """
        normalized = canonicalize_type(plugin_type)

        assert normalized.group != ""
        assert normalized.name != ""


class UnitTests[PluginT](metaclass=ABCMeta):
    """Unit testing information for all plugin test classes"""

    def test_plugin_construction(self, plugin: PluginT) -> None:
        """Verifies that the plugin being tested can be constructed

        Args:
            plugin: The data plugin fixture
        """
        assert plugin
