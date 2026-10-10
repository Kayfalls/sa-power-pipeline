from unittest.mock import patch

import pytest

import sa_power_pipeline.fetch_status as extract_module


def test_main_raises_when_an_endpoint_fails():
    with (
        patch.object(extract_module, "fetch_status", return_value={"ok": 1}),
        patch.object(extract_module, "fetch_area", return_value=None),
        patch.object(extract_module, "fetch_schedule", return_value={"ok": 1}),
    ):
        with pytest.raises(RuntimeError, match="area"):
            extract_module.main()