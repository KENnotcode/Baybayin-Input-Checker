from app import BaybayinApp
from baybayin.models import CheckResult
from baybayin_gui.controller import CheckerController


def test_gui_exposes_only_check_action():
    assert hasattr(BaybayinApp, "check_input")
    assert not hasattr(BaybayinApp, "set_sample")


def test_controller_preserves_diagnostics():
    received: list[CheckResult] = []
    controller = CheckerController(received.append)

    result = controller.check_text("ᜋ᜕᜕")

    assert result.valid is False
    assert "DOUBLE_VIRAMA" in {error.rule for error in result.errors}
    assert received == [result]
