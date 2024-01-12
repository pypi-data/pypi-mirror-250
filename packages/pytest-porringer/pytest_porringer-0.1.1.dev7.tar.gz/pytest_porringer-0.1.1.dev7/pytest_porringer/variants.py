"""Provides test data for plugin tests
"""

from collections.abc import Sequence

from porringer_core.plugin_schema.environment import Environment

from pytest_porringer.mock.environment import MockEnvironment


def _mock_environment_list() -> Sequence[type[Environment]]:
    """Mocked list of environments

    Returns:
        List of mock environments
    """
    variants = []

    # Default
    variants.append(MockEnvironment)

    return variants


environment_variants = _mock_environment_list()
