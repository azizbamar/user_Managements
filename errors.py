import requests
HTTP_400_BAD_REQUEST = 400
HTTP_401_UNAUTHORIZED = 401
HTTP_403_FORBIDDEN = 403
HTTP_404_NOT_FOUND = 404
HTTP_429_TOO_MANY_REQUESTS = 429
HTTP_500_INTERNAL_SERVER_ERROR = 500
HTTP_409_INTERNAL_SERVER_ERROR = 409

HTTP_EXCEPTIONS = {
    HTTP_400_BAD_REQUEST: requests.exceptions.HTTPError,
    HTTP_401_UNAUTHORIZED: requests.exceptions.HTTPError,
    HTTP_403_FORBIDDEN: requests.exceptions.HTTPError,
    HTTP_404_NOT_FOUND: requests.exceptions.HTTPError,
    HTTP_429_TOO_MANY_REQUESTS: requests.exceptions.HTTPError,
    HTTP_500_INTERNAL_SERVER_ERROR: requests.exceptions.HTTPError,
    HTTP_409_INTERNAL_SERVER_ERROR:requests.exceptions.HTTPError,
}