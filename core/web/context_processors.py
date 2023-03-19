from . import bm_user


def auth_user(request):
    response = {}

    if not request.user.is_authenticated:
        return response

    user_info = bm_user.get_user(request.user.passport)
    response["user_info"] = user_info

    return response
