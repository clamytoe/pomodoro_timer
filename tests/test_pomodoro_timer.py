"""
test_pomodoro_timer.py

Tests for pomodoro_timer.
"""
import logging
import pytest
from pomodoro_timer import app

logging.disable(logging.CRITICAL)


@pytest.fixture
def timer():
    return app.Pomodoro(1, breaks=1, interval=2)


def test_main_with_no_args():
    with pytest.raises(SystemExit):
        app.main()


def test_class_initialization(timer):
    assert timer.p_duration == 3600
    assert timer.p_breaks == 60
    assert timer.p_interval == 120
    assert timer.status == "IDLE"
    assert timer.rounds == 0


def test_start_interval(capfd, timer):
    timer.start_interval()
    output = capfd.readouterr()[0]
    assert "Next break" in output
    assert timer.status == "ACTIVE"
    assert timer.rounds == 1


def test_start_break(capfd, timer):
    timer.start_break()
    output = capfd.readouterr()[0]
    assert "Start again at" in output
    assert timer.status == "RESPITE"


def test_done_alarm(timer):
    timer.play("done")
    pass
