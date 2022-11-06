from django.http.response import JsonResponse

def handler404(request, *args, **argv):
    data = {
        "code": 40006,
        "error": True,
        "data": {},
        "detail": "you request resource not found, please check you request and try again!"
    }
    return JsonResponse(data)