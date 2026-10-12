"""Tests for smart-routing configuration wiring."""

from types import SimpleNamespace


def _reset_config_cache(system_config):
    system_config._file_cache = None
    system_config._file_cache_key = None


def test_auto_route_config_file_and_confidence_env(monkeypatch, tmp_path):
    from xenon.repl import system_config

    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """\nauto_route:\n  enabled: true\n  confidence_threshold: 0.9\n  notify_user: false\n  switch_only_on_improvement: false\n""",
        encoding="utf-8",
    )
    monkeypatch.setattr(system_config, "CONFIG_PATH", config_path)
    monkeypatch.setenv("XENON_AUTO_ROUTE_CONFIDENCE", "0.8")
    monkeypatch.delenv("XENON_AUTO_ROUTE", raising=False)
    _reset_config_cache(system_config)

    config = system_config.get_config()

    assert config.auto_route.enabled is True
    assert config.auto_route.confidence_threshold == 0.8
    assert config.auto_route.notify_user is False
    assert config.auto_route.switch_only_on_improvement is False


def test_repl_initializes_router_from_auto_route_config(monkeypatch):
    from xenon.repl import repl as repl_module

    auto_route = SimpleNamespace(
        enabled=True,
        confidence_threshold=0.85,
        notify_user=False,
        switch_only_on_improvement=False,
    )
    monkeypatch.setattr(
        repl_module,
        "get_config",
        lambda: SimpleNamespace(auto_route=auto_route),
    )

    instance = repl_module.REPL(streaming=False)

    assert instance.intelligent_router.enabled is True
    assert instance.intelligent_router.confidence_threshold == 0.85
    assert instance.intelligent_router.notify_user is False
    assert instance.intelligent_router.switch_only_on_improvement is False
