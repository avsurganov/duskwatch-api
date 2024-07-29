from app.models.common.common_model import ErrorResponse

common_responses = {
    400: {"model": ErrorResponse, "description": "Bad Request"},
    401: {"model": ErrorResponse, "description": "Unauthorized"},
    403: {"model": ErrorResponse, "description": "Forbidden"},
    404: {"model": ErrorResponse, "description": "Not Found"},
    405: {"model": ErrorResponse, "description": "Method Not Allowed"},
    406: {"model": ErrorResponse, "description": "Not Acceptable"},
    408: {"model": ErrorResponse, "description": "Request Timeout"},
    422: {"model": ErrorResponse, "description": "Unprocessable Entity"},
    500: {"model": ErrorResponse, "description": "Internal Server Error"},
    501: {"model": ErrorResponse, "description": "Not Implemented"},
    502: {"model": ErrorResponse, "description": "Bad Gateway"},
    503: {"model": ErrorResponse, "description": "Service Unavailable"},
    504: {"model": ErrorResponse, "description": "Gateway Timeout"},
    505: {"model": ErrorResponse, "description": "HTTP Version Not Supported"},
}
