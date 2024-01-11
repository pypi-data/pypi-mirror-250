import jwt
from flask import Flask, jsonify


class JWTAuthMiddleware:
    """
    The JWTAuthMiddleware class is a middleware class that provides authentication functionality for a Flask application.

    Attributes:
        app (Flask): The Flask application object.
        secret_key (str): The secret key used for JWT token verification.

    Methods:
        __init__(self, app: Flask, secret_key: str): Initializes the AuthMiddleware object with the Flask application and secret key.
        verify_jwt(self, token: str): Verifies the JWT token using the secret key.
        __call__(self, environ, start_response): The middleware function that is called for each request.

    To use this JWTAuthMiddleware in a Flask application, follow these steps:

    1. Create a Flask application object:
        app = Flask(__name__)

    2. Define a secret key for JWT token verification:
        secret_key = "secret_key"

    3.Initialize the JWTAuthMiddleware object with the Flask application and secret key:
        app.wsgi_app = JWTAuthMiddleware(app, secret_key=secret_key)

    4. All the routes will be protected now.
        @app.route("/protected")
        def secure_data():
            # Access user information set by the middleware
            user_info = request.environ.get("user", {})
            return jsonify({"message": "This is secure data", "user": user_info})

    5. Run Flask application
        if __name__ == "__main__":
                app.run()
    """

    def __init__(
        self,
        app: Flask,
        secret_key: str,
    ):
        self.app = app
        self.secret_key = secret_key
        self.original_app = app.wsgi_app

    def __call__(
        self,
        environ,
        start_response,
    ):
        try:
            authorization_header = environ.get("HTTP_AUTHORIZATION", "")
            if not authorization_header or not authorization_header.startswith(
                "Bearer "
            ):
                return self.handle_error(
                    start_response,
                    "Invalid Credentials",
                    status="401 Unauthorized",
                )

            token = authorization_header.split("Bearer ")[1]
            decoded_token = self.verify_jwt(token)
            environ["user"] = decoded_token
            return self.original_app(environ, start_response)

        except ValueError as exc:
            return self.handle_error(
                start_response,
                str(exc),
                status="401 Unauthorized",
            )

        except Exception as exc:
            return self.handle_error(
                start_response,
                f"Unexpected error: {str(exc)}",
                status="500 Internal Server Error",
            )

    def verify_jwt(
        self,
        token: str,
    ):
        try:
            decoded_token = jwt.decode(
                token,
                self.secret_key,
                algorithms=["HS256"],
            )
            return decoded_token
        except jwt.ExpiredSignatureError as exc:
            raise ValueError(f"Token has expired. {str(exc)}")
        except jwt.InvalidTokenError as exc:
            raise ValueError(f"Invalid Token. {str(exc)}")

    def handle_error(
        self,
        start_response,
        message,
        status="400 Bad Request",
    ):
        with self.app.app_context():
            response_body = jsonify({"message": message})
            headers = [("Content-Type", "application/json")]

            start_response(status, headers)
            return [response_body.get_data()]
