from fastapi import status


class APIException(Exception):
    detail = "server error"
    code = status.HTTP_500_INTERNAL_SERVER_ERROR


class ItemNotFound(APIException):
    detail = "item not found"
    code = status.HTTP_404_NOT_FOUND


class ItemAlreadyExists(APIException):
    detail = "item already exists"
    code = status.HTTP_400_BAD_REQUEST


class AccessDenied(APIException):
    detail = "access denied"
    code = status.HTTP_403_FORBIDDEN


class Unauthorized(APIException):
    detail = "unauthorized"
    code = status.HTTP_401_UNAUTHORIZED
