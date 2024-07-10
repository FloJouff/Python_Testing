# import pytest
# from server import app as flask_app


# @pytest.fixture(scope="module")
# def app():
#     flask_app.config["TESTING"] = True
#     return flask_app


# @pytest.fixture(scope="module")
# def client(app):
#     return app.test_client()


# @pytest.fixture(scope="module")
# def live_server(app):
#     import threading

#     server_thread = threading.Thread(target=lambda: app.run(port=5000))
#     server_thread.setDaemon(True)
#     server_thread.start()

#     yield "http://127.0.0.1:5000"
