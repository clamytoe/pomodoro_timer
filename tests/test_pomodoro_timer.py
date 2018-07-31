"""
test_pomodoro_timer.py

Tests for pomodoro_timer.
"""
import pytest
from pomodoro_timer import app


@pytest.fixture
def timer():
    return app.Pomodoro(1, breaks=1, interval=2)


def test_main_with_no_args():
    with pytest.raises(SystemExit):
        app.main()


@pytest.fixture(params=["--help"])
def test_help(capfd):
    app.main()
    output = capfd.readouterr()[0]
    assert "usage" in output.strip()


@pytest.fixture(params=["1"])
def test_help():
    params = app.get_args()
    assert isinstance(params, app.Params)
    assert params.duration == 1
    assert params.breaks == 5
    assert params.interval == 25


def test_class_initialization(timer):
    assert timer.start_time is None
    assert timer.stop_time is None
    assert timer.duration == 3600
    assert timer.break_length == 60
    assert timer.interval == 120
    assert timer.status == "IDLE"
    assert timer.rounds == 0


def test_start_interval(capfd, timer):
    assert timer.break_time is None
    timer.start_interval()
    output = capfd.readouterr()[0]
    assert "Next break" in output
    assert timer.break_time is not None
    assert timer.work_time is None
    assert timer.status == "ACTIVE"
    assert timer.rounds == 1


def test_start_break(capfd, timer):
    assert timer.work_time is None
    timer.start_break()
    output = capfd.readouterr()[0]
    assert "Start again at" in output
    assert timer.work_time is not None
    assert timer.break_time is None
    assert timer.status == "BREAK"


def test_done_alarm(timer):
    timer.play("done")
    pass
