from flask import request, jsonify
from services import APIKeyService


api_service = APIKeyService()


def private(func):
    """
    this decorator is for authorization for only requests
    which contain the API key. If API Key is invalid this
    decorator returns a 401 Unauthorized response and blocks
    the user from accessing the APIs.
    """

    def wrapper(*args, **kwargs):
        request_ipaddr = request.remote_addr
        authorization_header = request.headers.get('Authorization')

        if not authorization_header:
            return jsonify({
                "detail": "You need to provide valid api key to access." +
                " Contact an administrator for a valid API key"
            }), 401

        api_key = authorization_header.strip()
        is_valid = api_service.is_apikey_valid(api_key, request_ipaddr)

        if not is_valid:
            return jsonify({
                "detail": "You are not authorized as api key invalid." +
                " Contact an administrator for a valid API key"
            }), 401

        return func(*args, **kwargs)

    return wrapper
