"""Tests for marketplace configuration files."""

import json

import pytest


class TestPluginJson:
    """Test .claude-plugin/plugin.json structure."""

    @pytest.fixture
    def plugin_json(self, skill_root):
        """Load plugin.json content."""
        path = skill_root / ".claude-plugin" / "plugin.json"
        return json.loads(path.read_text())

    def test_has_name(self, plugin_json):
        """plugin.json must have name field."""
        assert "name" in plugin_json
        assert plugin_json["name"] == "rhdh"

    def test_has_description(self, plugin_json):
        """plugin.json must have description field."""
        assert "description" in plugin_json
        assert len(plugin_json["description"]) > 10

    def test_has_version(self, plugin_json):
        """plugin.json must have version field."""
        assert "version" in plugin_json
        # Should be semver format
        version = plugin_json["version"]
        parts = version.split(".")
        assert len(parts) == 3, f"Version should be semver: {version}"

    def test_has_license(self, plugin_json):
        """plugin.json must have license field."""
        assert "license" in plugin_json

    def test_has_keywords(self, plugin_json):
        """plugin.json should have keywords array."""
        assert "keywords" in plugin_json
        assert isinstance(plugin_json["keywords"], list)
        assert len(plugin_json["keywords"]) > 0


class TestMarketplaceJson:
    """Test .claude-plugin/marketplace.json structure."""

    @pytest.fixture
    def marketplace_json(self, skill_root):
        """Load marketplace.json content."""
        path = skill_root / ".claude-plugin" / "marketplace.json"
        return json.loads(path.read_text())

    def test_has_name(self, marketplace_json):
        """marketplace.json must have name field."""
        assert "name" in marketplace_json
        assert marketplace_json["name"] == "rhdh"

    def test_has_owner(self, marketplace_json):
        """marketplace.json must have owner field."""
        assert "owner" in marketplace_json
        assert "name" in marketplace_json["owner"]

    def test_has_metadata(self, marketplace_json):
        """marketplace.json must have metadata field."""
        assert "metadata" in marketplace_json
        assert "version" in marketplace_json["metadata"]

    def test_has_plugins_array(self, marketplace_json):
        """marketplace.json must have plugins array."""
        assert "plugins" in marketplace_json
        assert isinstance(marketplace_json["plugins"], list)
        assert len(marketplace_json["plugins"]) >= 1

    def test_plugin_entry_has_required_fields(self, marketplace_json):
        """Each plugin entry must have required fields."""
        for plugin in marketplace_json["plugins"]:
            assert "name" in plugin
            assert "source" in plugin
            assert "version" in plugin
