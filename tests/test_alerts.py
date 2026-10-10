from unittest.mock import Mock, patch

from sa_power_pipeline.alerts import send_discord_alert


def test_alert_skipped_without_webhook(monkeypatch):
    monkeypatch.delenv("DISCORD_WEBHOOK_URL", raising=False)
    assert send_discord_alert("hello") is False


def test_alert_posts_to_webhook(monkeypatch):
    monkeypatch.setenv("DISCORD_WEBHOOK_URL", "https://example.com/hook")
    with patch("sa_power_pipeline.alerts.requests.post") as post:
        post.return_value = Mock(ok=True, status_code=204)
        assert send_discord_alert("hello") is True
    post.assert_called_once()


def test_alert_handles_rejection(monkeypatch):
    monkeypatch.setenv("DISCORD_WEBHOOK_URL", "https://example.com/hook")
    with patch("sa_power_pipeline.alerts.requests.post") as post:
        post.return_value = Mock(ok=False, status_code=404)
        assert send_discord_alert("hello") is False