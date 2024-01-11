from unittest.mock import Mock

import jwt
from flask import jsonify


def test_successful_verification(
    app,
    middleware,
    secret_key,
    valid_jwt,
):
    environ = {
        "REQUEST_METHOD": "GET",
        "PATH_INFO": "/",
        "wsgi.url_scheme": "http",
        "HTTP_AUTHORIZATION": f"Bearer {valid_jwt}",
    }

    with app.test_request_context(
        environ["PATH_INFO"], method=environ["REQUEST_METHOD"]
    ):
        start_response = Mock()
        middleware(environ, start_response)
        expected_payload = jwt.decode(valid_jwt, secret_key, algorithms=["HS256"])
        assert "user" in environ
        assert environ["user"] == expected_payload


def test_missing_header(
    app,
    middleware,
):
    environ = {
        "REQUEST_METHOD": "GET",
        "PATH_INFO": "/",
        "wsgi.url_scheme": "http",
    }
    with app.test_request_context(
        environ["PATH_INFO"], method=environ["REQUEST_METHOD"]
    ):
        start_response = Mock()
        response_middleware = middleware(environ, start_response)

        assert response_middleware == [
            jsonify({"message": "Invalid Credentials"}).get_data()
        ]


def test_invalid_token(
    app,
    invalid_jwt,
    middleware,
):
    environ = {
        "REQUEST_METHOD": "GET",
        "PATH_INFO": "/",
        "wsgi.url_scheme": "http",
        "HTTP_AUTHORIZATION": f"Bearer {invalid_jwt}",
    }
    with app.test_request_context(
        environ["PATH_INFO"], method=environ["REQUEST_METHOD"]
    ):
        start_response = Mock()
        response_middleware = middleware(environ, start_response)

        assert response_middleware == [
            jsonify(
                {"message": "Invalid Token. Signature verification failed"}
            ).get_data()
        ]


def test_expired_token(
    app,
    middleware,
    expired_jwt,
):
    environ = {
        "REQUEST_METHOD": "GET",
        "PATH_INFO": "/",
        "wsgi.url_scheme": "http",
        "HTTP_AUTHORIZATION": f"Bearer {expired_jwt}",
    }
    with app.test_request_context(
        environ["PATH_INFO"], method=environ["REQUEST_METHOD"]
    ):
        start_response = Mock()
        response_middleware = middleware(environ, start_response)

        assert response_middleware == [
            jsonify({"message": "Token has expired. Signature has expired"}).get_data()
        ]
