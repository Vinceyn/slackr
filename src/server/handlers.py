from flask_api import status

def generic_handler(err):
	return {
		"message": str(err)
	}, status.HTTP_500_INTERNAL_SERVER_ERROR

def ValueError_handler(err):
    return {
        "message": str(err)
    }, status.HTTP_400_BAD_REQUEST

def AccessError_handler(err):
    return {
        "message": str(err)
    }, status.HTTP_401_UNAUTHORIZED
