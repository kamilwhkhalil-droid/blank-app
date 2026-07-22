from streamlit.testing.v1 import AppTest


def test_app_runs_without_exception():
    at = AppTest.from_file("streamlit_app.py").run()
    assert not at.exception


def test_app_shows_title():
    at = AppTest.from_file("streamlit_app.py").run()
    assert len(at.title) == 1
    assert "My new app" in at.title[0].value
